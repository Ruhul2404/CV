import numpy as np
import cv2
from handtrack import handDetector
import os
width, height =  1920, 1080
threshhold = 300
buttompress = False
buttoncounter = 0
buttondelay=22
annotations =[[]]
annotaionsnum = -1
annotationsstart = False
folderpath = 'presentation'
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pathimg = os.listdir(folderpath)
# print(pathimg)
imgnum = 0
hs, ws = int(120*1.5), int(213*1.5)
detector = handDetector(detectionCon=0.8, maxHands=1)
while True:
    suc, img = cap.read()
    img = cv2.flip(img, 1)
    pathfullimg = os.path.join(folderpath, pathimg[imgnum])
    imgcurrent = cv2.imread(pathfullimg)
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=False)
    if buttompress is False:
        if len(lmlist) !=0:
            fingers = detector.fingersUp()
            y1 = lmlist[9][2]

            # index = lmlist[8][1], lmlist[8][2]
            xval = int(np.interp(lmlist[8][1], [1280//2, 1280], [0, 1920]))
            yval = int(np.interp(lmlist[8][2], [150, 720-250], [0, 1080])) 
            index = xval, yval
            if y1 <=threshhold:
                if fingers == [1,0,0,0,0]:
                        # print('left')
                        
                        if imgnum>0:
                            buttompress = True
                            annotations =[[]]
                            annotaionsnum = -1
                            annotationsstart = False
                            imgnum -=1
                if fingers == [0,0,0,0,1]:
                        # print('right')
                        
                        if imgnum <len(pathimg)-1:
                            buttompress = True
                            annotations =[[]]
                            annotaionsnum = -1
                            annotationsstart = False
                            imgnum +=1
            if fingers == [0,1,1,0,0]:
                    cv2.circle(imgcurrent, index, 12, (0,0,255),5)
            if fingers == [0,1,0,0,0]:
                    if annotationsstart is False:
                         annotationsstart = True
                         annotaionsnum +=1
                         annotations.append([])
                    cv2.circle(imgcurrent, index, 12, (0,0,255), 5)
                    annotations[annotaionsnum].append(index)
            else:
                 annotationsstart=False
            

                 
    if buttompress:
         buttoncounter+=1
         if buttoncounter > buttondelay:
              buttoncounter=0
              buttompress=False
    for i in range (len(annotations)):
          for j in range (len(annotations[i])):
           if j!=0:
            cv2.line(imgcurrent, annotations[i][j-1], annotations[i][j], (0,0,255), 12)
    cv2.line(img, (0, threshhold), (width, threshhold), (0,255,0), 10)
    imgsmall = cv2.resize(img, (ws,hs))
    imgcurrent= cv2.resize(imgcurrent, (1280,720))
    h,w,_ = imgcurrent.shape
    imgcurrent[0:hs, w-ws:w] = imgsmall
    # cv2.imshow('vdo', img)
    cv2.imshow('Presentation', imgcurrent)
    cv2.waitKey(1)