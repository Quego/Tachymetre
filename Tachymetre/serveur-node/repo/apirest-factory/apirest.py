#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --

from pelix.ipopo.decorators import ComponentFactory, Provides, Validate, Invalidate, Property, Requires, Bind, Unbind, BindField, UnbindField
from pelix.ipopo import constants

import logging
import threading
import time

_logger = logging.getLogger(__name__)

@ComponentFactory("apirest-factory")
@Property("_name", constants.IPOPO_INSTANCE_NAME)
@Property("_history_size", "history.size", 10)
@Property("_poll_delta", "poll.delta", 10)

@Requires("_aggregator", "ShowEtatService")
@Requires("_serveur", "ReadDonneesElaboreesService")

@Provides("DonneesService")


class Apirest(object):

	def __init__(self):
		self._aggregator = None
		self._serveur = None
		self.data = None

		self._history_size = 0
		self._name = ""
		self._poll_delta = 0
		self._sensors = []
		self._cpt = 0      

		# The values history (sensor -> list of dictionaries)
		self._history = {}

		self._lock = threading.Lock()
		self._thread_stop = threading.Event()
		self._thread = None

	def get_etat(self):
		with self._lock:
			etat = self._aggregator.send_etat()

	def get_donnees_elaborees(self):
		with self._lock:
			self.data = self._serveur.load_donnees_elaborees()

	def send_donnees_elaborees(self):
		with self._lock:
			return self.data


	def get_history(self):
		"""
		Retrieves the whole known history as a dictionary.

		Result is a dictionary, with sensor name as entry and a list
		of HistoryEntry (Python map/Java bean) as value

		:return: The whole history
		"""
		with self._lock:
			return self._history

	def get_sensor_history(self, sensor):
		"""
		Retrieves the known history for the given sensor

		:param sensor: The name of a sensor
		:return: The history of the sensor. Can be None
		"""
		with self._lock:
			return self._history.get(sensor, None)

	def get_sensor_lastentry(self, sensor):
		"""
		Retrieves the last known history entry for the given sensor

		:param sensor: The name of the sensor
		:return: The last history entry of the sensor. Can be None.
		"""
		with self._lock:
			sensor_history = self._history.setdefault(sensor, [])
			if sensor_history:
				return sensor_history[0]

	def _poll(self):
		"""
		Polls the value of all known sensors
		"""
		while not self._thread_stop.is_set():
		#	if self._sensors is not None:
			#	for sensor in self._sensors:
			try:
				data = self._serveur.load_donnees_elaborees(self._cpt)
				for row in data:
					self._store("Tachymetre", row[0], row[1], row[2], row[3])
					self._cpt += 1
			except Exception as ex:
				_logger.error("Error retrieving sensor data: %s", ex)

			# Wait for the poll delta, or for the order to stop
			try:
				wait = float(self._poll_delta)
			except:
				wait = 30

			self._thread_stop.wait(wait)

	def _store(self, sensor, timestamp, vitesse_max, vitesse_moy, sens):
		"""
		Stores a value in the history
		"""
		# Get the history list for this sensor
		with self._lock:
			sensor_history = self._history.setdefault(sensor, [])

			# Remove the oldest entry if needed
			if len(sensor_history) >= self._history_size:
				del sensor_history[-1]

			# Insert the new entry in front
			sensor_history.insert(0,   {"sensor": 		sensor,
										"time": 		timestamp,
										"vitesse_max": 	vitesse_max,
										"vitesse_moy": 	vitesse_moy,
										"sens": 		sens})

	def get_vitesse_max(self):
		return self._serveur.get_vitesse_max()

	def get_vitesse_min(self):
		return self._serveur.get_vitesse_min()

	def get_vitesse_entre_deux_dates(self, date1, date2):
		return self._serveur.get_vitesse_entre_deux_dates( date1, date2)

	def get_vitesse_entre_deux_bornes(self, min, max):
		return self._serveur.get_vitesse_entre_deux_bornes(min, max)

	@Bind
	def bind(self, svc, ref):
		"""
		Called by iPOPO when a service is bound
		"""
		props = ref.get_properties()
		if props.get("service.imported", False):
			import_str = "from %s" % props.get("service.imported.from")
		else:
			import_str = "local"
			# if service is SpeedSensor then informe listeners        
			_logger.debug("%s> Bound to %s (%s)", self._name, ref, import_str)

	@Unbind
	def unbind(self, svc, ref):
		"""
		Called by iPOPO when a service is gone
		"""
		props = ref.get_properties()
		if props.get("service.imported", False):
			import_str = "from %s" % props.get("service.imported.from")
		else:
			import_str = "local"
			_logger.debug("%s> UnBound of %s (%s)", self._name, ref, import_str)

	@Validate
	def validate(self, context):
		"""
		Component validation
		"""
		# Clear the stop event
		self._thread_stop.clear()

		# Start the polling thread
		self._thread = threading.Thread(target=self._poll)
		self._thread.start()
		_logger.info("Component %s validated", self._name)

	@Invalidate
	def invalidate(self, context):
		"""
		Component invalidation
		"""
		# Set the stop event
		self._thread_stop.set()

		# Wait a little for the thread
		self._thread.join(2)
		self._thread = None
		_logger.info("Component %s invalidated", self._name)
