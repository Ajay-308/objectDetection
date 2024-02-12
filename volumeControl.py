import cv2
import mediapipe as mp
import time
import numpy as np
import virtual_mouse as vm

# --> defineing webcam height and width
wCam , hCam = 1240 , 640

cap  = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# --> PREVIOUS TIME
pTime =0



while True:
    success ,img = cap.read()
    cTime= time.time()
    fps = 1/(pTime-cTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN ,1 , (255,0,0) ,2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break



#path:volumeControl.py

cap.release()
cap.destroyAllWindows()