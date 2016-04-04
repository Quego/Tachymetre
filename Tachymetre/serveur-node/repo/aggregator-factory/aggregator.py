from pelix.ipopo.decorators import ComponentFactory, Provides, Requires, Validate, Invalidate
import logging as log

@ComponentFactory("aggregator-factory")
@Provides("GetDonneesElaboreesAggregatorService")
@Provides("ShowEtatService")
@Requires("_sender", "GetPresenceService", optional=True)
@Requires("_serveur", "StoreDonneesElaboreesService")
class Aggregator(object):

	def __init__(self):
		self._sender = None
		self._serveur = None
		self.presence = None

	@Validate
	def start(self, context):
		self.presence = True

	@Invalidate
	def stop(self, context):
		log.info("Aggregator Invalide")
		self.presence = False

	def get_presence(self):
		return self.presence

	def get_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		log.info("Donnees aggregator : " + str(timestamp) + " / " + str(vitesse_max) + " / " + str(vitesse_moy) + " / " + str(sens))
		log.debug("Appel de : self.send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)")
		self.send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)

	def send_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		log.info("Donnees aggregator : " + str(timestamp) + " / " + str(vitesse_max) + " / " + str(vitesse_moy) + " / " + str(sens))
		log.debug("Appel de : self._serveur.store_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)")
		self._serveur.store_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
