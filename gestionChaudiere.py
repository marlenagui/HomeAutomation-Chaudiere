import odroid_wiringpi as wpi
from w1thermsensor import W1ThermSensor
import datetime
import time
import threading
from urllib import request, parse
from configParser import read_config
from log import *
from w1thermsensor import W1ThermSensor
#from nap.url import Url

################################################################################################################################
# Global variables
################################################################################################################################

class glob(object):
	"""global variables definition"""
	verbose = True
	# define the config.ini file to use.
	configFile = 'config.ini'
	#define the sections of the config file
	mainConfig = {}
	arestioConfig = {}
	horairesConfig = {}
	logDBConfig = {}
	consignesConfig = {}
	digitalIOConfig = {}
	analogIOConfig = {}
	smsConfig = {}

	#define the arest.io variables
	#urlApi = ''

	# define the wpi port
	relaisCirculateur = 2
	relaisCirculateurIsOn = False  
	relaisChaudiere = 3 
	relaisChaudiereIsON = False
	analogChaudiere = 1

	# https://wiki.odroid.com/odroid-c1/application_note/gpio/wiringpi
	# +-----+-----+---------+------+---+--- C1 ---+---+------+---------+-----+-----+
	# | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
	# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
	# |     |     |    3.3V |      |   |  1 || 2  |   |      | 5V      |     |     |
	# | 493 |   8 |   SDA.2 | ALT1 | 1 |  3 || 4  |   |      | 5V      |     |     |
	# | 494 |   9 |   SCL.2 | ALT1 | 1 |  5 || 6  |   |      | 0V      |     |     |
	# | 473 |   7 |  IO.473 | ALT1 | 0 |  7 || 8  | 1 | ALT1 | TxD1    | 15  | 488 |
	# |     |     |      0V |      |   |  9 || 10 | 1 | ALT1 | RxD1    | 16  | 489 |
	# | 479 |   0 |  IO.479 |   IN | 1 | 11 || 12 | 1 | IN   | IO.492  | 1   | 492 |
	# | 480 |   2 |  IO.480 |   IN | 1 | 13 || 14 |   |      | 0V      |     |     |
	# | 483 |   3 |  IO.483 | ALT2 | 1 | 15 || 16 | 1 | IN   | IO.476  | 4   | 476 |
	# |     |     |    3.3V |      |   | 17 || 18 | 1 | IN   | IO.477  | 5   | 477 |
	# | 484 |  12 |    MOSI |   IN | 1 | 19 || 20 |   |      | 0V      |     |     |
	# | 485 |  13 |    MISO |   IN | 1 | 21 || 22 | 1 | IN   | IO.478  | 6   | 478 |
	# | 487 |  14 |    SCLK |   IN | 1 | 23 || 24 | 1 | IN   | CE0     | 10  | 486 |
	# |     |     |      0V |      |   | 25 || 26 | 0 | IN   | IO.464  | 11  | 464 |
	# | 474 |  30 |   SDA.3 | ALT2 | 1 | 27 || 28 | 1 | ALT2 | SCL.3   | 31  | 475 |
	# | 490 |  21 |  IO.490 | ALT1 | 1 | 29 || 30 |   |      | 0V      |     |     |
	# | 491 |  22 |  IO.491 | ALT1 | 1 | 31 || 32 | 0 | IN   | IO.472  | 26  | 472 |
	# | 481 |  23 |  IO.481 |   IN | 1 | 33 || 34 |   |      | 0V      |     |     |
	# | 482 |  24 |  IO.482 | ALT2 | 1 | 35 || 36 | 0 | IN   | IO.495  | 27  | 495 |
	# |     |  25 |   AIN.3 |      |   | 37 || 38 |   |      | 1V8     | 28  |     |
	# |     |     |      0V |      |   | 39 || 40 |   |      | AIN.2   | 29  |     |
	# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
	# | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
	# +-----+-----+---------+------+---+--- N2 ---+---+------+---------+-----+-----+
	

	# define the sensors variables
	tempDepartEau = 0
	tempDepartEauViessman = 0
	tempChaudiereViessman = 0
	tempChaufferie = 0
	humiditeChaufferie = 0
	tempextviessmann = 0

	# define the time variables
	heureDebut = 0
	heureFin = 0
	heureMaintenant = 0

