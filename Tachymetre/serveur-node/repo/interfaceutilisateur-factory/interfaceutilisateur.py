from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("interfaceutilisateur-factory.interfaceutilisateur")
@Requires("apirest", "ShowDonneesService")
class Interfaceutilisateur(object):

	def __init__(self):
		self.apirest = None

	# TODO l'écriture d'une page HTML
	def get_donnees_elaborees(self):
		data = self.apirest.send_donnees_elaborees();
