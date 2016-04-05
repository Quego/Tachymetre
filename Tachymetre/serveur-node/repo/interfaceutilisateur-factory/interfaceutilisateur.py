from pelix.ipopo import constants
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property

import pelix.http
import logging
import time
import sys

_logger = logging.getLogger(__name__)

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

@ComponentFactory("interfaceutilisateur-factory")
@Property("_name", constants.IPOPO_INSTANCE_NAME)
@Property("_path", pelix.http.HTTP_SERVLET_PATH, "/PythonSensor")
@Requires("_apirest", "DonneesService", optional = True)
@Requires("_http", pelix.http.HTTP_SERVICE)
class Interfaceutilisateur(object):

	def __init__(self):
		self._apirest = None
		self._name = ""
		self._http = None

	def get_donnees_elaborees(self):
		data = self._apirest.send_donnees_elaborees()

	def _make_histo(self):
		min_data = self._apirest.get_vitesse_min()
		max_data = self._apirest.get_vitesse_max()

		min = 0
		max = 0
		try:
			min = round(min_data[0][0],1)
			max = round(max_data[0][0],1)
		except TypeError as ex:
			_logger.error("Error retrieving sensor data: %s", ex)



		nb_data = self._apirest.get_vitesse_entre_deux_bornes(min, max)

		try:
			nb = nb_data[0][0]
		except TypeError as ex:
			_logger.error("Error retrieving sensor data: %s", ex)


		if ((max - min < 2.0) or nb < 2):
			return """	
			<div id="histogramme">
			<dl>
				<dt><a href="#1" title="{min}-{max}">{min}-{max}</a></dt>
				<dd style="border-bottom-width: 200px; height: 0px;">{nb}</dd>
			</dl>
			</div>""".format(min=min,max = max, nb = nb)
		else:
			step = (float(max) - float(min))/10.0

			step1 = round(min + step,1)
			step2 = round(min + 2*step,1)
			step3 = round(min + 3*step,1)
			step4 = round(min + 4*step,1)
			step5 = round(min + 5*step,1)
			step6 = round(min + 6*step,1)
			step7 = round(min + 7*step,1)
			step8 = round(min + 8*step,1)
			step9 = round(min + 9*step,1)
			value1 = self._apirest.get_vitesse_entre_deux_bornes(min, step1)[0][0]
			value2 = self._apirest.get_vitesse_entre_deux_bornes(step1, step2)[0][0]
			value3 = self._apirest.get_vitesse_entre_deux_bornes(step2, step3)[0][0]
			value4 = self._apirest.get_vitesse_entre_deux_bornes(step3, step4)[0][0]
			value5 = self._apirest.get_vitesse_entre_deux_bornes(step4, step5)[0][0]
			value6 = self._apirest.get_vitesse_entre_deux_bornes(step5, step6)[0][0]
			value7 = self._apirest.get_vitesse_entre_deux_bornes(step6, step7)[0][0]
			value8 = self._apirest.get_vitesse_entre_deux_bornes(step7, step8)[0][0]
			value9 = self._apirest.get_vitesse_entre_deux_bornes(step8, step9)[0][0]
			value10 = self._apirest.get_vitesse_entre_deux_bornes(step9, max)[0][0]
			percent1 = 200*value1/nb
			percent2 = 200*value2/nb
			percent3 = 200*value3/nb
			percent4 = 200*value4/nb
			percent5 = 200*value5/nb
			percent6 = 200*value6/nb
			percent7 = 200*value7/nb
			percent8 = 200*value8/nb
			percent9 = 200*value9/nb
			percent10 = 200*value10/nb
			return """	
			<div id="histogramme">
			<dl>
				<dt><a href="#1" title="{min}-{step1}">{min}-{step1}</a></dt>
				<dd style="border-bottom-width: {percent1}px; height: {mpercent1}px;">{value1}</dd>
			</dl>
			<dl>
				<dt><a href="#2" title="{step1}-{step2}">{step1}-{step2}</a></dt>
				<dd style="border-bottom-width: {percent2}px; height: {mpercent2}px;">{value2}</dd>
			</dl>
			<dl>
				<dt><a href="#3" title="{step2}-{step3}">{step2}-{step3}</a></dt>
				<dd style="border-bottom-width: {percent3}px; height: {mpercent3}px;">{value3}</dd>
			</dl>
			<dl>
				<dt><a href="#4" title="{step3}-{step4}">{step3}-{step4}</a></dt>
				<dd style="border-bottom-width: {percent4}px; height: {mpercent4}px;">{value4}</dd>
			</dl>
			<dl>
				<dt><a href="#5" title="{step4}-{step5}">{step4}-{step5}</a></dt>
				<dd style="border-bottom-width: {percent5}px; height: {mpercent5}px;">{value5}</dd>
			</dl>
			<dl>
				<dt><a href="#6" title="{step5}-{step6}">{step5}-{step6}</a></dt>
				<dd style="border-bottom-width: {percent6}px; height: {mpercent6}px;">{value6}</dd>
			</dl>
			<dl>
				<dt><a href="#7" title="{step6}-{step7}">{step6}-{step7}</a></dt>
				<dd style="border-bottom-width: {percent7}px; height: {mpercent7}px;">{value7}</dd>
			</dl>
			<dl>
				<dt><a href="#8" title="{step7}-{step8}">{step7}-{step8}</a></dt>
				<dd style="border-bottom-width: {percent8}px; height: {mpercent8}px;">{value8}</dd>
			</dl>
			<dl>
				<dt><a href="#9" title="{step8}-{step9}">{step8}-{step9}</a></dt>
				<dd style="border-bottom-width: {percent9}px; height: {mpercent9}px;">{value9}</dd>
			</dl>
			<dl>
				<dt><a href="#9" title="{step9}-{max}">{step9}-{max}</a></dt>
				<dd style="border-bottom-width: {percent10}px; height: {mpercent10}px;">{value10}</dd>
			</dl>
			</div>""".format(min=min,max = max,nb = nb,
			step1 = step1, step2 = step2,
			step3 = step3, step4 = step4,step5 = step5,
			step6 = step6,step7 = step7,step8 = step8,step9 = step9,
			value1 = value1, value2 = value2,value3= value3,
			value4 = value4,value5 = value5,value6 = value6,
			value7 = value7,value8 = value8,value9 = value9,value10 = value10,
			percent1 = percent1, percent2 = percent2,percent3 = percent3,
			percent4 = percent4,
			percent5 = percent5, percent6 = percent6,percent7 = percent7,
			percent8 = percent8,
			percent9 = percent9, percent10 = percent10,
			mpercent1 = 200 - percent1, mpercent2 = 200 -percent2,mpercent3 = 200- percent3,
			mpercent4 = 200 -percent4,
			mpercent5 = 200 - percent5, mpercent6 = 200 -percent6,mpercent7 = 200- percent7,
			mpercent8 = 200 -percent8,
			mpercent9 = 200 - percent9, mpercent10 = 200 -percent10)
		

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
		<td>{vitesse_max:.2f}</td>
		<td>{vitesse_moy}</td>
		<td>{sens}</td>
		</tr>""".format(time=entry["time"],
						vitesse_max=entry["vitesse_max"],
						vitesse_moy=entry["vitesse_moy"],
						sens=entry["sens"])
		for entry in history)

		return """
		<td>
		<h2>Sensor {name}</h2>
		<table class="result">
		<tr>
		<th>Timestamp</th>
		<th>Vitesse max</th>
		<th>Vitesse moy</th>
		<th>Sens</th>
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
		#histogramme {{
			display: block;
			width: 500px;
			height: 200px;
			border: 1px solid #333;
			background-color: #eee;
			margin: 100px auto;
		}}
		dl {{
			margin: 0;
			padding: 0;
			border: none;
			position: relative;
			display: block;
			width: 50px;
			height: 200px;
			float: left;
		}}
		dt {{
			margin: 0;
			padding: 0;
			border: none;
			position: absolute;
			bottom: 0;
			float: left;
			display: block;
			width: 50px;
			height: 20px;
			text-align: center;
		}}

		dd {{
			margin: 0;
			padding: 0;
			border: none;
			position: absolute;
			top: 0;
			z-index: 1;
			float: left;
			display: block;
			width: 50px;
			text-align: center;
			border-bottom-style: solid;
			border-bottom-color: #333;
			border-bottom-width: 0px;
		}}
		a {{
			margin: 0;
			padding: 0;
			border: none;
			position: absolute;
			top: -100px;
			z-index: 10;
			display: block;
			width: 50px;
			padding-top: 125px;
			height: 30px;
			overflow: hidden;
			text-align: center;
		}}
		</style>
		<title>Tachymetre - {name}</title>
		</head>
		<body>
		<h1>Tachymetre - {name}</h1>
		""".format(name=self._name)

		if not self._apirest:
			output += "<p>Apirest service unavailable</p>"
		else:
			output += "<p>Aggregator found</p>"
			history = self._apirest.get_history()
			output += "\n<table class=\"main\"><tr>"
			output += '\n'.join((self._make_sensor_part("Tachymetre", history["Tachymetre"])
			for name in sorted(history)))
			output += "\n</tr></table>"
			output += self._make_histo()

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
