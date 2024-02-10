from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO('yolov8n.pt')

# Load and resize the image
image_path = r'C:\Users\mraja\Downloads\non-recycle image\openCv\palm\imagw\download (3).jpg'
original_image = cv2.imread(image_path)
height, width, _ = original_image.shape

# Resize the image to make it bigger (e.g., doubling its size)
new_size = (width * 4, height * 4)
resized_image = cv2.resize(original_image, new_size)

# Run YOLO on the resized image
result = model(resized_image, show=True)

# Wait for a key press
cv2.waitKey(0)
