import cv2
import numpy as np
import time
import os
import handtrack as htm
brushthickness=15
eraserthickness=50
folderpath = "header"
mylist = os.listdir(folderpath)
# print(mylist
# )
overlaylist=[]
for impath in mylist:
    image= cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
# print(len(overlaylist))
header = overlaylist[0]
drawColor= (255,0,0)
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = htm.handDetector(detectionCon=0.8)
imgcanva= np.zeros((720, 1280, 3), np.uint8)
while True:
    istrue, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        # print(len(lmlist))``
         #print(lmlist[0][8])
          x1, y1 = lmlist[8][1:]
          x2, y2 = lmlist[12][1:]
          fingers = detector.fingersUp()
        #   print(fingers)
          if fingers[1] and fingers[2]:
            xp,yp=0,0
            if y1<125:
               if 0<x1<250:
                  header=overlaylist[0]
                  drawColor=(255,0,0)
               elif 300<x1<450:
                  header=overlaylist[1]
                  drawColor=(255,0,255)
               elif 600<x1<750:
                    header=overlaylist[2]
                    drawColor=(0,255,255)
               elif 900<x1<1200:
                    header=overlaylist[3]
                    drawColor=(0,0,0)
            # cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)

          if fingers[1] and fingers[2]==False:
           cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)
           if xp==0 and yp==0:
               xp,yp= x1,y1
           if drawColor == (0,0,0):
            cv2.line(img, (xp, yp), (x1,y1), drawColor, eraserthickness)
            cv2.line(imgcanva, (xp, yp), (x1,y1), drawColor, eraserthickness)
                
           cv2.line(img, (xp, yp), (x1,y1), drawColor, brushthickness)
           cv2.line(imgcanva, (xp, yp), (x1,y1), drawColor, brushthickness)
           xp,yp = x1,y1
    imggray = cv2.cvtColor(imgcanva, cv2.COLOR_BGR2GRAY)
    _, imginverse = cv2.threshold(imggray, 50,255, cv2.THRESH_BINARY_INV)
    imginverse= cv2.cvtColor(imginverse, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imginverse)
    img = cv2.bitwise_or(img, imgcanva)
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgcanva, 0.5, 0)
    cv2.imshow("vdo", img)
    # cv2.imshow("vdo1", imgcanva)
    cv2.waitKey(1)
