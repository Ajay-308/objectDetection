import cv2
import mediapipe as mp
import time

detect = cv2.VideoCapture(1)

while True:
    success, img = detect.read()

    if not success:
        print("Failed to capture video.")
        break

    cv2.imshow('Image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

detect.release()
cv2.destroyAllWindows()
