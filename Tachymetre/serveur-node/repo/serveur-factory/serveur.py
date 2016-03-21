from pelix.ipopo.decorators import ComponentFactory, Provides, Requires
import sqlite3

@ComponentFactory("serveur-factory")
@Provides("StoreDonneesElaboreesService")
@Provides("LoadDonneesElaboreesService")
@Provides("ShowDonneesService")
class Serveur(object):

	def __init__(self):
		conn = sqlite3.connect('base.db')
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS mesures(
				timestamp 		TEXT PRIMARY KEY	NOT NULL,
				vitesse_max 	REAL				CHECK(vitesse_max > 0),
				vitesse_moy 	REAL				CHECK(vitesse_moy > 0),
				sens 			CHAR(1)
			)
		""")
		conn.commit()
		conn.close()

	def store_donnees_elaborees(self, timestamp, vitesse_max, vitesse_moy, sens):
		# Ecriture dans la base de donnees
		conn = sqlite3.connect('base.db')
		data = {"timestamp" : timestamp, "vitesse_max" : vitesse_max, "vitesse_moy" : vitesse_moy, "sens" : sens}
		cursor.execute("""
			INSERT INTO mesures(timestamp, vitesse_max, vitesse_moy, sens) VALUES(:timestamp, :vitesse_max, :vitesse_moy, :sens)
		""", data)
		conn.close()

	def load_donnees_elaborees(self):
		# Lecture de la base de donnees
		conn = sqlite3.connect('base.db')
		cursor.execute("""
			SELECT timestamp, vitesse_max, vitesse_moy, sens FROM mesures
		""")
		data = cursor.fetchone()
		conn.close()
		return data
