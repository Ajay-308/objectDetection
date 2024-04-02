import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def main():
    st.title("Image Processing App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Convert image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Display the original image
        st.image(image, caption="Original Image", use_column_width=True)

        # Image processing options
        option = st.sidebar.selectbox("Choose an option", ["Original", "Grayscale", "Binary", "Brightness & Contrast", "Annotation"])

        if option == "Original":
            st.image(image, caption="Original Image", use_column_width=True)
        elif option == "Grayscale":
            grayscale_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            st.image(grayscale_image, caption="Grayscale Image", use_column_width=True)
        elif option == "Binary":
            threshold = st.slider("Threshold", 0, 255, 128)
            _, binary_image = cv2.threshold(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY), threshold, 255, cv2.THRESH_BINARY)
            st.image(binary_image, caption="Binary Image", use_column_width=True)
        elif option == "Brightness & Contrast":
            brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
            adjusted_image = cv2.convertScaleAbs(opencv_image, alpha=contrast, beta=brightness)
            st.image(adjusted_image, caption="Adjusted Image", use_column_width=True)
        elif option == "Annotation":
            st.subheader("Draw on Image:")

            # Hand tracking using Mediapipe
            with mp_hands.Hands(static_image_mode=False, max_num_hands=1) as hands:
                results = hands.process(opencv_image)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(opencv_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
            st.image(opencv_image, use_column_width=True, caption="Annotated Image")

if __name__ == "__main__":
    main()
