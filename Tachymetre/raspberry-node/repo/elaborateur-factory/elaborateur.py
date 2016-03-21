from pelix.ipopo.decorators import ComponentFactory, Provides, Requires
from math import radians, cos

@ComponentFactory("elaborateur-factory")
@Provides("GetDonneesBrutesService")
@Requires("_cache", "SaveDonneesElaboreesService")
@Requires("_sender", "GetDonneesElaboreesService")
class Elaborateur(object):

	def __init__(self):
		self.cache = None
		self.sender = None
		self.timestamp = None
		self.vitesse = 0
		self.vitesse_moy = 0
		self.vitesse_max = -1
		self.tension = []
		self.angle = radians(15)

	def get_donnees_brutes(self, timestamp, frequence, tension):
		# Debut du passage
		if frequence != 0:
			# Recuperation du timestamp du debut du passage
			if self.timestamp is None:
				self.timestamp = timestamp
			# Calcul de la vitesse avec la frequence
			self.vitesse = abs(frequence / (2 * 10525000000 * cos(angle) / 300000000))
			# Stockage de la vitesse maximum
			if self.vitesse > self.vitesse_max:
				self.vitesse_max = self.vitesse
			# Ajout de la vitesse dans le calcul de la vitesse moyenne
			self.vitesse_moy += self.vitesse
			# Ajout de la valeur de tension dans le tableau de tension
			self.tension.append(tension)
		# Fin du passage
		elif self.timestamp is not None:
			if len(self.tension) > 3:
				# Fin du calcul de la vitesse moyenne
				self.vitesse_moy = self.vitesse_moy / len(self.tension)
				# Calcul du sens de circulation
				if self.tension[0] > self.tension[-1]:
					sens = "A"
				else:
					sens = "R"
				# Envoi des donnees
				self.send_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
			# Remise a zero des variables
			self.timestamp = None
			self.vitesse = 0
			self.vitesse_moy = 0
			self.vitesse_max = -1
			self.tension = []
		# Frequence a 0 et rien dans les variables : On ne fait rien
		else:
			pass

	def send_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		# TODO
		# Determination de l'envoie des donnees elaborees
		priorite_sender = self.sender.get_priorite()
		priorite_cache = self.cache.get_priorite()
		if priorite_sender > priorite_cache:
			acces_sender = True
		else:
			acces_sender = False

		# Envoie des donnees elaborees
		if acces_sender:
			# Le sender est disponible donc l'envoie est direct
			self.sender.get_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
		else:
			# Le sender n'est pas disponible donc on sauvegarde en cache
			self.cache.save_donnees_elaborees(timestamp, vitesse_max, vitesse_moy, sens)
