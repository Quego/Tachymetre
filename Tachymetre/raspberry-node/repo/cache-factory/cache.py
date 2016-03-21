from pelix.ipopo.decorators import ComponentFactory, Provides, Requires

@ComponentFactory("cache-factory")
@Provides("SaveDonneesElaboreesService")
@Provides("PushDonneesElaboreesService")
class Cache(object):

	def get_priorite(self):
		return 50

	def save_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		# On rajoute les donnees a sauvegarder dans le cache
		f = open("cache.txt", "a")
		# Format : timestamp/vitesse_max/vitesse_moy/sens
		f.write(str(timestamp) + "/" + str(vitesse_max) + "/" + str(vitesse_moy) + "/" + str(sens) + "\n")
		f.close()

	def push_donnees_elaborees(self):
		# Lecture du cache
		f = open("cache.txt", "r")
		# Recuperation des donnees mise en cache
		donnees = f.read()
		f.close()
		# Reinitialisation du cache
		f = open("cache.txt", "w")
		f.write("")
		f.close()
		return donnees
