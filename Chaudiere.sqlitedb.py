import sqlite3
import urllib.request
import requests
from nap.url import Url
import datetime
import time



def connectDB(database):
	con = sqlite3.connect(database)
	c = con.cursor()
	# get to the last row
	newId = c.lastrowid

def insertinDB(date, temperature, humidity):
	c.execute("INSERT INTO temphum (dateTime,temp,humidity) VALUES (17,35)")
	con.commit()


while 1:
	#set target ip address
	api = Url('http://192.168.1.4:8088/')
	#Read temperature, json is returned
	temp= api.get('temperature').json()
	#Read humidity, json is returned
	humidity = api.get('humidity').json()
	#Read tempExt, json is returned
	tempDepartEau = api.get('temperatureEXT').json()
	tempDepartEauChaudiere = api.get('analog/1').json()
	tempEauChaudiere = api.get('analog/3').json()
	#print temperatures and humdity on the console
	print ("la temperature est de : \t\t", temp['temperature'])
	print ("L'humidite est de : \t\t\t", humidity['humidity'])
	print ("La temperature depart Eau est de : \t", tempDepartEau['temperatureEXT'])
	print ("La temperature depart Eau Chaudiere est de : \t", tempDepartEauChaudiere['return_value'])
	print ("La temperature Chaudiere est de : \t", tempEauChaudiere['return_value'])


	con = sqlite3.connect("chaudiere.db")
	c = con.cursor()
	
	newId = c.lastrowid
	c.execute("INSERT INTO chaudiere (dateTime,temp,humidity,tdeparteau,tdeparteauchaudiere,teauchaudiere) VALUES (?,?,?,?,?,?)", (datetime.datetime.now(), temp['temperature'], humidity['humidity'],tempDepartEau['temperatureEXT'],tempDepartEauChaudiere['return_value'],tempEauChaudiere['return_value']))
	con.commit()
	con.close()
	print ("pause 15s min")
	time.sleep(15) 



