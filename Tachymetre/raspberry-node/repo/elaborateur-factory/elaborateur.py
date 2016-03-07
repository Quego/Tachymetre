from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("elaborateur-factory.elaborateur")
@Provides("GetDonneesBrutesService")
@Requires("cache", "SaveDonneesElaboreesService")
@Requires("sender", "GetDonneesElaboreesService")
class Elaborateur(object):

	def __init__(self):
		self.cache = None
		self.sender = None

	def get_donnees_brutes(self, timestamp, frequence, tension):
		# TODO calculs
		# Calculs de la vitesse et du sens
		vitesse_max = frequence
		vitesse_moy = frequence
		sens = tension

		# Envoie des données élaborées
		self.send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)

	def send_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		# TODO
		# Détermination de l'envoie des données élaborées
		priorite_sender = self.sender.get_priorite()
		priorite_cache = self.cache.get_priorite()
		if priorite_sender > priorite_cache:
			acces_sender = True
		else:
			acces_sender = False

		# Envoie des données élaborées
		if acces_sender:
			# Le sender est disponible donc l'envoie est direct
			self.sender.get_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
		else:
			# Le sender n'est pas disponible donc on sauvegarde en cache
			self.cache.save_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
