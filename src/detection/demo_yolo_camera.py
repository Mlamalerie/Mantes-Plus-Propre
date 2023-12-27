from ultralytics import YOLO

#model_path = 'yolov8s.pt'
model_path = "../weights/best yolov8s [taco-yolo-format train-4066-val-718 20231218_18, epochs=100] 20231223_0024.pt"
model = YOLO(model_path)

results = model.predict(source="0", show=True)

print(results)

"""
import cv2
from ultralytics import YOLO



# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the camera
cap = cv2.VideoCapture(0)

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
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
"""

