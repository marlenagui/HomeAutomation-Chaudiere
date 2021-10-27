import time
import sqlite3
from mysql.connector import MySQLConnection, Error
from configParser import read_config

################################################################################################################################
# Global variables
################################################################################################################################

class glob(object):
	"""global variables definition"""
	verbose = False
	# define the config.ini file to use.
	configFile = 'config.ini'
	#define the sections of the config file
	logDBConfig = {}

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

	# Database
	glob.logDBConfig = read_config(glob.configFile, 'logdb')
	logtext = "logDBConfig = " + str(glob.logDBConfig)
	log(name, verbose, severity, logtext)



################################################################################################################################
# Function insertLogMysql
################################################################################################################################
def insertLogMysql(date, function, severity, text):
    date = date
    function = function
    severity = severity
    text =text

    query = "INSERT INTO log (date, function, severity, text) " \
            "VALUES (%s, %s, %s, %s)"

    args = (date, function, severity, text)

    #db_config = read_config("config.ini","logmysqldb")
    db_config = {
        'user': 'sepenet@adco-container-aks-demo-mysql',
        'password': 'Seb@MS-2020-MySQL',
        'host': 'adco-container-aks-demo-mysql.mysql.database.azure.com',
        'database': 'log',
        'ssl_ca': 'BaltimoreCyberTrustRoot.crt.pem'
    }

    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        if conn.is_connected():
            cursor.execute(query, args)
            conn.commit()
        else:
            print('connection failed.')

        conn.close()

    except Error as error:
        print(error)

################################################################################################################################
# Function insertLogSqlite3
################################################################################################################################
def insertLogSqlite3(date, function, severity, text):
    date = date
    function = function
    severity = severity
    text = text

    try:
        connection = sqlite3.connect("log.db")
        cursor = connection.cursor()

        newId = cursor.lastrowid
        cursor.execute("""
        INSERT INTO log(date, function, severity, text) VALUES(?, ?, ?, ?)""", (date, function, severity, text))
        connection.commit()

    except sqlite3.Error as e:
        print("Error :", e.args[0])

    finally:
        if connection:
            connection.close()

################################################################################################################################
# Function insertIOTDataSqlite3
################################################################################################################################
def insertIOTDataSqlite3(iotid, date, value):
    date = date
    iotid = iotid
    value = value

    try:
        connection = sqlite3.connect("iot.db")
        cursor = connection.cursor()

        newId = cursor.lastrowid
        cursor.execute("""
        INSERT INTO iotdata(date, iotid, value) VALUES(?, ?, ?)""", (date, iotid, value))
        connection.commit()

    except sqlite3.Error as e:
        print("Error :", e.args[0])

    finally:
        if connection:
            connection.close()

################################################################################################################################
# Function insertIOTDataMysql
################################################################################################################################
def insertIOTDataMysql(iotid, date, value):
    date = date
    value = value

    query = "INSERT INTO iotdata (iotid, date, value) " \
            "VALUES (%s, %s, %s)"

    args = (iotid, date, value)

    db_iot = {
        'user': 'sepenet@adco-container-aks-demo-mysql',
        'password': 'Seb@MS-2020-MySQL',
        'host': 'adco-container-aks-demo-mysql.mysql.database.azure.com',
        'database': 'iot',
        'ssl_ca': 'BaltimoreCyberTrustRoot.crt.pem'
    }

    try:
        conn = MySQLConnection(**db_iot)
        cursor = conn.cursor()

        if conn.is_connected():
            cursor.execute(query, args)
            conn.commit()
        else:
            print('connection failed.')

        conn.close()

    except Error as error:
        print(error)

################################################################################################################################
# Function log
################################################################################################################################
def log(name, verbose = False, severity="INFO ", text="Free text"):
	name = name
	verbose = verbose
	severity = severity
	logTime = time.ctime(time.time())
	logText = logTime + ' :: ' + name + ' :: ' + ' -- ' + severity + ' -- ' + str(text)
	#insertLogSqlite3(int(time.time()), name, severity, str(text))
	insertLogMysql(int(time.time()), name, severity, str(text))
	if verbose == True:
		print(logText)
