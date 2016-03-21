from pelix.ipopo.decorators import ComponentFactory, Provides, Requires

@ComponentFactory("interfaceutilisateur-factory")
@Requires("_apirest", "ShowDonneesService")
class Interfaceutilisateur(object):

	def __init__(self):
		self.apirest = None

	# TODO l'ecriture d'une page HTML
	def get_donnees_elaborees(self):
		data = self.apirest.send_donnees_elaborees();
