from mysql.connector import MySQLConnection, Error
from configParser import read_config
import time


def select_log_mysql(dbConfig):
    # Create a temp list to store the what returned by SELECT
    temp = []
    temp2 = ""

    dbConfig = dbConfig

    try:
        conn = MySQLConnection(**dbConfig)
        cursor = conn.cursor()

        if conn.is_connected():

            # calcul l'epoch date du debut du jour actuel
            midnightdaydate = int(time.time()) - ( time.gmtime().tm_hour * 3600 ) - (time.gmtime().tm_min * 60 ) - time.gmtime().tm_sec

            # Select tous les records du jour
            query = "SELECT  date, value FROM iotdata WHERE iotid = 1 and date > '%d'" % midnightdaydate
            cursor.execute(query)
            # parcours le cursor et recupere date et value cf le select juste avant
            for (date, value) in cursor:
                temp.append("{\"date\": \"" +  time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(date)) + "\", \"value\": " + value.decode('utf-8') + "}")

            # get the number of item of the list -1 (-2 because it start at 0)
            counter = (len(temp) - 1 )

            # On cree une list du retour de select avec une virgule a la fin sauf pour le dernier qui ne doit pas avoir de virgule
            for value in range(counter):
                temp2 = temp2 + str(temp[value] + "," + "\n")
            temp2 = temp2 + str(temp[len(temp) - 1])
            print(temp2)
            return temp2
            #Create the html file out of the template
            #fileTemplate = open('template.html', mode='r')
            #fileOutput = open('/var/www/html/chaudiere.html', mode='w')
            #for line in fileTemplate:
            #    fileOutput.write(line.replace('dataToReplace', temp2))
            #fileTemplate.close()
            #fileOutput.close()

        else:
            print('connection failed.')

        conn.close()


    except Error as error:
        print(error)


def select_log_mysql2(dbConfig):
    # Create a temp list to store the what returned by SELECT
    temp = []
    temp2 = ""

    dbConfig = dbConfig

    try:
        conn = MySQLConnection(**dbConfig)
        cursor = conn.cursor()

        if conn.is_connected():

            # calcul l'epoch date du debut du jour actuel
            midnightdaydate = int(time.time()) - ( time.gmtime().tm_hour * 3600 ) - (time.gmtime().tm_min * 60 ) - time.gmtime().tm_sec

            # Select tous les records du jour
            query = "SELECT  date, value FROM iotdata WHERE iotid = 5 and date > '%d'" % midnightdaydate
            cursor.execute(query)
            # parcours le cursor et recupere date et value cf le select juste avant
            for (date, value) in cursor:
                temp.append("{\"date\": \"" +  time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(date)) + "\", \"value\": " + value.decode('utf-8') + "}")

            # get the number of item of the list -1 (-2 because it start at 0)
            counter = (len(temp) - 1 )

            # On cree une list du retour de select avec une virgule a la fin sauf pour le dernier qui ne doit pas avoir de virgule
            for value in range(counter):
                temp2 = temp2 + str(temp[value] + "," + "\n")
            temp2 = temp2 + str(temp[len(temp) - 1])
            print(temp2)
            return temp2


        else:
            print('connection failed.')

        conn.close()


    except Error as error:
        print(error)


    #finally:


def main():
    configFile = '../config.ini'
    dbConfig = read_config(configFile, 'logdb')
    temp2 = select_log_mysql(dbConfig)
    temp3 = select_log_mysql2(dbConfig)
    #Create the html file out of the template
    fileTemplate = open('./js/chaudiereOnOff.js', mode='r')
    fileTemplate2 = open('./js/tempDepartEau.js', mode='r')
    fileOutput = open('/var/www/html/js/chaudiereOnOff.js', mode='w')
    fileOutput2 = open('/var/www/html/js/tempDepartEau.js', mode='w')
    for line in fileTemplate:
        fileOutput.write(line.replace('dataToReplace', temp2))
    for line in fileTemplate2:
        fileOutput2.write(line.replace('dataToReplace', temp3))
    fileTemplate.close()
    fileOutput.close()
    fileOutput2.close()

if __name__ == '__main__':
    main()
