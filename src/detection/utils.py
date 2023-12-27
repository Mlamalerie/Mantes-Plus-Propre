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
        "default_model": "yolov8s (taco)",
    }

# load models from name
def load_model(model_name):
    if model_name not in AVAILABLE_YOLO_MODELS:
        raise ValueError(f"Model {model_name} not available. Available models are: {list(AVAILABLE_YOLO_MODELS.keys())}")

    model_path = "../weights/" + AVAILABLE_YOLO_MODELS[model_name]
    model = YOLO(model_path)

    return model

# launch detection on image (array)
def run_detection_from_array(image_array : np.ndarray, model : YOLO, confidence_threshold : float = 0.5):
    # Ajoutez ici le code pour charger votre modèle YOLO et exécuter la détection
    # Par exemple, model.detect(image_array)
    # Remplacez la ligne suivante par votre logique de détection
    detections = model(image_array, conf=confidence_threshold)
    # Retournez les résultats de la détection
    return detections[0]

def run_detection_from_base64(encoded_image : str, model : YOLO, confidence_threshold : float = 0.5):
    # 1. Décodez l'image à partir de la chaîne en base64
    decoded_image = base64.b64decode(encoded_image)
    # 2. Exécutez la détection d'objets avec le modèle YOLO
    # 3. Formatez les résultats et renvoyez-les
    return run_detection_from_array(decoded_image, model, confidence_threshold)

# Fonction pour dessiner les boîtes englobantes sur l'image





