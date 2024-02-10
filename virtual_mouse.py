import cv2
import mediapipe as mp
import pyautogui



cap = cv2.VideoCapture(0)
# --> for detection of hands
hand_detect = mp.solutions.hands.Hands()
# --> for drawing the hans landmarks we use this mediapipe

draw = mp.solutions.drawing_utils

# --> for getting the frame of laptop screen we gonna use pyautogui
screen_width, screen_height = pyautogui.size()

# global variable
index_y =0;


while True:
    ret, frame =cap.read()
    frame = cv2.flip(frame,1) # flip the frame horizontally for mirror effect 
    frame_width, frame_height = frame.shape[1], frame.shape[0] 
    if not ret:
        print('Error:Could not get frame')
        break
    # --> for detectiing hand
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert BGR TO RGB
    output = hand_detect.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            draw.draw_landmarks(frame,hand,mp.solutions.hands.HAND_CONNECTIONS)
            landmarks= hand.landmark
            # yaha se mai ab index fingure ki tip ki position nikal raha hu 
            for id,landmarks in enumerate(landmarks):
                x = int(landmarks.x * frame_width)
                y = int(landmarks.y* frame_height)
               # print(id,x,y)
                #tip of index fingure is 8
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=10 , color=(255,0,255), thickness=-4)

                   # pyautogui.moveTo(x,y) # currently it will move pointer according to box size not my screen size
                    
                    #--> now setting for full screen
                    index_x= int(x *screen_height/frame_height)
                    index_y = int(y*screen_width/frame_width)
                    pyautogui.moveTo(index_x,index_y)

                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10 , color=(255,0,255), thickness=-4)
                    thumb_x= int(x *screen_height/frame_height)
                    thumb_y = int(y*screen_width/frame_width)
                    #print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 40:
                        print("clicked")
                        pyautogui.click()
                        




    print(hands)
    cv2.imshow('virtaul mouse', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()

