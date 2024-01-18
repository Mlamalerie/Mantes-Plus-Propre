import streamlit as st
import ultralytics.engine.results
from PIL import Image
import base64
import requests
import io
import os
import cv2
import numpy as np
from src.detection.utils import run_detection_from_array
from src.detection.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI
from src.detection.utils import get_available_models, load_model, AVAILABLE_YOLO_MODELS
from PIL import Image, ImageOps, ImageDraw, ImageFont

# SESSION STATE
# image uploaded
if "uploaded_image" not in st.session_state:
    st.session_state["uploaded_image"] = None
# model selected
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = get_available_models()["default_model"]


# load model cache
#@st.cache_resource(show_spinner=True) #todo
def load_model_cache(model_name="yolov8s"):
    return load_model(model_name)


# Fonction pour dessiner les boîtes englobantes sur l'image
BBOX_COLOR = "magenta"
OVERWRITE = True
N_JOBS = 4


def draw_bboxes_on_image(image_array, bboxes: ultralytics.engine.results.Boxes, bbox_format='xyxy', font_size=60,
                         bbox_color=BBOX_COLOR, bbox_thickness=12,
                         square_size=None):
    img = Image.fromarray(image_array)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(font_size)

    #font = ImageFont.truetype(
    #    font='font/FiraMono-Medium.otf',
    #    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    #thickness = (image.size[0] + image.size[1]) // 300


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


# Streamlit UI
st.title("Détection d'objets avec YOLO")

# Sélect input
st.sidebar.title("Sélection du modèle")
available_models = get_available_models()["models"]
selected_model = st.sidebar.selectbox("Choisissez un modèle", available_models)
confidences_threshold = st.sidebar.slider("Confidence threshold", min_value=0.1, max_value=1.0, value=0.3, step=0.1)

# today date str
from datetime import datetime

YYYYMMDD = datetime.now().strftime("%Y-%m-%d")

# Téléchargement de l'image
uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and uploaded_file != st.session_state["uploaded_image"]:

    image = Image.open(uploaded_file)
    image_name = uploaded_file.name
    st.image(image, caption='Image téléchargée', use_column_width=True)
    st.session_state["uploaded_image"] = image
    st.session_state["image_name"] = image_name

    if st.button('Détecter'):
        # Chargement du modèle
        model = load_model_cache(selected_model)
        # Affichage d'un message de chargement
        with st.spinner('Modèle en cours d’exécution...'):
            # Convertir l'image PIL en un array NumPy pour le traitement avec YOLO/OpenCV
            image_np = np.array(Image.open(uploaded_file))
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            # Exécution de la détection à partir de l'array
            output_detections, save_dir = run_detection_from_array(image_np, model, confidence_threshold=confidences_threshold,
                                                                   xp_name=f"{YYYYMMDD}/{image_name}")

            st.success(f'Voir le dossier {save_dir} pour les résultats.', icon="🎉")
            # Nombre de détections
            n_detected = len(output_detections.boxes)
            output_image_path = os.path.join(save_dir, "image0.jpg")

            # Charger l'image avec OpenCV
            output_image = Image.open(output_image_path)

            # Afficher l'image avec Streamlit
            st.image(output_image, caption=f"Image avec {n_detected} détections", use_column_width=True)