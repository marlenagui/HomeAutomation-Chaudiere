import datetime
from mysql.connector import MySQLConnection, Error
from configParser import read_config
from nap.url import Url
import time

class glob(object):
	"""global variables definition"""
	verbose = False
	# define the config.ini file to use.
	configFile = '../config.ini'
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
	urlApi = ''
	
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

def arestio(url, urlPath):
	"""This funtion use the rest API arest.io loaded on the arduino board. to retrieve analog pin values or set digital pin to 0 or 1
	"""
	api = Url(url)
	try: 
		var = api.get(urlPath)
		time.sleep(0.5)
		return var.json()
	except Exception as e:
		print("ERROR", e)
		return False

def main():
	
	while 1: 
		glob.dbConfig = read_config(glob.configFile, 'logdb')
		glob.analogIOConfig = read_config(glob.configFile, 'analogIO')
		glob.arestioConfig = read_config(glob.configFile, 'arestio')
		glob.urlApi = 'http://' + glob.arestioConfig['api_url'] + ':' + glob.arestioConfig['api_url_port'] + '/'

		urlPath = 'analog/' + glob.analogIOConfig['temp_depart_eau_viessman']
		glob.tempDepartEauViessman = arestio(glob.urlApi, urlPath)
		print("temp depart eau : ", glob.tempDepartEauViessman['return_value'])
		time.sleep(2.5)

if __name__ == '__main__':
    main()
