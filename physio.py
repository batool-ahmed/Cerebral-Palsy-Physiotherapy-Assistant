# Currently this module only works for ELbow Extension Exercise
# We can increase the number of exercises by simply 

import cv2
import time
import numpy as np
import PoseModule as pm


detector = pm.poseDetector()

count = 0
dir = 0

eTime = 0 
normalETime = 1640323861.7450624
cTime = 0
pTime = 0

print(normalETime)

max_count = 15 # on reassesment, the max_count will change

# image acquisition and pre-processing using opencv-python
cameraPort = 0
cap = cv2.VideoCapture(cameraPort, cv2.CAP_DSHOW)

# HD Resolution
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1) #since webcam displays mirror image

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    cTime = time.time()
    pTime = cTime

    if len(lmList) != 0:
        angle = detector.findAngle(img, 12, 14, 16)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))

        eTime = pTime

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
                print(eTime)
                if eTime < normalETime:
                    print("Too Fast")
                eTime = 0

        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)


        if count < max_count:
            cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)) + "/" + str(max_count), (45, 670), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 5)
        else:
            cv2.putText(img, "Complete", (45, 670), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)



    cv2.putText(img, "Elbow Extension Exercise", (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)