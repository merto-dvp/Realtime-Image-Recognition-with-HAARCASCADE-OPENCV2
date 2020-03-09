import cv2
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util


cameraNo = 0

casSTM="odtu.xml"
casODTU="stm.xml"
casORT="ort.xml"
casH="heli.xml"

objSTM="STM"
objODTU="ODTU"
objORT="ORT"
objH="H"

frameWidth= 640
frameHeight = 480
colorH= (255,0,0)
colorSTM=(0,55,255)
colorODTU=(255,200,100)
colorORT=(0,0,0)

#################################################################


cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

# CREATE TRACKBAR
cv2.namedWindow("Result")
cv2.resizeWindow("Result",frameWidth,frameHeight+100)
cv2.createTrackbar("Brightness","Result",200,255,empty)


cascadeH = cv2.CascadeClassifier(casH)
cascadeSTM = cv2.CascadeClassifier(casSTM)
cascadeODTU= cv2.CascadeClassifier(casODTU)
cascadeORT= cv2.CascadeClassifier(casORT)

frame_rate_calc = 1
freq = cv2.getTickFrequency()
while True:

    t1 = cv2.getTickCount()
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    objectsH=cascadeH.detectMultiScale(gray,1.1, 12)
    objectsSTM= cascadeSTM.detectMultiScale(gray,1.1, 4)
    objectsODTU= cascadeODTU.detectMultiScale(gray,1.1, 20)
    objectsORT= cascadeORT.detectMultiScale(gray,1.04, 1)


    for (x,y,w,h) in objectsORT:
         area = w*h
         if area >1600:
             cv2.rectangle(img,(x,y),(x+w,y+h),colorORT,3)
             print("ORT :"+" x:"+str(x)+" ,y:"+str(y)+" ,w:"+str(w)+" ,h:"+str(h))
             cv2.putText(img,objORT,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,colorORT,2)
             roi_color = img[y:y+h, x:x+w]


    for (x,y,w,h) in objectsSTM:
         area = w*h
         if area >10000:
             cv2.rectangle(img,(x,y),(x+w,y+h),colorSTM,3)
             print("STM :"+" x:"+str(x)+" ,y:"+str(y)+" ,w:"+str(w)+" ,h:"+str(h))
             cv2.putText(img,objSTM,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,colorSTM,2)
             roi_color = img[y:y+h, x:x+w]


    for (x,y,w,h) in objectsH:
        area = w*h
        if area >20000:
            cv2.rectangle(img,(x,y),(x+w,y+h),colorH,3)
            print("H:"+" x:"+str(x)+" ,y:"+str(y)+" ,w:"+str(w)+" ,h:"+str(h))
            cv2.putText(img,objH,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,colorH,2)
            roi_color = img[y:y+h, x:x+w]


    for (x,y,w,h) in objectsODTU:
        area = w*h
        if area >30000:
            cv2.rectangle(img,(x,y),(x+w,y+h),colorODTU,3)
            print("ODTU:"+" x:"+str(x)+" ,y:"+str(y)+" ,w:"+str(w)+" ,h:"+str(h))
            cv2.putText(img,objODTU,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,colorODTU,2)
            roi_color = img[y:y+h, x:x+w]


    #img=cv2.flip(img,-1)
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1
    cv2.putText(img,'FPS: {0:.2f}'.format(frame_rate_calc),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