################################################################################################################################
# CLASS myThreadReasSensors
################################################################################################################################
class myThreadReadSensors(threading.Thread):
	"""Class to read all the sensors.
	   start function is a while loop contolled by self.running set to true in the init and set to false in the stop
	   Stop function is called in start when something wrong happens
	   Each iteration of the loop is managed at the end by a sleep, time.sleep is controled in the config file main section"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		self.verbose = True
		#self.verbose = glob.verbose
		self.severity = "INFO"

	def run(self):
		logtext = 'Thread ' +  self.name + 'read sensor started'
		log(self.name, self.verbose, self.severity, logtext)

		# self.running is class variable set to True during init, the while will loop until
		# the stop function of the class is called with parameters itself, so self.running can be updated and the loop will stop.
		while self.running:

			log(self.name, self.verbose, self.severity, "Reading sensors")
			# read temp_chaudiere_viessman
			#log(self.name, self.verbose, self.severity, glob.analogIOConfig)
			# urlPath = 'analog/' +  glob.analogIOConfig['temp_chaudiere_viessman']
			# sensor = arestio(glob.urlApi, urlPath)
			sensor = readAnalog(glob.analogChaudiere)
			if sensor == False:
				log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read temp_chaudiere_viessman")
				myThreadReadSensors.stop(self)
			glob.tempChaudiereViessman = sensor
			##insertIOTDataSqlite3(5, int(time.time()), str(glob.tempChaudiereViessman))
			insertIOTDataMysql(5, int(time.time()), str(glob.tempChaudiereViessman))
			#insertIOTDataMysql(glob.logDBConfig, 5, int(time.time()), str(glob.tempChaudiereViessman))
			# Read temp_depart_eau_viessman_1W
			#urlPath = 'analog/' +  glob.analogIOConfig['temp_depart_eau_viessman']
			sensor = read1Wire()
			if sensor == False:
				log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read temp_depart_eau_viessman")
				myThreadReadSensors.stop(self)
			glob.tempDepartEauViessman = sensor
			##insertIOTDataSqlite3(3, int(time.time()), str(glob.tempDepartEauViessman))
			insertIOTDataMysql(3, int(time.time()), str(glob.tempDepartEauViessman))
			#insertIOTDataMysql(glob.logDBConfig, 3, int(time.time()), str(glob.tempDepartEauViessman))
			# Read temp_depart_eau_10kresistor
			# sensor = arestio(glob.urlApi, glob.analogIOConfig['temp_depart_eau_10kresistor'])
			# if sensor == False:
			# 	log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read temp_depart_eau_10kresistor")
			# 	myThreadReadSensors.stop(self)
			# glob.tempDepartEau = sensor['temperatureEXT']
			# # Read temp_dth11
			# sensor =  arestio(glob.urlApi, glob.analogIOConfig['temp_dth11'] )
			# if sensor == False:
			# 	log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read temp_dth11")
			# 	myThreadReadSensors.stop(self)
			# glob.tempChaufferie = sensor['temperature']
			# # Read humidite_dht11
			# sensor = arestio(glob.urlApi, glob.analogIOConfig['humidite_dht11'])
			# if sensor == False:
			# 	log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read humidite_dht11")
			# 	myThreadReadSensors.stop(self)
			# glob.humiditeChaufferie = sensor['humidity']
			# # Read temp_ext_viessmann
			# #set manually right now no external temperature sensor connected
			# glob.tempextviessmann = int(glob.analogIOConfig['temp_ext_viessmann'])
			# #urlPath = 'analog/' +  glob.analogIOConfig['temp_ext_viessmann']
			# #glob.tempextviessmann = arestio(glob.urlApi, urlPath )
			# if glob.tempextviessmann == False:
			# 	log(self.name, self.verbose, self.severity, ":: ERROR :: Cannot read temp_ext_viessmann")
			# 	myThreadReadSensors.stop(self)
			# # Wait until next reading
			time.sleep(int(glob.consignesConfig['sleep_between_sensor_reading']))

			#log the values
			#logtext = 'tempChaudiereViessman = ' + str(glob.tempChaudiereViessman) + ', tempDepartEauViessman = ' + str(glob.tempDepartEauViessman) \
			#+ ', tempDepartEau = ' + str(glob.tempDepartEau) + ', tempChaufferie = ' + str(glob.tempChaufferie) + ', humiditeChaufferie = ' + str(glob.humiditeChaufferie) \
			#+ ', tempextviessmann = ' + str(glob.tempextviessmann)
			logtext = 'tempChaudiereViessman = ' + str(glob.tempChaudiereViessman) + ', tempDepartEauViessman = ' + str(glob.tempDepartEauViessman)
			log(self.name, self.verbose, self.severity, logtext)
		logtext = 'Thread ' +  self.name + 'read sensor stopped'
		log(self.name, self.verbose, self.severity, logtext)

	def stop(self):
		logtext = 'Thread ' +  self.name + 'read sensor is being stopped'
		log(self.name, self.verbose, self.severity, logtext)
		self.running = False


################################################################################################################################
# CLASS myThreadChaudiere
################################################################################################################################
class myThreadChaudiere(threading.Thread):
	"""Class thread to manage the heating boiler
	   start function is a while loop contolled by self.running set to true in the init and set to false in the stop
	   Stop function is called in start when something wrong happen"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		self.verbose = True
		#self.verbose = glob.verbose
		self.severity = "INFO"
		self.debug = False

	def run(self):
		logtext = 'Thread ' +  self.name + ' started'
		log(self.name, self.verbose, self.severity, logtext)
		while self.running:
			# Verifie si la temp ext est > a la consigne basse
			while glob.tempextviessmann > int(glob.consignesConfig['temp_exterieur_basse']):
				logtext = "il fait chaud dehors on attend :) " + glob.consignesConfig['sleep_temp_ext'] + " seconds"
				log(self.name, self.verbose, self.severity, logtext)
				time.sleep(glob.consignesConfig['sleep_temp_ext'])

			log(self.name, self.verbose, self.severity, "il caille dehors faut chauffer :( ")
			# verifie si la temp chaudiere est > a la consigne basse temperature chaudiere, si oui on attend
			while glob.tempChaudiereViessman > int(glob.consignesConfig['temp_chaudiere_basse']):
				logtext = "La chaudiere est chaude : " + str(glob.tempChaudiereViessman) + ", on attend :) " + glob.consignesConfig['sleep_chaudiere'] + " seconds"
				log(self.name, self.verbose, self.severity, logtext)
				time.sleep(int(glob.consignesConfig['sleep_chaudiere']))

			# Il fait froid et la chaudiere est froide on demarre :(
			log(self.name, self.verbose, self.severity, "-- DEMARRAGE -- chaudiere :( ")
			##insertIOTDataSqlite3(1, int(time.time()), 1)
			insertIOTDataMysql(1, int(time.time()), 1)
			#insertIOTDataMysql(glob.logDBConfig, 1, int(time.time()), 1)
			# ancienne version avec arest.io
			# urlPath = 'digital/' + glob.digitalIOConfig['relais_chaudiere'][1] + '/0'
			# demarrageChaudiere = arestio(glob.urlApi, urlPath)
			demarrageChaudiere = commandeRelais(glob.relaisChaudiere, 0)
			if demarrageChaudiere == False:
				log(self.name, self.verbose, self.severity, ":: ERROR :: Impossible de demarrer la chaudiere")
				myThreadChaudiere.stop(self)
			# Envoie SMS si debug = True
			if self.debug == True:
				 sendSMS(glob.smsConfig['url'], glob.smsConfig['user'], glob.smsConfig['pass'], "--DEMARRAGE_Chaudiere")
			# Verifie si la temp chaudiere est < a la consigne  haute temp chaudiere.
			while glob.tempChaudiereViessman < int(glob.consignesConfig['temp_chaudiere_haute']):
				logtext = "Temperature chaudiere : " + str(glob.tempChaudiereViessman) + " < a la temperature de consigne haute : " + str(glob.consignesConfig['temp_chaudiere_haute']) + ", on attend :( " + glob.consignesConfig['sleep_chaudiere'] + " seconds"
				log(self.name, self.verbose, self.severity, logtext)
				time.sleep(int(glob.consignesConfig['sleep_chaudiere']))

			# La chaudiere a atteind la consigne on l'arrete
			logtext = "Temperature chaudiere : " + str(glob.tempChaudiereViessman) + " > a la temperature de consigne haute : " + str(glob.consignesConfig['temp_chaudiere_haute'])
			log(self.name, self.verbose, self.severity, logtext)
			log(self.name, self.verbose, self.severity, "-- ARRET -- chaudiere :) ")
			##insertIOTDataSqlite3(1, int(time.time()), 0)
			insertIOTDataMysql(1, int(time.time()), 0)
			#insertIOTDataMysql(glob.logDBConfig, 1, int(time.time()), 0)
			# ancienne version avec arest.io
			# urlPath = 'digital/' + glob.digitalIOConfig['relais_chaudiere'][1] + '/1'
			# arretChaudiere = arestio(glob.urlApi, urlPath)
			arretChaudiere = commandeRelais(glob.relaisChaudiere, 1)
			if arretChaudiere == False:
				log(self.name, self.verbose, self.severity, ":: ERROR :: Impossible d arreter la chaudiere")
				myThreadChaudiere.stop(self)
				sendSMS(glob.smsConfig['url'], glob.smsConfig['user'], glob.smsConfig['pass'], "-- IMPOSSIBLE ARRET_Chaudiere")

	def stop(self):
		logtext = 'Thread ' +  self.name + ' is being stopped'
		log(self.name, self.verbose, self.severity, logtext)
		self.running = False
		#We stop the heating boiler in any case to be safe
		log(self.name, self.verbose, self.severity, "On arrete la chaudiere :) ")
		urlPath = 'digital/' + glob.digitalIOConfig['relais_chaudiere'][1] + '/1'
		arretChaudiere = commandeRelais(glob.relaisChaudiere, 1)
		if arretChaudiere == False:
			log(self.name, self.verbose, self.severity, ":: ERROR :: Impossible d arreter la chaudiere")
			myThreadChaudiere.stop(self)
			sendSMS(glob.smsConfig['url'], glob.smsConfig['user'], glob.smsConfig['pass'], "-- IMPOSSIBLE ARRET_Chaudiere")

