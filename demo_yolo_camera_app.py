import streamlit as st
import cv2
from ultralytics import YOLO


#model_path = 'yolov8s.pt'
model_path = "src/weights/best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt"
model = YOLO(model_path)


# Open the camera
cap = cv2.VideoCapture(0)
st_frame = st.empty()
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        #cv2.imshow("YOLOv8 Inference", annotated_frame)

        st_frame.image(annotated_frame, channels='BGR')

        # Break the loop if 'q' is pressed
        #if cv2.waitKey(1) & 0xFF == ord("q"):
        #    break
    else:
        # Break the loop if the end of the video is reached
        break