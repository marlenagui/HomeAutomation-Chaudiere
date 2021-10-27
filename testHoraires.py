from configParser import read_config
from log import log
import datetime
import time
import json


class glob(object):
	"""global variables definition"""
	verbose = True
	severity = "INFO"
	# define the config.ini file to use.
	configFile = 'config.ini'
	#define the sections of the config file 
	horairesConfig = {}

def initiatilisation():
	"""Function to initialise all the variables
	it uses the configparser python module imported at the top"""
	verbose = glob.verbose
	name = "INIT       "
	severity = "INFO"

	glob.horairesConfig = read_config(glob.configFile, 'horaires')
	logtext = "horairesConfig = " + str(glob.horairesConfig)
	log(name, verbose, severity, logtext)

def readHoraires():
	localtime = time.localtime(time.time())
	jour = localtime.tm_wday
	print("localtime : ", localtime)
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

	heureDebut = int((horaires[0].split(':'))[0]) * 3600 + int((horaires[0].split(':'))[1]) * 60
	heureFin = int((horaires[1].split(':'))[0]) * 3600 + int((horaires[1].split(':'))[1]) * 60
	heureMaintenant = localtime.tm_hour * 3600 + localtime.tm_min * 60
	print("heure debut en s : ", heureDebut, "heure fin en s : ", heureFin, "heure maintenant en s : ", heureMaintenant)



def main():
	name = "MAIN       "
	severity = "INFO"
	verbose = glob.verbose

	log(name, True, severity, "-- DEMARRAGE -- Programme")
	
	initiatilisation()
	readHoraires()

if __name__ == '__main__':
	main()