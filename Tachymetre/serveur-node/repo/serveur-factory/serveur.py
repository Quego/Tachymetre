from pelix.ipopo.decorators import ComponentFactory, Provides, Requires, Validate, Invalidate
import sqlite3
import logging as log

@ComponentFactory("serveur-factory")
@Provides("StoreDonneesElaboreesService")
@Provides("LoadDonneesElaboreesService")
@Provides("ReadDonneesElaboreesService")
class Serveur(object):

	def __init__(self):
		self.conn = None
		self.cursor = None

	@Validate
	def start(self, context):
		log.info("Creation de la table mesures")
		self.conn = sqlite3.connect('base.db', check_same_thread=False)
		self.cursor = self.conn.cursor()
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS mesures(
				id 				INTEGER PRIMARY KEY	AUTOINCREMENT UNIQUE,
				timestamp 		TEXT 				NOT NULL,
				vitesse_max 	REAL				CHECK(vitesse_max > 0),
				vitesse_moy 	REAL				CHECK(vitesse_moy > 0),
				sens 			CHAR(1)
			)
		""")
		self.conn.commit()

	@Invalidate
	def stop(self, context):
		log.info("Fermeture de la base")
		self.conn.close()

	def store_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		log.info("Store de : " + str(timestamp) + " / " + str(vitesse_max) + " / " + str(vitesse_moy) + " / " + str(sens))
		# Ecriture dans la base de donnees
		data = {"timestamp" : timestamp, "vitesse_max" : vitesse_max, "vitesse_moy" : vitesse_moy, "sens" : sens}
		self.cursor.execute("""
			INSERT INTO mesures(timestamp, vitesse_max, vitesse_moy, sens) VALUES(:timestamp, :vitesse_max, :vitesse_moy, :sens)
		""", data)
		self.conn.commit()

	def load_donnees_elaborees(self, taille):
		# Lecture de la base de donnees
		self.cursor.execute("""
			SELECT timestamp, vitesse_max, vitesse_moy, sens FROM mesures WHERE id > ?
		""", (taille,))
		data = self.cursor.fetchall()
		return data

	def get_vitesse_max(self):
		# Lecture de la base de donnees
		self.cursor.execute("""
			SELECT max(vitesse_moy)
			FROM mesures
		""")
		data = self.cursor.fetchall()
		return data

	def get_vitesse_min(self):
		# Lecture de la base de donnees
		self.cursor.execute("""
			SELECT min(vitesse_moy)
			FROM mesures
		""")
		data = self.cursor.fetchall()
		return data

	def get_vitesse_entre_deux_dates(self, date1, date2):
		# date1 et date2 au format : YYYY-MM-DD
		# Lecture de la base de donnees
		self.cursor.execute("""
			SELECT vitesse_moy
			FROM mesures
			WHERE date(substr(timestamp, 7, 4)
			|| '-'
			|| substr(timestamp, 4, 2)
			|| '-'
			|| substr(timestamp, 1, 2))
			BETWEEN date(?) AND date(?)
		""", (date1, date2,))
		data = self.cursor.fetchall()
		return data

	def get_vitesse_entre_deux_bornes(self, min, max):
		# Lecture de la base de donnees
		self.cursor.execute("""
			SELECT count(vitesse_moy)
			FROM mesures
			WHERE vitesse_moy >= (?) AND vitesse_moy <= (?)
		""", (min, max,))
		data = self.cursor.fetchall()
		return data
