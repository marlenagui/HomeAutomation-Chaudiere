import time
import sqlite3
from mysql.connector import MySQLConnection, Error

def select_log():
    try:
        print("--TRY-- SELECT")
        connection = sqlite3.connect("log.db")
        cursor = connection.cursor()

        newId = cursor.lastrowid
        cursor.execute("""
        SELECT date, function, severity, text FROM log """)
        rows = cursor.fetchall()
        for row in rows:
            print("date : ", row[0], ", function : ", row[1], ", serverity : ", row[2], ", text : ", row[3])

    except sqlite3.Error as e:
        print("Error :", e.args[0])

    finally:
        print("--FINALLY--")
        if connection:
            connection.close()

def insert_log(date, function, severity, text):
    date = date
    function = function
    severity = severity
    text = text

    try:
        print("--TRY--")
        connection = sqlite3.connect("log.db")
        cursor = connection.cursor()

        newId = cursor.lastrowid
        cursor.execute("""
        INSERT INTO log(date, function, severity, text) VALUES(?, ?, ?, ?)""", (date, function, severity, text))
        connection.commit()

    except sqlite3.Error as e:
        print("Error :", e.args[0])

    finally:
        print("--FINALLY--")
        if connection:
            connection.close()


def insert_log_mysql(date, function, severity, text):
    date = date
    function = function
    severity = severity
    text =text

    query = "INSERT INTO Chaudiere(date, function, severity, text) " \
            "VALUES (%d, %s, %s, %s)"

    args = (date, function, severity, text)

    print("before try")

    try:
        print("--MYSQL TRY--")
        conn = MySQLConnection("localhost", "root", "Seb@0103", "Log")
        cursor = conn.cursor()
        print('connected to database')
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()

    except Error as error:
        print("except loop")
        print(error)
    finally:
        cursor.close()
        conn.close()

def main():
    insert_log(int(time.time()),"TEST", "INFO", "Ceci est un test different")
    #insert_log_mysql(int(time.time()),"TEST", "INFO", "Ceci est un test")
    print(int(time.time()))
    select_log()

if __name__ == '__main__':
    main()
