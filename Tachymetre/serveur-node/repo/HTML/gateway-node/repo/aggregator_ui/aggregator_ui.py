#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
An aggregator of sensors values
"""

# ------------------------------------------------------------------------------

# iPOPO
from pelix.ipopo import constants
from pelix.ipopo.decorators import ComponentFactory, Requires, \
    Validate, Invalidate, Property
import pelix.http

# Standard library
import logging
import time

# ------------------------------------------------------------------------------

_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

import sys
if sys.version_info[0] == 3:
    # Python 3
    def _to_string(data, encoding="UTF-8"):
        """
        Converts the given bytes array to a string
        """
        if type(data) is str:
            # Nothing to do
            return data

        return str(data, encoding)

else:
    # Python 2
    def _to_string(data, encoding="UTF-8"):
        """
        Converts the given bytes array to a string
        """
        if type(data) is str:
            # Nothing to do
            return data

        return data.encode(encoding)

# ------------------------------------------------------------------------------

@ComponentFactory("aggregator-ui-factory")
@Property("_name", constants.IPOPO_INSTANCE_NAME)
@Property("_path", pelix.http.HTTP_SERVLET_PATH, "/PythonSensor")
@Requires("_aggregator", "java:/speed.aggregator.AggregatorService",
          optional=True)
@Requires("_http", pelix.http.HTTP_SERVICE)
class AggregatorServlet(object):
    """
    Speed sensor
    """
    def __init__(self):
        """
        Constructor
        """
        self._name = ""

        self._aggregator = None
        self._http = None


    def _format_timestamp(self, time_stamp):
        """
        Format the given time (in seconds) to string
        """
        return time.strftime("%H:%M:%S", time.localtime(time_stamp))


    def _make_sensor_part(self, name, history):
        """
        Prepares a HTML title and a table containing sensor history
        
        :param name: Sensor name
        :param history: Sensor history
        :return: A HTML paragraph
        """
        table_rows = ("""
<tr>
<td>{time}</td>
<td>{value:.2f}</td>
<td>{unit}</td>
<td>{direction}</td>
</tr>""".format(time=self._format_timestamp(entry["time"] / 1000.),
                value=entry["value"], unit=_to_string(entry["unit"]), direction=entry["direction"])
        for entry in history)

        return """
<td>
<h2>Sensor {name}</h2>
<table class="result">
<tr>
<th>Time Stamp</th>
<th>Value</th>
<th>Unit</th>
<th>Direction</th>
</tr>{rows}
</table>
</td>""".format(name=name, rows=''.join(table_rows))


    def do_GET(self, request, response):
        """
        Handles a GET request
        
        :param request: The HTTP request bean
        :param request: The HTTP response handler
        """
        output = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="refresh" content="1">
<style>
body {{
    font:12px arial,sans-serif;
}}
table {{
    font:12px arial,sans-serif;
}}
table.main {{
    border:solid blue 1px;
    width:100%;
}}
table.result {{
    border:solid red 1px;
    margin:20px;
}}
td {{
    border:solid black 1px;
    padding:5px
}}
</style>
<title>Tachymetre - {name}</title>
</head>
<body>
<h1>Tachymetre - {name}</h1>
""".format(name=self._name)

        if not self._aggregator:
            output += "<p>Aggregator service unavailable</p>"

        else:
            output += "<p>Aggregator found</p>"
            history = self._aggregator.get_history()
	    active_sensors = self._aggregator.get_active_sensors()	
            output += "\n<table class=\"main\"><tr>"
	    output += "\n<a href=\"accueil\">accueil</a>"
            output += '\n'.join((self._make_sensor_part(name, history[name])
                                 for name in sorted(history)))
            output += "\n</tr></table>"

        output += """
</body>
</html>
"""

        # Send the result
        response.send_content(200, output)


    @Validate
    def validate(self, context):
        """
        Component validation
        """
        # Register the servlet
        self._http.register_servlet(self._path, self)

        _logger.info("Component %s validated", self._name)


    @Invalidate
    def invalidate(self, context):
        """
        Component invalidation
        """
        # Unregister the servlet
        self._http.unregister(None, self)

        _logger.info("Component %s invalidated", self._name)
