import streamlit as st
import ultralytics.engine.results
import base64
import requests
import os
import cv2
import numpy as np
from src.detection.utils import run_detection_from_array
from src.detection.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI
from src.detection.utils import get_available_models, load_model, AVAILABLE_YOLO_MODELS
from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime

# ===============
# SESSION STATE
# ===============


if "uploaded_image" not in st.session_state:
    st.session_state["uploaded_image"] = None

# ===============
# CONSTANTES
# ===============

PRED_CONFIDENCES_THRESHOLD = 0.25
YYYYMMDD = datetime.now().strftime("%Y-%m-%d")

###################################################
# FUNCTIONS #######################################
###################################################

# load model cache
# @st.cache_resource(show_spinner=True) #todo
def load_model_cache(model_name="yolov8n (coco)"):
    return load_model(model_name)


###################################################
# PAGE CONFIG and SIDEBAR #########################
###################################################

page_logo = Image.open("./assets/logo.ico")
st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=page_logo,
    initial_sidebar_state="expanded",
)

st.sidebar.success(
    """
    This is a **beta** version of the app.
    """
)

###################################################
# MAIN ############################################
###################################################

st.write("<h1 align='center'> <b> Mantes + Propre </b> </h1>", unsafe_allow_html=True)

# Description
st.write(
    "<p align='center'> <b> Mantes + Propre </b> est une application qui permet de détecter les déchets sauvages sur des images et de les localiser sur une carte. </p>",
    unsafe_allow_html=True)

st.divider()

st.markdown("<h4 align='center'> <b> Oh... J'ai trouvé un déchet ! </b> </h2>", unsafe_allow_html=True)
st.write('\n')
st.write(
    "<p align='center'> Vous vous promenez dans la ville et vous trouvez un déchet ? Prenez une photo et téléchargez-la ici. Nous nous occuperons de la détecter et de l'ajouter à la carte des déchets sauvages. </p>",
    unsafe_allow_html=True)
st.write('\n')

# Téléchargement de l'image
uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and uploaded_file != st.session_state["uploaded_image"]:
    col1, col2 = st.columns(2)

    image = Image.open(uploaded_file)
    image_name = uploaded_file.name
    col1.image(image, caption='Image téléchargée', use_column_width=True)
    st.session_state["uploaded_image"] = image
    st.session_state["image_name"] = image_name

    if st.button('Signaler les déchets 📷🗑️'):
        # Chargement du modèle
        model = load_model_cache()
        # Affichage d'un message de chargement
        with st.spinner('Modèle en cours d’exécution...'):
            # Convertir l'image PIL en un array NumPy pour le traitement avec YOLO/OpenCV
            image_np = np.array(Image.open(uploaded_file))
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            # Exécution de la détection à partir de l'array
            output_detections, save_dir = run_detection_from_array(image_np,
                                                                   confidence_threshold=PRED_CONFIDENCES_THRESHOLD,
                                                                   xp_name=f"{YYYYMMDD}/{image_name}")

            # Nombre de détections
            n_detected = len(output_detections.boxes)
            if n_detected > 0:
                st.success(f'Voir le dossier {save_dir} pour les résultats. [DEBUG]', icon="🎉")

                # Afficher l'image avec les détections
                output_image_path = os.path.join(save_dir, "image0.jpg")
                output_image = Image.open(output_image_path)
                col2.image(output_image, caption=f"Image avec {n_detected} détections", use_column_width=True)

            else:
                st.error(f'Aucune détection trouvée.', icon="☹️")

st.divider()

## Add some explainer text
