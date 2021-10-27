from mysql.connector import MySQLConnection, Error
from configParser import read_config
import time
 
def insert_log_mysql(date, function, severity, text):
    date = date
    function = function
    severity = severity
    text =text
    print("date : ", date, " function : ", function, " severity : ", severity, " text : ", text)
    query = "INSERT INTO chaudiere (date, function, severity, text) " \
            "VALUES (%s, %s, %s, %s)"

    args = (date, function, severity, text)

    db_config = read_config("config.ini","db")

    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        
        if conn.is_connected():
            cursor.execute(query, args)
            conn.commit()
        else:
            print('connection failed.')

        conn.close()
        """if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')"""

        

    except Error as error:
        print(error)
 
    #finally:
        
 
def main():
    insert_log_mysql(int(time.time()),'TEST', 'INFO', 'Ceci est un test')

if __name__ == '__main__':
    main()