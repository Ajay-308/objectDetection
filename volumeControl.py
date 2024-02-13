import cv2
import mediapipe as mp
import time
import numpy as np
import pycaw as caw
import pyautogui
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --> defineing webcam height and width
wCam , hCam = 1240 , 640

cap  = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# --> PREVIOUS TIME
pTime =0
hand_detect = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)

minVol = volRange[0]
maxVol = volRange[1]



while True:
    success ,img = cap.read()
    img = cv2.flip(img,1) # flip the frame horizontally for mirror effect 
    frame_width, frame_height = img.shape[1], img.shape[0] 
    if not success:
        print('Error:Could not get frame')
        break
    # --> for detectiing hand
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert BGR TO RGB
    output = hand_detect.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            draw.draw_landmarks(img,hand,mp.solutions.hands.HAND_CONNECTIONS)
            landmarks= hand.landmark
            # yaha se mai ab index fingure ki tip ki position nikal raha hu 
            for id,landmarks in enumerate(landmarks):
                x = int(landmarks.x * frame_width)
                y = int(landmarks.y* frame_height)
               # print(id,x,y)
                #tip of index fingure is 8

                if id == 8:
                    cv2.circle(img=img, center=(x,y), radius=10 , color=(255,0,255), thickness=-4)

                   # pyautogui.moveTo(x,y) # currently it will move pointer according to box size not my screen size
                    
                    #--> now setting for full screen
                    index_x= int(x *hCam/frame_height)
                    index_y = int(y*wCam/frame_width)

                if id == 4:
                    cv2.circle(img=img, center=(x,y), radius=10 , color=(255,0,255), thickness=-4)
                    thumb_x= int(x *hCam/frame_height)
                    thumb_y = int(y*wCam/frame_width)
            length = math.hypot(thumb_x-index_x, thumb_y-index_y)

            # --> Hand range 50-300
            # --> Volume range -65 -0
            vol = np.interp(length ,[50,300] ,[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            #print(Length, vol)
            print(length,vol)

    cTime= time.time()
    fps = 1/(pTime-cTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN ,1 , (255,0,0) ,2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break



#path:volumeControl.py


cap.release()
cap.detroyAllWindows()