from io import BytesIO
import streamlit as st
import requests
import numpy as np
from src.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI, BULKY_WASTE_IDXS, CATIDX_2_FR_SUPERCATNAME
from PIL import Image
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.db.baserow_db import DechetsTable as DB_manager, TABLE_ID_REAL
from streamlit_js_eval import get_geolocation, set_cookie, get_cookie
import base64

###################################################
# PAGE CONFIG and SIDEBAR #########################
###################################################

logo_path = "./assets/logo.png"
page_logo = Image.open(logo_path)
st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=page_logo,
    initial_sidebar_state="expanded",
)

st.sidebar.success(
    """
    Ceci est une version **beta** de l'application.
    """
)
# ===============
# SESSION STATE
# ===============


if "user_img_file" not in st.session_state:
    st.session_state["user_img_file"] = None


def clear_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]


# ===============
# CONSTANTES
# ===============

PRED_CONFIDENCES_THRESHOLD = 0.15
YYYYMMDD = datetime.now().strftime("%Y-%m-%d")
BASE_DIR = Path(__file__).resolve(strict=True).parent

# base d'adresse pour l'api
# API_BASE_URL = "http://localhost:8080"
# API_BASE_URL = "http://mpp-api:8080"
API_BASE_URL = "https://mpp-mantes-api-ddlzhsitgq-ew.a.run.app"


###################################################
# FUNCTIONS #######################################
###################################################


def init_get_location():
    if 'getLocation()' not in st.session_state:
        st.info("Autorisez la géolocalisation pour pouvoir récupérer votre position.",
                icon="🗺️")
        location = get_geolocation()
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

debug_expander = st.expander("   ")
try:
    r_test_api = requests.get(API_BASE_URL)
except Exception as e:
    st.error(f"Erreur lors de la vérification de l'API: {e}")

with debug_expander:
    st.write(f"API: {API_BASE_URL}")

    st.write(st.session_state)

_, col_logo, _ = st.columns([0.45, 0.1, 0.45])
col_logo.image(page_logo, use_column_width=True)
st.write("<h1 align='center'> <b> Mantes + Propre </b> </h1>", unsafe_allow_html=True)

# Description enrichie
st.markdown("""
<p style='text-align: center;'>Bienvenue sur <b>Mantes + Propre</b>, l'application dédiée pour la propreté de la ville de Mantes-la-Jolie. 🌳🚮</p>
<p style='text-align: center;'>Notre mission est simple mais ambitieuse : détecter tous les déchets sauvages dans la ville et les signaler pour qu'ils soient ramassés,
contribuant ainsi à une ville plus propre et plus verte. 🌐💚</p>
""", unsafe_allow_html=True)

st.divider()
print(st.session_state)
st.markdown("""
<h3 style='text-align: center; color: green;'>🔍 Oh... J'ai trouvé un déchet ! 📸</h3>
<p align='center'> Vous vous promenez dans la ville et vous trouvez un déchet ? Prenez une photo et téléchargez-la ici. Nous nous occuperons de la détecter et de l'ajouter à la carte des déchets sauvages. </p>""",
            unsafe_allow_html=True)


main_container = st.container(border=True)
# Téléchargement de l'image
cols_upload = main_container.columns([0.2, 0.8])
camera_file = cols_upload[0].camera_input("Prendre une photo")
uploaded_file = cols_upload[1].file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
user_img_file = None
# si pas de photo prise ou téléchargée, et pas de photo déjà téléchargée (session state)

# si photo prise
if camera_file is not None or uploaded_file is not None:
    user_img_file = camera_file if camera_file is not None else uploaded_file
# si photo déjà téléchargée (session state)
elif st.session_state["user_img_file"] is not None:
    user_img_file = st.session_state["user_img_file"]
else:
    st.stop()



col1, col2 = st.columns([0.42, 0.58])

orig_image = Image.open(user_img_file)
# st.write(type(uploaded_file.getvalue()))
col1.image(orig_image, caption='Image téléchargée', use_column_width=True)
st.session_state["user_img_file"] = user_img_file
# active
active_description = col1.checkbox("Ajouter un message (optionnel)", value=True)

if active_description:
    description = col1.text_input("Que voyez-vous sur cette photo ?")
launch_detection = col1.button('📷 Faire un signalement !', use_container_width=True, type="primary")

# todo verify si l'image est dans la BDD (load manager avec cache)

