#! /usr/bin/python2

import time
import sys
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()
scount = 0
hcount = 0
jcount = 0
hx = HX711(5, 6)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(1)

hx.reset()
#hx.tare()

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

while True:
    
    
    def reduce(mobile_id):
        
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
           #mobile_id = 1
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
    
    
    def insert(Id, Product, Price):
        
        try:
            
            connection = mysql.connector.connect(host='localhost',
                             database='mydb',
                             user='ajay',
                             password='ajay5596')
            cursor = connection.cursor(prepared=True)
            sql_insert_query = """ INSERT INTO `tableC`
                          (`id`, `Product`, `Price`) VALUES (%s,%s,%s)"""
            insert_tuple = (Id, Product, Price)
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
    
    
    
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        if False:
            np_arr8_string = hx.get_np_arr8_string()
            binary_string = hx.get_binary_string()
            print(binary_string + " " + np_arr8_string)
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        ##val = hx.get_weight(5)
        val = hx.read_long()   
        ##val = max(0, int(hx.get_weight(5)))
        
            
        
        if(val > 0):
            print(val)
                
        else:
            print(0)
            
        
                
            
        
        ##print(val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
