import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
def insertPythonVaribleInTable(userId, Product, Price):
    try:
        connection = mysql.connector.connect(host='localhost',
                             database='mydb',
                             user='ajay',
                             password='ajay5596')
        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO `ajay`
                          (`id`, `Product`, `Value`) VALUES (%s,%s,%s)"""
        insert_tuple = (userId, Product, Price)
        result  = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print ("Record inserted successfully into python_users table")
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
insertPythonVaribleInTable(1,"Wallet",175)
insertPythonVaribleInTable(2, "pen", 15)