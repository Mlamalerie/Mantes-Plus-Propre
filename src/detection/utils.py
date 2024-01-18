from ultralytics import YOLO
import cv2
import numpy as np
import io
import base64
# list of all models (key and filename)
AVAILABLE_YOLO_MODELS = {
    "yolov8n (coco)" : "yolov8n.pt",
    "yolov8s (taco)" : "best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt",
}

# avaible models
def get_available_models():
    return {
        "models": list(AVAILABLE_YOLO_MODELS.keys()),
        "default_model": "yolov8s (coco)"
    }

# load models from name
def load_model(model_name):
    if model_name not in AVAILABLE_YOLO_MODELS:
        raise ValueError(f"Model {model_name} not available. Available models are: {list(AVAILABLE_YOLO_MODELS.keys())}")

    model_path = "weights/" + AVAILABLE_YOLO_MODELS[model_name]
    model_path = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\src\weights\best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt"
    print(f"Loading model from {model_path}")
    model = YOLO(model_path)

    return model

# launch detection on image (array)
def run_detection_from_array(bgr_image_array : np.ndarray, model : YOLO, confidence_threshold : float = 0.5, xp_name : str = "detect"):

    output_dir = ".inference"
    detections = model(bgr_image_array, conf=confidence_threshold, save=True, save_crop=True, project=output_dir, name=xp_name)
    # Retournez les résultats de la détection
    if len(detections) == 0:
        print(">>>> No detections found.")
        return None
    elif len(detections) > 1:
        raise ValueError(f"More than one detection found. Please check the code and output directory {output_dir}.")

    print(">>>> Detection found.", detections[0])
    return detections[0], detections[0].save_dir



# Fonction pour dessiner les boîtes englobantes sur l'image





