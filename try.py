import cv2
import numpy as np
import mediapipe as mp
import handtrack as ht
import math

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1280)
detector = ht.handDetector()
while True:
    bool, img = cap.read()
    img=detector.findHands(img)
    lmlist, bbox=detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        x1, y1=lmlist[4][1], lmlist[4][2]
        x2, y2=lmlist[8][1], lmlist[8][2]
        x3, y3=lmlist[12][1], lmlist[12][2]
        lenght = math.hypot(x1-x1, y1-y2)
        # print(lenght)
        cv2.circle(img, (x1,y1), 15, (0,255,0), 3, cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (0,255,0), 3, cv2.FILLED)
        # cv2.circle(img, (x3,y3), 3, (0,255,0), 3, cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 4, cv2.FILLED)
        # cv2.line(img, (x3,y3), (x1,y1), (0,255,255), 2, cv2.FILLED)
        if lenght<20:
            cv2.circle(img, (x1,y1), 15, (0,255,255), 3, cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (0,255,255), 3, cv2.FILLED)
            cv2.putText(img, 'Hello motto!!',(10,70), 3, 1, (100,0,255), 3, cv2.FILLED)
    cv2.imshow('video',img)
    cv2.waitKey(1)