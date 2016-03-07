from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("cache-factory.cache")
@Provides("SaveDonneesElaboreesService")
@Provides("PushDonneesElaboreesService")
class Cache(object):

	def get_priorite(self):
		return 50

	def save_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		# TODO sauvegarde dans un fichier
		# OU
		# TODO sauvegarde en mémoire dans une liste
		return "TODO"

	# TODO liaison avec le sync
	def push_donnees_elaborees(self):
		# TODO lecture du fichier de sauvegarde
		# OU
		# TODO envoie direct de la liste en mémoire
		return "TODO"
