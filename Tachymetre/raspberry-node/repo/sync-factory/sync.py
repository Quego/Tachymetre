from pelix.ipopo.decorators import ComponentFactory, Provides, Requires

@ComponentFactory("sync-factory")
@Requires("_cache", "PushDonneesElaboreesService")
@Requires("_sender", "GetDonneesElaboreesService")
class Sync(object):

	def __init__(self):
		self.cache = None
		self.sender = None

	def get_donnees_elaborees(self):
		# On recupere l'ensemble du fichier cache dans data avec le format :
		# 'timestamp1/vitesse_max1/vitesse_moy1/sens1
		#  timestamp2/vitesse_max2/vitesse_moy2/sens2
		#  ...
		#  timestampN/vitesse_maxN/vitesse_moyN/sensN'
		data = self.cache.push_donnees_elaborees()
		# On envoie la data precedente mais splitee par les '\n' :
		# ['timestamp1/vitesse_max1/vitesse_moy1/sens1'],
		# ['timestamp2/vitesse_max2/vitesse_moy2/sens2'],
		#   ...
		# ['timestampN/vitesse_maxN/vitesse_moyN/sensN']
		data_split = data.split('\n')
		# Envoie des donnees.
		self.send_donnees_elaborees(data_split)

	def send_donnees_elaborees(self, data):
		# On verifie bien que le sender est disponible.
		priorite_cache = self.cache.get_priorite()
		priorite_sender = self.sender.get_priorite()

		# Si le sender est effectivement disponible.
		if priorite_sender > priorite_cache:
			# one_data correspond a :
			# 'timestampX/vitesse_maxX/vitesse_moyX/sensX'
			for one_data in data:
				# On split one_data par les '/' pour recuperer chaque valeur
				# et pouvoir les envoyer correctement.
				one_data_split = one_data.split('/')
				self.sender.get_donnees_elaborees(one_data_split[0], one_data_split[1], one_data_split[2], one_data_split[3])
		# Si le sender n'est pas disponible, on essaiera au prochain envoie des donnees
		# depuis le cache
		else:
			pass
		
