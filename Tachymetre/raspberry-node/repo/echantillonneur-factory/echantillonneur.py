from pelix.ipopo.decorators import ComponentFactory, Provides
import time, datetime

@ComponentFactory("echantilloneur-factory.echantillonneur")
@Requires("elaborateur", "GetDonneesBruteService")
class Echantillonneur(object):

	def __init__(self):
		self.elaborateur = None

	# TODO réception des données brutes à partir du capteur

	# Appel lors d'un passage d'une voiture
	def send_donnees_brutes(self, frequence, tension):
		# Envoie des données brutes
		t = time.time()
		ts = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
		self.elaborateur.get_donnees_brutes(timestamp, frequence, tension)