if launch_detection:

    # 1. LANCER LA DETECTION
    with st.spinner('Détection en cours d’exécution (cela peut prendre quelques sec)...'):
        r_detections = requests.post(f"{API_BASE_URL}/detect/image?confidence={PRED_CONFIDENCES_THRESHOLD}",
                                     files={"file": user_img_file.getvalue()})

    if r_detections.status_code != 200:
        st.error(f"Erreur lors de la détection: {r_detections.status_code} {r_detections.reason}")
        st.stop()

    r_detections_json = r_detections.json()
    n_detected = r_detections_json["count"]
    if n_detected == 0:
        col2.error(f'Aucun déchets trouvés.', icon="☹️")
        st.stop()

    # st.success(f'{n_detected} détection(s) trouvée(s) !', icon="😊")
    # Afficher l'image avec les détections
    encoded_output_image = r_detections_json["image"]
    # base64 to bytes
    decoded_output_image = base64.b64decode(encoded_output_image)

    output_image = Image.open(BytesIO(decoded_output_image))
    col2.image(output_image, caption=f"Image avec {n_detected} détections", use_column_width=True)

    # Afficher les détections
    df_detections = pd.DataFrame(r_detections_json["detections"])
    df_detections["cls"] = df_detections["cls"].astype(int)
    df_detections["cat_name"] = df_detections["cls"].map(CATIDX_2_FR_CATNAME)
    df_detections["supercat_name"] = df_detections["cls"].map(CATIDX_2_FR_SUPERCATNAME)
    df_detections["is_bulky"] = df_detections["cls"].isin(BULKY_WASTE_IDXS)
    debug_expander.dataframe(df_detections)

    df_detections_supercat_counts = df_detections.groupby("supercat_name").agg({"xywh": "count"}).reset_index()
    df_detections_supercat_counts = df_detections_supercat_counts.rename(columns={"xywh": "count"})
    df_detections_supercat_counts = df_detections_supercat_counts.sort_values("count", ascending=False)
    debug_expander.dataframe(df_detections_supercat_counts)

    df_detections_cls_counts = df_detections.groupby("cls").agg(
        {"xywh": "count", "conf": "mean", "is_bulky": "first", "cat_name": "first",
         "supercat_name": "first"}).reset_index()
    df_detections_cls_counts = df_detections_cls_counts.rename(columns={"xywh": "count", "conf": "mean_conf"})
    # df_detections_cls_counts = df_detections_cls_counts.sort_values("count", ascending=False)
    debug_expander.dataframe(df_detections_cls_counts)

    # count * is_bulky
    n_bulky = (df_detections_cls_counts["count"] * df_detections_cls_counts["is_bulky"]).sum()

    # display list of detections
    # > {count_supercat_name} {supercat_name}
    #    * `count` 'cat_name' emoji
    list_detection_text = ""
    plurial_str = "(s)" if n_detected > 1 else ""
    with st.expander(
            f"Au moins **{n_detected} déchet{plurial_str}** trouvé{plurial_str}, dont {n_bulky} encombrant{plurial_str}."):
        for i, row_super in df_detections_supercat_counts.iterrows():
            list_detection_text += f"* `{row_super['count']}` {row_super['supercat_name']} \n"
            for j, row in df_detections_cls_counts[df_detections_cls_counts["supercat_name"] == row_super[
                "supercat_name"]].iterrows():
                list_detection_text += f"    * `{row['count']}` {row['cat_name']} {CATIDX_2_EMOJI[row['cls']]} \n"

        st.markdown(list_detection_text)

    # 2. ENVOIE A LA BDD
    # 2.1. Récupérer les coordonnées GPS

    longitude, latitude = 1.6919780441680976, 48.99566235430435
    # add noise
    distance_max = 0.001
    longitude += np.random.uniform(-distance_max, distance_max)
    latitude += np.random.uniform(-distance_max, distance_max)

    st.sidebar.info(f"{latitude}, {longitude} [DEBUG]", icon="📍")
    # 2.2. Ajouter les données à la carte



    with st.spinner("🛢️ Enregistrement de votre photo dans notre base de données..."):
        dechets_db_manager = DB_manager(table_id=TABLE_ID_REAL)
        response = dechets_db_manager.add_dechet_row(image=decoded_output_image,
                                                     cat_idx_occurences=df_detections_cls_counts.set_index("cls")[
                                                         "count"].to_dict(),
                                                     longitude=str(longitude),
                                                     latitude=str(latitude),
                                                     generate_description=False,
                                                     verbose=True)

    if "id" not in response or response is None:
        st.error(f"Erreur lors de l'ajout à la base de données: {response.status_code} {response.reason}", icon="☹️")
        st.stop()
    else:
        st.balloons()
        st.success(f"Votre photo a bien été ajoutée à la base de données !", icon="😊")
        st.info("Vous pouvez dès à présent consulter la carte des déchets sauvages pour voir votre photo.", icon="🗺️")


        # clear session state and all
        # clear_session_state()

        # wait 2 seconds and reload page
        # with st.spinner("Rechargement de la page..."):
