import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
try:
   conn = mysql.connector.connect(host='localhost',
                             database='mydb',
                             user='ajay',
                             password='ajay5596')
   cursor = conn.cursor()
   print ("Displaying records Before Deleting single record from mobile table")
   sql_select_query = """select * from tableC"""
   cursor.execute(sql_select_query)
   records = cursor.fetchall()
   for record in records :
       print (record)
   #Delete record now
   sql_Delete_query = """Delete from tableC where id = %s"""
   mobile_id = 1
   cursor.execute(sql_Delete_query,(mobile_id,))
   conn.commit()
   print ("\nRecord Deleted successfully ")
   print("\nDisplaying Total records from mobile table after Deleting single record \n ")
   cursor.execute(sql_select_query)
   records = cursor.fetchall()
   for record in records:
       print(record)
except mysql.connector.Error as error :
    print("Failed to delete record to database: {}".format(error))
finally:
    #closing database connection.
    if(conn.is_connected()):
        conn.close()
        print("MySQL connection is closed")