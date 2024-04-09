import cv2
import numpy as np
import mediapipe as mp
import handtrack as ht

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1280)
detector = ht.handDetector()
while True:
    bool, img = cap.read()
    img=detector.findHands(img)
    lmlist, bbox=detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        number=[]
        if lmlist[4][1]<lmlist[3][1]:
                number.append(1)
        else:
                number.append(0)
        for id in (8,12,16,20):
            if lmlist[id][2]<lmlist[id-2][2]:
                number.append(0)
            else:
                number.append(1)
        # print(number)
        count=0
        for finger in enumerate(number):
            #  print(finger)
            
            if finger[1]==0:
                 count=count+1
        cv2.putText(img, 'Number:'+str(count), (10,70), 2,2,(255,100,0), 3,cv2.FILLED)
    cv2.imshow('video',img)
    cv2.waitKey(1)