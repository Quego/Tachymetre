from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("sync-factory.sync")
@Requires("cache", "PushDonneesElaboreesService")
@Requires("sender", "GetDonneesElaboreesService")
class Sync(object):

	def __init__(self):
		self.cache = None
		self.sender = None

	def get_donnees_elaborees(self):
		# On récupére la vitesse et le sens depuis le cache
		data = self.cache.push_donnees_elaborees()
		self.send_donnees_elaborees(data)

	def send_donnees_elaborees(self, data):
		# On vérifie bien que le sender est disponible
		priorite_cache = self.cache.get_priorite()
		priorite_sender = self.sender.get_priorite()

		# Si le sender est effectivement disponible
		if priorite_sender > priorite_cache:
			for one_data in data:
				self.sender.get_donnees_elaborees(one_data[0], one_data[1], one_data[2], one_data[3])
		else:
			# TODO écrire dans un log par exemple
		
