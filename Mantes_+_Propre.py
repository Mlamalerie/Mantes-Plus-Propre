import streamlit as st
import ultralytics.engine.results
import base64
import requests
from requests.adapters import HTTPAdapter, Retry
import os
import cv2
import numpy as np
from src.detection.utils import run_detection_from_array
from src.detection.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI, BULKY_WASTE_IDXS
from src.detection.utils import get_available_models, load_model, AVAILABLE_YOLO_MODELS
from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.db.baserow_db import DechetsTable as DB_manager
from streamlit_js_eval import get_geolocation, set_cookie, get_cookie
from streamlit_geolocation import streamlit_geolocation
import urllib

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
# ===============
# SESSION STATE
# ===============


if "uploaded_image" not in st.session_state:
    st.session_state["uploaded_image"] = None

# ===============
# CONSTANTES
# ===============

PRED_CONFIDENCES_THRESHOLD = 0.2
YYYYMMDD = datetime.now().strftime("%Y-%m-%d")
BASE_DIR = Path(__file__).resolve(strict=True).parent


###################################################
# FUNCTIONS #######################################
###################################################


def init_get_location():
    if 'getLocation()' not in st.session_state:
        st.info("Autorisez la géolocalisation pour pouvoir récupérer votre position.",
                icon="🗺️")
        location = streamlit_geolocation()
        set_cookie('location', location, 10)
        # st.write("Cookie set")
        st.stop()
    else:
        get_cookie('location')
        longitude = st.session_state['getLocation()']['coords']['longitude']
        latitude = st.session_state['getLocation()']['coords']['latitude']


###################################################
# MAIN ############################################
###################################################
with st.expander("Debug"):
    st.write(st.session_state)
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
# expander debug empty
expander_debug = st.empty()
if uploaded_file is None or uploaded_file == st.session_state["uploaded_image"]:
    st.stop()

col1, col2 = st.columns(2)

image = Image.open(uploaded_file)
image_name = uploaded_file.name
# st.write(type(uploaded_file.getvalue()))
col1.image(image, caption='Image téléchargée', use_column_width=True)
st.session_state["uploaded_image"] = image
st.session_state["image_name"] = image_name

launch_detection = col1.button('📷 Lancer la détection !', use_container_width=True, type="primary")

if launch_detection:

    # 1. LANCER LA DETECTION
    with st.spinner('Modèle en cours d’exécution...'):
        r_detections = requests.post(f"http://localhost:8000/detect/image?confidence={PRED_CONFIDENCES_THRESHOLD}",
                                     files={"file": uploaded_file.getbuffer()})

    if r_detections.status_code != 200:
        st.error(f"Erreur lors de la détection: {r_detections.status_code} {r_detections.reason}")
        st.stop()

    r_detections_json = r_detections.json()
    n_detected = r_detections_json["count"]
    if n_detected == 0:
        col2.error(f'Aucune détection trouvée.', icon="☹️")
        st.stop()

    # st.success(f'{n_detected} détection(s) trouvée(s) !', icon="😊")
    # Afficher l'image avec les détections
    output_image_path = os.path.join(BASE_DIR, r_detections_json["out_image_path"])
    output_image = Image.open(output_image_path)
    col2.image(output_image, caption=f"Image avec {n_detected} détections", use_column_width=True)

    # Afficher les détections
    df_detections = pd.DataFrame(r_detections_json["detections"])
    df_detections["is_bulky"] = df_detections["cls"].isin(BULKY_WASTE_IDXS)
    df_detections_counts = df_detections.groupby("cls").agg(
        {"x1": "count", "conf": "mean", "is_bulky": "first"}).reset_index()
    df_detections_counts = df_detections_counts.rename(columns={"x1": "count", "conf": "mean_conf"})
    df_detections_counts["cls"] = df_detections_counts["cls"].astype(int)

    df_detections_counts = df_detections_counts.sort_values("count", ascending=False)

    # count * is_bulky
    n_bulky = (df_detections_counts["count"] * df_detections_counts["is_bulky"]).sum()

    # display list of detections ( * count cat_name emoji)
    with col2.expander(f"{n_detected} déchets trouvée(s), dont {n_bulky} encombrant(s)."):
        for i, row in df_detections_counts.iterrows():
            cls = row["cls"]
            count = int(row["count"])
            mean_conf = row["mean_conf"]
            emoji = CATIDX_2_EMOJI[cls]
            cat_name = CATIDX_2_FR_CATNAME[cls]
            st.write(f"""- `{count}` '{cat_name}' {emoji}""")

    # 2. ENVOIE A LA BDD
    # 2.1. Récupérer les coordonnées GPS

    longitude, latitude = 48.9833, 1.7167
    # add noise
    longitude += np.random.normal(scale=0.0001)
    latitude += np.random.normal(scale=0.0001)
    # emoji épingle ->
    st.info(f"{longitude}, {latitude} [DEBUG]")
    # 2.2. Ajouter les données à la carte
    with st.spinner("Enregistrement de votre photo dans la base de données 'Mantes + Propre'..."):
        dechets_db_manager = DB_manager(table_id=244285)

        response = dechets_db_manager.add_dechet_row(image=uploaded_file.getvalue(),
                                                     cat_idx_occurences=df_detections_counts.set_index("cls")[
                                                         "count"].to_dict(),
                                                     longitude="0.0",
                                                     latitude="0.0", generate_description=False, verbose=True)

    if "id" not in response or response is None:
        st.error(f"Erreur lors de l'ajout à la base de données: {response.status_code} {response.reason}", icon="☹️")
        st.stop()
    else:
        st.success(f"Votre photo a bien été ajoutée à la base de données ! [id={response['id']}]", icon="😊")
    st.info(f"Vous pouvez la retrouver sur la carte des déchets sauvages de la ville.", icon="🗺️")

## Add some explainer text
