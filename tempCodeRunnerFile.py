import cv2

# --> read video using cv2
video_read_karle = r'C:\Users\mraja\Downloads\non-recycle image\openCv\object detection\Untitled video - Made with Clipchamp.mp4'
cap = cv2.VideoCapture(video_read_karle)

cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, image = cap.read()

    if not ret:
        print("Error: video not present .")
        break

    win_name = "mera camera"

    # Creating a window with resizable property
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    cv2.imshow(win_name, image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
