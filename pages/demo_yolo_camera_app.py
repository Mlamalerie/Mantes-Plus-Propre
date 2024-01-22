import streamlit as st
import cv2
from ultralytics import YOLO


img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as bytes:
    bytes_data = img_file_buffer.getvalue()
    # Check the type of bytes_data:
    # Should output: <class 'bytes'>
    st.write(type(bytes_data))


st.stop()
#model_path = 'yolov8s.pt'
model_path = "../src/weights/best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt"
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