################################################################################################################################
# CLASS myThreadCirculateur
################################################################################################################################
class myThreadCirculateur(threading.Thread):
	"""Thread pour la gestion du circulateur"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		#self.verbose = True
		self.verbose = glob.verbose
		self.severity = "INFO"

	def run(self):
		logtext = 'Thread ' +  self.name + ' started'
		log(self.name, self.verbose, self.severity, logtext)
		while self.running:
			# # Verifie si la temp ext est > a la consigne basse
			# while glob.tempextviessmann > int(glob.consignesConfig['temp_exterieur_basse']):
			# 	logtext = "il fait chaud dehors on attend :) " + glob.consignesConfig['sleep_temp_ext'] + " seconds"
			# 	log(self.name, self.verbose, self.severity, logtext)
			# 	time.sleep(int(glob.consignesConfig['sleep_temp_ext']))
			# log(self.name, self.verbose, self.severity, "il caille dehors faut chauffer :( ")

			# # Verifie si la temperature eau < temp consigne basse circulateur, si c'est le cas on attend que l'eau chauffe avant de la faire circuler
			# while glob.tempChaudiereViessman < int(glob.consignesConfig['temp_chaudiere_basse_circulateur']):
			# 	logtext = "La temperature chaudiere est basse :( " + str(glob.tempChaudiereViessman) + ", on attent : " +glob.consignesConfig['sleep_temp_ext'] + " seconds"
			# 	log(self.name, self.verbose, self.severity, logtext)
			# 	time.sleep(int(glob.consignesConfig['sleep_temp_ext']))

			# On demarre le circulateur
			# #insertIOTDataSqlite3(2, int(time.time()), 1)
			insertIOTDataMysql(2, int(time.time()), 1)
			#insertIOTDataMysql(glob.logDBConfig, 2, int(time.time()), 1)
			#urlPath = 'digital/' + glob.digitalIOConfig['relais_circulateur'][1] + '/0'
			if glob.relaisCirculateurIsOn: 
				log(self.name,self.verbose, self.severity, "Le circulateur est deja demarrer")
			else:
				log(self.name, self.verbose, self.severity, "Demarrage du circulateur")
				demarrageCirculateur = commandeRelais(glob.relaisCirculateur, 0)
				if demarrageCirculateur == False:
					log(self.name, self.verbose, self.severity, "Impossible de demarrer le circulateur")
					myThreadCirculateur.stop(self)
				else: 
					glob.relaisCirculateurIsOn = True
			time.sleep(3600)
			# # Verifie si la temp chaudiere est > a la consigne basse pour le circulateur, si c'est le cas on attend et l'eau chaude continue de circuler
			# while glob.tempChaudiereViessman > int(glob.consignesConfig['temp_chaudiere_basse_circulateur']):
			# 	logtext = "La temperature chaudiere est chaude :) " + str(glob.tempChaudiereViessman) + ", on attent : " +glob.consignesConfig['sleep_temp_ext'] + " seconds"
			# 	log(self.name, self.verbose, self.severity, logtext)
			# 	time.sleep(int(glob.consignesConfig['sleep_temp_ext']))

			# # On arrete le circulateur
			# log(self.name, self.verbose, self.severity, "Arret du circulateur")
			# #insertIOTDataSqlite3(2, int(time.time()), 0)
			# insertIOTDataMysql(2, int(time.time()), 0)
			# #insertIOTDataMysql(glob.logDBConfig, 2, int(time.time()), 0)
			# urlPath = 'digital/' + glob.digitalIOConfig['relais_circulateur'][1] + '/1'
			# arretCirculateur = arestio(glob.urlApi, urlPath)
			# if arretCirculateur == False:
			# 	log("ERROR", self.verbose, "Impossible d'arreter le circulateur")
			# 	myThreadCirculateur.stop(self)


	def stop(self):
		logtext = 'Thread ' +  self.name + ' is being stopped'
		log(self.name, self.verbose, self.severity, logtext)
		demarrageCirculateur = commandeRelais(glob.relaisCirculateur, 1)
		self.running = False

################################################################################################################################
# CLASS myThreadGestionVanne
################################################################################################################################
# class myThreadVanne(threading.Thread):
# 	"""Thread pour la gestion de la vanne"""
# 	def __init__(self, name):
# 		threading.Thread.__init__(self)
# 		self.name = name
# 		self.running = True
# 		self.verbose = glob.verbose
# 		self.severity = "INFO"

# 	def run(self):
# 		logtext = 'Thread ' +  self.name + ' started'
# 		log(self.name, self.verbose, self.severity, logtext)
# 		while self.running:
# 			# on verifie si le ciculateur fonctionne
# 			while myThreadCirculateur.is_alive(self):
# 				# on mesure la temperature de sortie eau
# 				urlPath = 'analog/' + glob.analogIOConfig['temp_depart_eau_viessman']
# 				glob.tempDepartEauViessman = arestio(glob.urlApi, urlPath)['return_value']
# 				#while int(glob.tempDepartEauViessman) > int(glob.consignesConfig['temp_depart_eau_bas'] and int(glob.tempDepartEauViessman) > int(glob.consignesConfig['temp_depart_eau_haut']:
# 				#	log(self.name, self.verbose, self.severity, "la vanne est bien reglee, on attent 20 secondes")

# 				# tant que la temperature sortie eau est superieure a la consigne on tourne vers le froid et on attend
# 				while int(glob.tempDepartEauViessman) > int(glob.consignesConfig['temp_depart_eau_haut']):
# 					logtext = "Temperature depart eau : " + str(glob.tempDepartEauViessman) + " superieur a la consigne : " + glob.consignesConfig['temp_depart_eau_haut']
# 					log(self.name, self.verbose, self.severity, logtext)
# 					# On verifie le sens de rotation de la vanne, on veut FROID
# 					logtext = "On tourne la vanne vers le froid pendant : " + glob.consignesConfig['duree_rotation_vanne']
# 					log(self.name, self.verbose, self.severity, logtext)
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne_chaudfroid'][1]
# 					relais_vanne_chaudfroid = arestio(glob.urlApi, urlPath)['return_value']
# 					if relais_vanne_chaudfroid != 1:
# 						# On position the sens de rotation de la vanne sur FROID
# 						urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne_chaudfroid'][1] + "/1"
# 						relais_vanne_chaudfroid = arestio(glob.urlApi, urlPath)
# 						if relais_vanne_chaudfroid == False:
# 							log("ERROR", self.verbose, "Impossible de changer le sens de rotation de la vanne")
# 							myThreadGestionVanne.stop()
# 					# On alimente le moteur de la vanne
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne'][1] + "/0"
# 					relaisVanne = arestio(glob.urlApi, urlPath)
# 					if relaisVanne == False:
# 						log("ERROR", self.verbose, "Impossible de demarrer le relais de vanne")
# 						myThreadGestionVanne.stop()
# 					# On attent de la duree de consigne de rotation de la vanne
# 					time.sleep(int(glob.consignesConfig['duree_rotation_vanne']))
# 					# On arrete le moteur de la vanne
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne'][1] + "/1"
# 					relaisVanne = arestio(glob.urlApi, urlPath)
# 					if relaisVanne == False:
# 						log("ERROR", self.verbose, "Impossible d'arreter le relais de vanne")
# 						myThreadGestionVanne.stop()
# 					else:
# 						log(self.name, self.verbose, self.severity, "Vanne tournee")
# 					# on mesure la temperature apres 60 secondes
# 					log(self.name, self.verbose, self.severity, "on attend 60 secondes avant de mesurer la temperature de depart eau")
# 					time.sleep(60)
# 					urlPath = 'analog/' + glob.analogIOConfig['temp_depart_eau_viessman']
# 					glob.tempDepartEauViessman = arestio(glob.urlApi, urlPath)['return_value']

# 				# cas ou la temp depart eau est inferieur a la consigne	basse on tourne la vanne vers le CHAUD
# 				while int(glob.tempDepartEauViessman) < int(glob.consignesConfig['temp_depart_eau_bas']):
# 					logtext = "Temperature depart eau : " + str(glob.tempDepartEauViessman) + " inferieur a la consigne : " + glob.consignesConfig['temp_depart_eau_haut']
# 					log(self.name, self.verbose, self.severity, logtext)
# 					logtext = "On tourne la vanne vers le chaud pendant : " + glob.consignesConfig['duree_rotation_vanne']
# 					log(self.name, self.verbose, self.severity, logtext)
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne_chaudfroid'][1]
# 					relais_vanne_chaudfroid = arestio(glob.urlApi, urlPath)['return_value']
# 					if relais_vanne_chaudfroid != 0:
# 						# On position the sens de rotation de la vanne sur CHAUD
# 						urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne_chaudfroid'][1] + "/0"
# 						relais_vanne_chaudfroid = arestio(glob.urlApi, urlPath)
# 						if relais_vanne_chaudfroid == False:
# 							log("ERROR", self.verbose, "Impossible de changer le sens de rotation de la vanne")
# 							myThreadGestionVanne.stop()
# 					# On alimente le moteur de la vanne
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne'][1] + "/0"
# 					relaisVanne = arestio(glob.urlApi, urlPath)
# 					if relaisVanne == False:
# 						log("ERROR", self.verbose, "Impossible de demarrer le relais de vanne")
# 						myThreadGestionVanne.stop()
# 					# On attent de la duree de consigne de rotation de la vanne
# 					time.sleep(int(glob.consignesConfig['duree_rotation_vanne']))
# 					# On arrete le moteur de la vanne
# 					urlPath = 'digital/' + glob.digitalIOConfig['relais_vanne'][1] + "/1"
# 					relaisVanne = arestio(glob.urlApi, urlPath)
# 					if relaisVanne == False:
# 						log("ERROR", self.verbose, "Impossible d'arreter le relais de vanne")
# 						myThreadGestionVanne.stop()
# 					else:
# 						log(self.name, self.verbose, self.severity, "Vanne tournee")
# 					# on mesure la temperature apres 60 secondes
# 					log(self.name, self.verbose, self.severity, "on attend 60 secondes avant de mesurer la temperature de depart eau")
# 					time.sleep(60)
# 					urlPath = 'analog/' + glob.analogIOConfig['temp_depart_eau_viessman']
# 					glob.tempDepartEauViessman = arestio(glob.urlApi, urlPath)['return_value']
# 					print(glob.tempDepartEauViessman)

# 				# et finallement la temperature est bonne on attend.
# 				logtext = "Temperature depart eau : " + str(glob.tempDepartEauViessman) + " est entre les consignes haute et basse :)"
# 				log(self.name, self.verbose, self.severity, logtext)
# 				log(self.name, self.verbose, self.severity, "on attend 60 secondes avant de mesurer la temperature de depart eau")
# 				time.sleep(60)

# 	def stop(self):
# 		logtext = 'Thread ' +  self.name + ' is being stopped'
# 		log(self.name, self.verbose, self.severity, logtext)
# 		self.running = False



################################################################################################################################
# CLASS myThreadConsignes
################################################################################################################################
class myThreadConsignes(threading.Thread):
	"""Thread to read the consigne every 10min, so any changes done to config file will be used"""
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		self.verbose = glob.verbose
		self.severity = "INFO"

	def run(self):
		logtext = 'Thread ' +  self.name + ' started'
		log(self.name, self.verbose, self.severity, logtext)
		while self.running:
			# -----------------------------------------------------------------------------------------------------------------
			#First check how often we need to read the consignes.
			if glob.mainConfig['debug_config_file'] == "on":
				#Read consignes every 10s
				time.sleep(int(glob.mainConfig['debug_config_file_sleep_on']))
			else:
				# read consignes every 10min
				time.sleep(int(glob.mainConfig['debug_config_file_sleep_off']))
			log(self.name, self.verbose, self.severity, "Relecture des consignes")
			readConfigFile()
			# consignes
			#glob.consignesConfig = read_config(glob.configFile, 'consignes')
			#logtext = "consignesConfig = " + str(glob.consignesConfig)
			#log(self.name, self.verbose, self.severity, logtext)

			# -----------------------------------------------------------------------------------------------------------------


	def stop(self):
		logtext = 'Thread ' +  self.name + ' is being stopped'
		log(self.name, self.verbose, self.severity, logtext)
		self.running = False

################################################################################################################################
# Function readConfigFile
################################################################################################################################
def readConfigFile():
	"""Function to initialise all the variables
	it uses the configparser python module imported at the top"""
	verbose = glob.verbose
	name = "READ CONFIG"
	severity = "INFO"
	# Initialistion, read configFile

	# Main
	glob.mainConfig = read_config(glob.configFile, 'main')
	logtext = "mainConfig = " + str(glob.mainConfig)
	log(name, verbose, severity, logtext)

	# arestio
	# glob.arestioConfig = read_config(glob.configFile, 'arestio')
	# logtext = "arestioConfig = " + str(glob.arestioConfig)
	# log(name, verbose, severity, logtext)

	# Horaires
	glob.horairesConfig = read_config(glob.configFile, 'horaires')
	logtext = "horairesConfig = " + str(glob.horairesConfig)
	log(name, verbose, severity, logtext)

	# SMS
	glob.smsConfig = read_config(glob.configFile, 'sms')
	logtext = "smsConfig = " + str(glob.smsConfig)
	log(name, verbose, severity, logtext)

	# Database
	glob.logDBConfig = read_config(glob.configFile, 'logdb')
	logtext = "logDBConfig = " + str(glob.logDBConfig)
	log(name, verbose, severity, logtext)

	# consignes
	glob.consignesConfig = read_config(glob.configFile, 'consignes')
	logtext = "consignesConfig = " + str(glob.consignesConfig)
	log(name, verbose, severity, logtext)

	# DigitalIO
	glob.digitalIOConfig = read_config(glob.configFile, 'digitalIO')
	logtext = "digitalIOConfig = " + str(glob.digitalIOConfig)
	log(name, verbose, severity, logtext)

	# AnalogIO
	glob.analogIOConfig = read_config(glob.configFile, 'analogIO')
	logtext = "analogIOConfig = " + str(glob.analogIOConfig)
	log(name, verbose, severity, logtext)

################################################################################################################################
# Function initialisation
################################################################################################################################
def initialisation():
	"""Function to initialise the relais board all set to 1, 1 is NOT trigger relais state"""
	verbose = glob.verbose
	name = "INIT       "
	severity = "INFO"
	# Initialistion, read configFile

	# Build the arest.io base url
	# glob.urlApi = 'http://' + glob.arestioConfig['api_url'] + ':' + glob.arestioConfig['api_url_port'] + '/'
	# logtext = "Base arest.io url is : " + glob.urlApi
	# log(name, verbose, severity, logtext)

	# #Arduino Pin set mode output and at 0 (relais) HIGH for the pin
	# for pin in glob.digitalIOConfig:
	# 	urlPath = 'mode/' + glob.digitalIOConfig[pin][1] + "/" + glob.digitalIOConfig[pin][3]
	# 	modeOutput = arestio(glob.urlApi, urlPath)
	# 	if modeOutput == False:
	# 		break
	# 		#TODO
	# 	urlPath = 'digital/' + glob.digitalIOConfig[pin][1] + "/" + glob.digitalIOConfig[pin][5]
	# 	modeOutput = arestio(glob.urlApi, urlPath)
	# 	if modeOutput == False:
	# 		break
	# 		#TODO clean stop
	
	wpi.wiringPiSetup()
	# Chaudiere First
	log(name, verbose, severity, "Initialisation relais chaudiere")
	wpi.pinMode(3, 1)
	commandeRelais(3, 1)
	# Circulateur
	log(name, verbose, severity, "Initialisation relais circulateur")
	wpi.pinMode(2, 1)
	commandeRelais(2, 1)
	# Vanne
	log(name, verbose, severity, "Initialisation relais Vanne 1")
	wpi.pinMode(4, 1)
	commandeRelais(4, 1)
	# Vanne 
	log(name, verbose, severity, "Initialisation relais Vanne 2")
	wpi.pinMode(0, 1)
	commandeRelais(0, 1)




################################################################################################################################
# Function arestio
################################################################################################################################
# def arestio(url, urlPath):
# 	"""This funtion use the rest API arest.io loaded on the arduino board. to retrieve analog pin values or set digital pin to 0 or 1
# 	"""
# 	verbose = glob.verbose
# 	name = "AREST      "
# 	severity = "INFO"

