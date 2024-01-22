from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw, ImageFont
# list of all models (key and filename)
from pathlib import Path
from ultralytics.engine.results import Boxes
from src.detection.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI
from src.weights.utils import AVAILABLE_YOLO_MODELS
import functools

__version__ = "0.1.0"
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


def draw_bboxes_on_image(image_array, bboxes: Boxes, bbox_format='xyxy', font_size=60,
                         bbox_color="magenta", bbox_thickness=12,
                         square_size=None):
    img = Image.fromarray(image_array)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(font_size)

    # font = ImageFont.truetype(
    #    font='font/FiraMono-Medium.otf',
    #    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    # thickness = (image.size[0] + image.size[1]) // 300

    for box in bboxes:
        if bbox_format == 'xyxy':
            print("..." * 50)
        elif bbox_format == 'xywh':
            raise ValueError(f'Unknown bbox format {bbox_format}')
        elif bbox_format == 'cxcywh':
            raise ValueError(f'Unknown bbox format {bbox_format}')
        else:
            raise ValueError(f'Unknown bbox format {bbox_format}')

        # Extraire les données de la boîte
        xyxy = box.xyxy.cpu().numpy().flatten()  # Aplatir le tableau
        x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]

        cls = int(box.cls.cpu().numpy().item())
        conf = box.conf.cpu().numpy().item()

        emoji = CATIDX_2_EMOJI[cls]
        label = f"{CATIDX_2_FR_CATNAME[cls]} {conf:.2f}"

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline=bbox_color, width=bbox_thickness)

        # Draw text
        space = (font_size * 1.25)
        text_x, text_y = x1, y1 - space
        draw.text((text_x, text_y), label, fill=bbox_color, font=font, width=bbox_thickness)

    if square_size:
        img = ImageOps.pad(img, size=(square_size, square_size), color="black", centering=(0.5, 0.5))

    return img


def draw_boxes(image, result_detections):
    if result_detections.boxes is None:
        return image, []
    for box in result_detections.boxes:
        # Extraire les données de la boîte
        xyxy = box.xywh.cpu().numpy().flatten()  # Aplatir le tableau
        x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]

        cls = int(box.cls.cpu().numpy().item())
        conf = box.conf.cpu().numpy().item()

        emoji = CATIDX_2_EMOJI[cls]
        label = f"{emoji} {CATIDX_2_FR_CATNAME[cls]} {conf:.2f}"

        image = cv2.rectangle(image, (x1, y1, x2, y2), (255, 0, 0), 2)
        image = cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return image, result_detections.boxes
