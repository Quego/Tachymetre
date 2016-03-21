from pelix.ipopo.decorators import ComponentFactory, Provides, Requires

@ComponentFactory("apirest-factory")
@Provides("ShowDonneesService")
@Requires("_aggregator", "ShowEtatService")
@Requires("_serveur", "ReadDonneesElaboreesService")
class Apirest(object):

	def __init__(self):
		self.aggregator = None
		self.serveur = None
		self.data = None

	def get_etat(self):
		etat = self.aggregator.send_etat()

	def get_donnees_elaborees(self):
		self.data = self.serveur.load_donnees_elaborees()

	def send_donnees_elaborees(self):
		return self.data