# 	api = Url(url)
# 	try:
# 		var = api.get(urlPath)
# 		logText = str(var.json())
# 		log(name, verbose, severity, logText)
# 		time.sleep(0.5)
# 		return var.json()
# 	except Exception as e:
# 		logtext = 'Cannot retreive: ' + url + urlPath + ' returning FALSE' + e
# 		log("ERROR", verbose,e)
# 		return False

################################################################################################################################
# Function commandeRelais
################################################################################################################################
def commandeRelais(wpiPort, wpiState):
	"""This funtion use wiringpi lib to set wpi port to 0 or 1
	0 trigger the relais, 1 release it 
	"""
	verbose = glob.verbose
	name = "WPI-RELAIS "
	severity = "INFO"

	if wpiPort == 2:
		relais = "Circulateur"
	else:
		relais = "Chaudiere"
	
	if wpiState == 0:
		action = "Demarrage"
	else:
		action = "Arret"

	try:
		wpi.digitalWrite(wpiPort, wpiState)
		logText = 'On ' + action + ' le : ' + relais
		log(name, verbose, severity, logText)
		return True
	except Exception as e:
		logText = action + ' IMPOSSIBLE du : ' + relais + e
		log(name,True, "ERROR", logText )
		return False
		
################################################################################################################################
# Function ReadAnalog
################################################################################################################################
def readAnalog(wpiPort):
	"""This funtion use wiringpi lib to readAnalog port 0 or 1
	"""
	verbose = glob.verbose
	name = "WPI-ANALOG "
	severity = "INFO"

	try:
		analogSensor = wpi.analogRead(wpiPort)
		logText = 'the value of the sensor is : ' + str(analogSensor)
		log(name, verbose, severity, logText)
		return analogSensor
	except Exception as e:
		logText = 'Cannot read the analog sensor attached to port: ' + str(wpiPort) + e
		log(name,True, "ERROR", logText )
		return False

