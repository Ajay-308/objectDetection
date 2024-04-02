import cv2
import sys
import numpy as np

PREVIEW = 0
BLUR = 1
FEATURES = 2
CANNY = 3

s = 0
if len(sys.argv) > 1:
    s = int(sys.argv[1])

image_filter = PREVIEW
alive = True
win_name = "Camera Filters"

cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

source = cv2.VideoCapture(s)

while alive:
    has_frame, frame = source.read()
    
    if not has_frame:
        break
    
    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 50, 70)  # Adjust threshold values as per requirement
    elif image_filter == BLUR:
        result = cv2.blur(frame, (20, 20))
    elif image_filter == FEATURES:
        result = frame.copy()  # Create a copy to avoid modifying the original frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, 250, 0.01, 10)
        
        if corners is not None:
            corners = np.int0(corners)
            for i in corners:
                x, y = i.ravel()
                cv2.circle(result, (x, y), 5, (0, 0, 255), 2)

    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)

    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR
    elif key == ord("F") or key == ord("f"):
        image_filter = FEATURES
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

source.release()
cv2.destroyAllWindows()
