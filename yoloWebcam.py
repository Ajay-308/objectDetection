import cv2
from ultralytics import YOLO
import cvzone
import math

# Create a VideoCapture object with camera index 0
det = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not det.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set the width and height of the video frame
det.set(3, 640)
det.set(4, 480)
model  = YOLO("../palm/yolov8n.pt")

# lets define all classes of object what we are detecting
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
while True:
    # Read a frame from the camera
    ret, img = det.read()
    
    # Check if the frame is read successfully
    if not ret:
        print("Error: Could not read frame.")
        break
    results = model(img , stream=True)
    for r in results:
        boxes= r.boxes
        for box in boxes:
            # -- >this one for openCV
            # x1,y1,x2,y2= box.xyxy[0]
            # x1,y1,x2,y2 = int(x1), int(y1) ,int(x2) ,int(y2)
            # print(x1,y1,x2,y2)
            # cv2.rectangle(img, (x1,y1),(x2,y2), (12,0,125),3)

            #--> this one for cvZone
            x1,y1,x2,y2= box.xyxy[0]  # box bana diya hai
            x1,y1,x2,y2 = int(x1), int(y1) ,int(x2) ,int(y2)
            w,h = x2-x1, y2-y1
            print(x1,y1,w,h)
            cvzone.cornerRect(img,(x1,y1,w,h))

            # here confidence means the probability of the object detected range from 0 to 1
            confidenc= math.ceil((box.conf[0]*100))/100 # 2 decimal point of confidence 
            print(confidenc)
            #img , text ,pos of text ,font, font size ,color of text , thickness of text
            #cv2.putText(img, f'{confidenc}', (max(0,x1),max(40,y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255,0,255),2)

            # here we are getting the class of the object detected
            clas =int(box.cls[0])
            if 0 <= clas < len(classNames):
               cvzone.putTextRect(img, f'{classNames[clas]} {confidenc}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            else:
                print(f"Invalid class index: {clas}, Classes list length: {len(classNames)}")
      
    # Display the frame
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the window
det.release()
cv2.destroyAllWindows()
