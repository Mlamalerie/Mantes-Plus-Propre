from ultralytics import YOLO

model_path = "../weights/yolov8n.pt"
#model_path = "../weights/best yolov8s [taco-yolo-format train-4066-val-718 20231218_18, epochs=100] 20231223_0024.pt"

model = YOLO(model_path)

bool_camera = False
input_image_path = "../../images_demo/egoblur_demo/mantes (18).jpg"
# get full path
import os
input_image_path = os.path.abspath(input_image_path)

results = model(input_image_path if not bool_camera else "0", project="inference", name="detect")

for i, box_det in enumerate(results[0].boxes):
    print(f"Detection {i}: {box_det}")

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

