from pelix.ipopo.decorators import ComponentFactory, Provides, Requires
import time, datetime
import serial

@ComponentFactory("echantillonneur-factory")
@Requires("_elaborateur", "GetDonneesBrutesService")
class Echantillonneur(object):

	def __init__(self):
		self.elaborateur = None
		# On prepare la connexion avec la liaison serie de l'Arduino.
		self.ser = serial.Serial('/dev/ttyACM0', 9600)
		# Indicateur de coherence entre Raspberry et Arduino.
		coherence = False
		v1 = 0
		v2 = 0
		# Reglage de la synchronisation Raspberry - Arduino.
		while not coherence:
			try:
				# Lecture de deux valeurs : -1 (frequence), -2 (tension)
				# - soit -1 et -2 donc la coherence est verifiee
				# - soit -2 et -1 dans ce cas on skyp une valeur pour
				# se mettre dans un etat coherent
				# - soit des valeurs autres que -1 et -2 dues au reset
				# de la carte Arduino, dans ce cas la on recommence la
				# boucle et on relit deux nouvelles valeurs
				# L'Arduino ne cessera d'envoyer des -1 et -2 tant que
				# la coherence n'est pas verifiee.
				v1 = ser.readline()
				v2 = ser.readline()
				# L'ordre de reception est verifie.
				if float(v1) == -1 and float(v2) == -2:
					coherence = True
					# On signal a l'Arduino que la coherence est verifiee
					# donc que la synchronisation est faite.
					# 
					ser.write(bytes("T", "UTF-8"))
				# L'ordre de reception est mauvais.
				else:
					# On skip une valeur.
					ser.readline()
			except:
				# Suite a des valeurs autres que -1 et -2 on recommence
				# la verification de la coherence.
				pass
		# La coherence est maintenant verifiee, l'Arduino envoie :
		# - la frequence
		# - puis la tension
		while True:
			# L'Arduino envoie d'abord la frequence puis la tension.
			f = float(ser.readline())
			t = float(ser.readline())
			# Envoie des donnees pour elaboration d'une vitesse et d'un sens.
			send_donnees_brutes(float(f), float(t))
			
	# Appel lors d'un passage d'une voiture.
	def send_donnees_brutes(self, frequence, tension):
		# Envoie des donnees brutes.
		t = time.time()
		# Ajout du timestamp.
		ts = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
		self.elaborateur.get_donnees_brutes(timestamp, frequence, tension)
