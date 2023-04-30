import cv2
import time
import numpy as np
import htm
import math
####

import paho.mqtt.client as mqtt

# Define MQTT broker address and port
broker_address = "test.mosquitto.org"
broker_port = 1883

# Create MQTT client instance
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_address, broker_port)

###
cap = cv2.VideoCapture(0)
cap.set(3,440)
cap.set(4,220)

detector = htm.handDetector()



while True :
    success,img=cap.read()
    img=detector.findHands(img)

    lmList = detector.findPosition(img, draw=True)
    if len(lmList[0])!=0:
        #print((lmList[0])[4],(lmList[0])[8])

        x1,y1=(lmList[0])[4][1] , (lmList[0])[4][2]
        x2,y2=(lmList[0])[8][1] , (lmList[0])[8][2]
        cx,cy=(x1+x2)//2 ,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(125,0,125),cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (125, 0, 125), cv2.FILLED)
        cv2.line(img, (x1, y1),(x2,y2), (0, 0, 125),5)
        cv2.circle(img, (cx,cy), 10, (125, 0, 125), cv2.FILLED)
        #print(x1,y1)

        length=math.hypot(x2-x1,y2-y2)
        print(length)

        # Publish the length value to the MQTT broker
        topic = "hand/length"
        payload = str(length)
        client.publish(topic, payload)
###
    cv2.imshow("Img",img)
    cv2.waitKey(1)