################################################################################################################################
# Function Read1Wire
################################################################################################################################
def read1Wire():
	"""This funtion use wiringpi lib to 1 Wire dedicated port
	"""
	verbose = glob.verbose
	name = "WPI-1WIRE  "
	severity = "INFO"

	sensor = W1ThermSensor()

	try:
		temperature = sensor.get_temperature()
		logText = 'the value of the sensor is : ' + str(temperature)
		log(name, verbose, severity, logText)
		return temperature
	except Exception as e:
		logText = 'Cannot read the 1 Wire sensor attached' + e
		log(name,True, "ERROR", logText )
		return False

################################################################################################################################
# Function sendSMS
################################################################################################################################
def sendSMS(url, user, password, msg):
	"""fonction to sens sms to  mobile using free"""
	verbose = glob.verbose
	name = "SMS        "
	severity = "INFO"
	url = glob.smsConfig.url # "https://smsapi.free-mobile.fr/sendmsg"
	user = glob.smsConfig.user #"10279070"
	password = glob.smsConfig.password #"4cSINH8jiafqzI"
	msg = msg.replace(" ", "%20")

	# configure the free url and options
	smsUrl = url + "?user=" + user + "&password=" + password + "&msg=" + msg
	req =  request.Request( smsUrl , method="POST")
	response = request.urlopen(req)

