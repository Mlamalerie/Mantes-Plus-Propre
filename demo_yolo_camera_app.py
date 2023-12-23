import streamlit as st
import cv2
from ultralytics import YOLO


#model_path = 'yolov8s.pt'
model_path = "ai/yolo_models/best yolov8s [taco-yolo-format train-4066-val-718 20231218_18, epochs=100] 20231223_0024.pt"
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
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break