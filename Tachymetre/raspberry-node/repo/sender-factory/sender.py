from pelix.ipopo.decorators import ComponentFactory, Provides, Requires

@ComponentFactory("sender-factory")
@Provides("GetDonneesElaboreesService")
@Provides("GetPresenceService")
@Requires("_aggregator", "GetDonneesElaboreesAggregatorService")
class Sender(object):

	def __init__(self):
		self.aggregator =  None
		self.presence = True

	def get_priorite(self):
		if self.presence:
			return 100
		else:
			return 0

	def get_presence(self):
		return self.presence

	def get_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		if self.aggregator is not None:
			self.presence = True
			self.send_donnees_elaborees
		else:
			self.presence = False

	def send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens):
		self.aggregator.get_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
