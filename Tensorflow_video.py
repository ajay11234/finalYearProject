import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime


IM_WIDTH = 160    ##Use smaller resolution for
IM_HEIGHT = 120

##cap = cv2.VideoCapture(0)
count = 0
scount = 0
bcount = 0
hcount = 0
icount = 0
kcount = 0
hkcount = 0
ajcount = 0
dancount = 0
ikcount = 0
jcount = 0
wcount = 0
amcount = 0
jmcount = 0
sys.path.append("..")

from utils import label_map_util

from utils import visualization_utils as vis_util

##MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
CWD_PATH = os.getcwd()

# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
 
# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 90


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

camera = cv2.VideoCapture(0)
ret = camera.set(3,IM_WIDTH)
ret = camera.set(4,IM_HEIGHT)

import time
import sys

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

########################









####################################
   
   



while(True):
    
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
    

    
    def insertPythonVaribleInTable(Id, Product, Price):
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

    ##########################################################
    if False:
            np_arr8_string = hx.get_np_arr8_string()
            binary_string = hx.get_binary_string()
            print(binary_string + " " + np_arr8_string)
    val = hx.read_long()   
        ##val = max(0, int(hx.get_weight(5)))
        
    if(val > 0):
        print(val)
        for i in range(11000,11800):
            amcount = amcount + 1
            if(amcount == 1):
                reduce(4)
            
        for i in range(5000,10000):
            jmcount = jmcount + 1
            if(jmcount + 1):
                reduce(6)
        
        
    else:
        print(0)
        count = 0
        scount = 0
        icount = 0
        jcount = 0
        hkcount = 0
        kcount = 0
        ajcount = 0
        dancount = 0
        bcount = 0
        wcount = 0
        for i in range(10):
            reduce(i)
            
        
        
        
        ##print(val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    
    
    #########################################################
    
    t1 = cv2.getTickCount()

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
    ret, frame = camera.read()
    frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],feed_dict={image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)
    ###print(classes)
    threshold = 0.5
    objects = []
    
    for index, value in enumerate(classes[0]):
         object_dict = {}
         if scores[0, index] > threshold:
             print(index)
             object_dict[(category_index.get(value)).get('name').encode('utf8')] = scores[0, index]
                #print(category_index.get(value))
             objects.append(object_dict)
             for obj in objects:
                 for cj,ij in enumerate(obj):
                     if(ij == b'bottle'):
                         count = count + 1
                         if(count == 1):
                             ajay = "bottle"
                             insertPythonVaribleInTable(1, "Bottle", 80)
                             print(ajay)
                         elif(count > 1):
                             ajay = 0
                     if(ij == b'apple'):
                         scount = scount + 1
                         if(scount == 1):
                             dan = "apple"
                             insertPythonVaribleInTable(2,"apple",250)
                             print(dan)
                         elif(scount > 1):
                             dan = 0
                     if(ij == b'book'):
                         bcount = bcount +1
                         if(bcount == 1):
                             san = "book"
                             insertPythonVaribleInTable(3,"book",125)
                             print(san)
                         elif(bcount > 1):
                             san = 0
                     if(ij == b'cell phone'):
                         jcount = jcount + 1
                         if(jcount == 1):
                             jan = "cell phone"
                             amcount = 0
                             insertPythonVaribleInTable(4,"Samsung phone",4500)
                             print(jan)
                         elif(jcount > 1):
                             jan = 0
                     if(ij == b'cup'):
                         icount = icount + 1
                         if(icount == 1):
                             han = "cup"
                             insertPythonVaribleInTable(5,"cup",25)
                             print(han)
                         elif(icount > 1):
                             han = 0
                     if(ij == b'tv' or ij == b'suitcase'):
                         ajcount = ajcount + 1
                         if(ajcount == 1):
                             jmcount = 0
                             yan = "Wallet"
                             insertPythonVaribleInTable(6,"Wallet",250)
                             print(yan)
                         elif(ajcount > 1):
                             yan = 0
                     if(ij == b'toothbrush'):
                         hkcount = hkcount + 1
                         if(hkcount == 1):
                             can = "toothbrush"
                             insertPythonVaribleInTable(7,"toothbrush",85)
                             print(can)
                         elif(hkcount > 1):
                             can = 0
                     if(ij == b'sports ball'):
                         dancount = dancount + 1
                         if(dancount == 1):
                             fan = "sports ball"
                             insertPythonVaribleInTable(8,"tennis ball",60)
                             print(fan)
                         elif(dancount > 1):
                             fan = 0
                     if(ij == b'spoon'):
                         kcount = kcount + 1
                         if(kcount == 1):
                             htfan = "spoon"
                             insertPythonVaribleInTable(9,"spoon",20)
                             print(htfan)
                         elif(kcount > 1):
                             htfan = 0
                     if(ij == b'banana'):
                         ikcount = ikcount + 1
                         if(ikcount == 1):
                             tan = "banana"
                             insertPythonVaribleInTable(10,"banana",15)
                             print(tan)
                         elif(ikcount > 1):
                             tan = 0 
                     if(ij == b'bowl'):
                         wcount = wcount + 1
                         if(wcount == 1):
                             lan = "bowl"
                             insertPythonVaribleInTable(11,"bowl",80)
                             print(lan)
                         elif(wcount > 0):
                             
                             lan = 0 
                                  
                         ##print(ij)    
    cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1

        # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()

cv2.destroyAllWindows()

