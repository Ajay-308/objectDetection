import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0 
while True:
    success, img = cap.read()
    cTime= time.time()
    fps = 1/(pTime-cTime)
    pTime = cTime
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    
    result = hands.process(imgRGB)
     
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms , mpHands.HAND_CONNECTIONS)
            landmarks= handLms.landmark
            for id,landmarks in enumerate(landmarks):
                h , w ,c = img.shape
                x = int(landmarks.x * w)
                y = int(landmarks.y* h)
               # print(id,x,y)
                if id == 8:
                    cv2.circle(img=img, center=(x,y), radius=5 , color=(255,0,0), thickness=4)
            

    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN ,1 , (255,0,0) ,2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break






cap.release()
cap.destroyAllWindows()