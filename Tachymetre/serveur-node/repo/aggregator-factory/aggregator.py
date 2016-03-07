from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("aggregator-factory.aggregator")
@Provides("GetDonneesElaboreesService")
@Provides("ShowEtatService")
@Requires("sender", "GetPresenceService")
@Requires("serveur", "StoreDonneesElaboreesService")
class Aggregator(object):

	def __init__(self):
		self.sender = None
		self.serveur = None
		self.presence = True

	def send_presence(self):
		return self.presence

	# TODO à améliorer
	def send_etat(self):
		return self.presence

	def get_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		self.send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)

	def send_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens)
		self.serveur.store_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
