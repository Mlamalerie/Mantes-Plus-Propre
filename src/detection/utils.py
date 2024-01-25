from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
# list of all models (key and filename)
from pathlib import Path
from src.detection.weights.utils import AVAILABLE_YOLO_MODELS
import functools

__version__ = "2024.01.18"
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
model = None

# load models from name
@functools.cache
def load_model(model_name: str = "yolov8s (mpp)") -> YOLO:
    if model_name not in AVAILABLE_YOLO_MODELS:
        raise ValueError(
            f"Model {model_name} not available. Available models are: {list(AVAILABLE_YOLO_MODELS.keys())}")

    model_path = AVAILABLE_YOLO_MODELS[model_name]
    # model_path = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\src\weights\best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt"
    print(f"> YOLO model loaded from {model_path}")
    model = YOLO(model_path)

    return model


# launch detection on image (array)
def __run_detection_from_array(bgr_image_array: np.ndarray, model: YOLO, confidence_threshold: float = 0.5,
                               xp_name: str = "detect"):
    output_dir = ".inference"
    detections = model(bgr_image_array, conf=confidence_threshold, save=True, save_crop=True, project=output_dir,
                       name=xp_name)
    # Retournez les résultats de la détection
    if len(detections) == 0:
        print(">>>> No detections found.")
        return None
    elif len(detections) > 1:
        raise ValueError(f"More than one detection found. Please check the code and output directory {output_dir}.")

    print(">>>> Detection found.")
    return detections[0], detections[0].save_dir

def run_detection_from_array(bgr_image_array: np.ndarray, confidence_threshold: float = 0.5, xp_name: str = "detect"):
    global model
    if model is None:
        model = load_model()

    return __run_detection_from_array(bgr_image_array, model, confidence_threshold, xp_name)

def read_imagefile(file: bytes) -> np.ndarray:
    image = Image.open(BytesIO(file))
    image_np = np.array(image)
    return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