################################################################################################################################
# Function consignesHoraires
################################################################################################################################
def consignesHoraires():
	""" On recupere les consignes horaires du jour et on met tout ca en seconde
	"""
	verbose = glob.verbose
	name = "HORAIRES   "
	severity = "INFO"

	# get the day of the week 0 -> Monday, ..
	# horaires format is like Lundi = 06:00 -> 21:30 qui veut dire debut a 6h30 et fin chauffage a 21h30
	localtime = time.localtime(time.time())
	jour = localtime.tm_wday
	if jour == 0:
		horaires = glob.horairesConfig['lundi'].split(' -> ')
	if jour == 1:
		horaires = glob.horairesConfig['mardi'].split(' -> ')
	if jour == 2:
		horaires = glob.horairesConfig['mercredi'].split(' -> ')
	if jour == 3:
		horaires = glob.horairesConfig['jeudi'].split(' -> ')
	if jour == 4:
		horaires = glob.horairesConfig['vendredi'].split(' -> ')
	if jour == 5:
		horaires = glob.horairesConfig['samedi'].split(' -> ')
	if jour == 6:
		horaires = glob.horairesConfig['dimanche'].split(' -> ')

	# On calcul le nombre de secondes depuis le debut de la journee pour les consignes.
	glob.heureDebut = int((horaires[0].split(':'))[0]) * 3600 + int((horaires[0].split(':'))[1]) * 60
	glob.heureFin = int((horaires[1].split(':'))[0]) * 3600 + int((horaires[1].split(':'))[1]) * 60
	logText = "heure debut : " + str(horaires[0]) + " en s : " + str(glob.heureDebut) + " heure fin : " + str(horaires[1]) + " en s : " + str(glob.heureFin)
	log(name, verbose, severity, logText)



