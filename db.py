import datetime
from mysql.connector import MySQLConnection, Error
from configParser import read_config

configFile = "config.ini"
dbConfig = read_config(configFile, 'logdb')

def select_iodata():
    query = "SELECT from_unixtime(date), value from iotdata;"

    try:
        
        conn = MySQLConnection(**dbConfig)

        cursor = conn.cursor()
        cursor.execute(query)

        for (date, value) in cursor:
            print("{\n\t\"dtate\":", date, "\n\t\"value\":", value.decode("utf-8"), "\n},")
            #print(value.decode("utf-8"))

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def main():
    select_iodata()

if __name__ == '__main__':
    main()

"""cnx = mysql.connector.connect(user='scott', database='employees')
cursor = cnx.cursor()

query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query, (hire_start, hire_end))

for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))

cursor.close()
cnx.close()"""