{
    "name": "speed",
    "root": {
        "name": "speed-composition",
        "components": [
			{
				/**
				 * Aggregator component
				 */
				"name" : "Aggregator",
				"factory" : "aggregator-factory",
				"language" : "python",
				/*"isolate" : "aggregation",*/
				"node" : "gateway-node",
				"properties" : {
					"poll.delta" : 1
				}
			}, {
				/**
				 * Aggregator web UI
				 */
				"name" : "UserInterface",
				"factory" : "aggregator-ui-factory",
				"language" : "python",
				"isolate" : "web.interface",
				"node" : "gateway-node",
				"properties" : {
					"servlet.path" : "/PythonSensor"
				},
				"wires" : {
					"_aggregator" : "aggregator"
				}
			}, {
			/**
				 * Aggregator web UI
				 */
				"name" : "UserInterfaceList",
				"factory" : "aggregator-list-factory",
				"language" : "python",
				//"isolate" : "web.interface",
				"node" : "gateway-node",
				"properties" : {
					"servlet.path" : "/accueil"
				},
				"wires" : {
					"_aggregator" : "aggregator"
				}
			}, {	
				/**
				 * Python sensor
				 */
				"name" : "PythonSensor2",
				"factory" : "python-sensor-factory",
				/*"isolate" : "speed.python",*/
				"node" : "python-sensor-node",
				"properties" : {
					"temper.value.min" : -5,
					"temper.value.max" : 45
				}
			},{
				/**
				 * Python sensor
				 */
				"name" : "PythonSensor",
				"factory" : "python-sensor-factory",
				/*"isolate" : "speed.python",*/
				"node" : "python-sensor-node",
				"properties" : {
					"speed.value.min" : -5,
					"speed.value.max" : 45
				}

			}
        ]
    }
}