################################################################################################################################
# Function Main
################################################################################################################################
def main():
	name = "MAIN       "
	severity = "INFO"
	verbose = True
	#verbose = glob.verbose
	running = True

	log(name, True, severity, " ** DEMARRAGE ** gestion chaudiere")

	# On initialise la plupart des variables
	readConfigFile()
	initialisation()

	# Create new threads
	# argument is Thread name used for logging purpose set to 11 charaters
	# Sensors
	ThreadReadSensors = myThreadReadSensors("SENSOR     ")
	# Chaudiere gestion du demarrage et arret
	ThreadChaudiere = myThreadChaudiere("CHAUDIERE  ")
	# Gestion de la vanne
	#ThreadVanne = myThreadVanne("VANNE      ")
	# Gestion du Circulateur
	ThreadCirculateur = myThreadCirculateur("CIRCULATEUR")
	# Gestion des consignes
	ThreadConsignes = myThreadConsignes("CONSIGNES  ")


	# Start new Threads
	ThreadReadSensors.start()
	#Sleep 10 seconds for the sensor to be read before we kick off tje thread chaudiere
	log(name, verbose, severity, "Wait 15s before starting next threads")
	time.sleep(15)


	#-------------------------------------------------------------------------------------------------------------------------
	# boucle principale de gestion de la chaudiere
	# On demarrae la chaudiere en fonction des consignes horaires
	while running:
		# Onlit les consignes horaires
		consignesHoraires()
		localtime = time.localtime(time.time())
		# glob.heureMaintenant = localtime.tm_hour * 3600 + localtime.tm_min * 60
		# # On verifie si heureMaintenant < consignes horaires basse
		# while glob.heureMaintenant < glob.heureDebut or glob.heureMaintenant > glob.heureFin:
		# 	if glob.heureMaintenant < glob.heureDebut:
		# 		logText = str(localtime.tm_hour) + "h" + str(localtime.tm_min) + " il est trop tot pour chauffer :) --on attent : " + str(glob.horairesConfig['sleep_horaires'])
		# 		log(name, verbose, severity, logText)
		# 	else:
		# 		logText = str(localtime.tm_hour) + "h" + str(localtime.tm_min) + " il est trop tard pour chauffer :) --on attent : " + str(glob.horairesConfig['sleep_horaires'])
		# 		log(name, verbose, severity, logText)

		# 	time.sleep(int(glob.horairesConfig['sleep_horaires']))
		# 	# On actualise l'heure
		# 	localtime = time.localtime(time.time())
		# 	glob.heureMaintenant = localtime.tm_hour * 3600 + localtime.tm_min * 60


		logText = str(localtime.tm_hour) + "h" + str(localtime.tm_min) + " Il est l'heure de demarrer la chaudiere :( "
		log(name, verbose, severity, logText)
		ThreadChaudiere.start()
		ThreadCirculateur.start()
		# la vanne 4 voies est tre abimees et elle fuie, on arrete de la piloter automatiquement
		#ThreadVanne.start()
		ThreadConsignes.start()

		# On actualise l'heure
		localtime = time.localtime(time.time())
		glob.heureMaintenant = localtime.tm_hour * 3600 + localtime.tm_min * 60
		# Verifie que l'on a pas depasser la consigne horaire haute
		while glob.heureMaintenant < glob.heureFin:
			logText = "Il est trop tot pour arreter la chaudiere :( --on attent : " + str(glob.horairesConfig['sleep_horaires'])
			log(name, verbose, severity, logText)
			time.sleep(int(glob.horairesConfig['sleep_horaires']))
			# On actualise l'heure
			localtime = time.localtime(time.time())
			glob.heureMaintenant = localtime.tm_hour * 3600 + localtime.tm_min * 60

		logText = str(localtime.tm_hour) + "h" + str(localtime.tm_min) + " Il est l'heure d'arreter la chaudiere :)"
		log(name, verbose, severity, logText)
		# lOn appel la fonction stop de la thread Chaudiere, cela arretera la chaudiere a la fin de son prochain cycle
		ThreadChaudiere.stop()
		#ThreadVanne.stop()
		ThreadConsignes.stop()
		ThreadCirculateur.is_alive()
		# On attend un cycle d'attente sinon on va rester dans le meme cycle et le premier while va etre sauter
		time.sleep(int(glob.horairesConfig['sleep_horaires']))

if __name__ == '__main__':
	main()
