import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    conn = None
    date = "2021-01-05T20:51:03.00"
    temp = 101
    try:
        conn = mysql.connector.connect(host='adco-container-aks-demo-mysql.mysql.database.azure.com',
                                       database='iot',
                                       user='sepenet@adco-container-aks-demo-mysql',
                                       password='Seb@MS-2020-MySQL',
                                       ssl_ca='BaltimoreCyberTrustRoot.crt.pem')
        cursor = conn.cursor()
        if conn.is_connected():
            print('Connected to MySQL database')
            query = "INSERT INTO externaltemperature (datetime, temperature) " \
                    "VALUES (%s, %s)"
            args = (date, temp)
            cursor.execute(query, args)
            conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    connect()