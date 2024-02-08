import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from src.db.baserow_db import DechetsTable as DB_manager
from src.db.baserow_db import TABLE_ID_REAL, TABLE_ID_DEMO
import pandas as pd
from folium.plugins import MarkerCluster
from src.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI, BULKY_WASTE_IDXS, CATIDX_2_FR_SUPERCATNAME, \
    FR_SUPERCATNAME_2_EN_SUPERCATNAME
from PIL import Image

###################################################
# PAGE CONFIG and SIDEBAR #########################
###################################################
logo_path = "./assets/logo.png"
page_logo = Image.open(logo_path)
st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=page_logo,
    initial_sidebar_state="expanded",
    layout="wide",
)


###################################################
# SESSION #########################################
###################################################


###################################################
# FUNCTIONS #######################################
###################################################


# Fonction pour récupérer les données de Baserow
@st.cache_data
def load_data(table_id: int):
    db_manager = DB_manager(table_id=table_id)
    data = db_manager.get_list_all_rows()
    return data


def eval_cat_idx_occurences(value):
    try:
        #print(value, type(value))
        cat_idx_occurences = eval(value)

    except:
        cat_idx_occurences = {}
    else:
        cat_idx_occurences = {int(k): int(v) for k, v in cat_idx_occurences.items()}
    return cat_idx_occurences


###################################################
# VARS ############################################
###################################################


###################################################
# MAIN ############################################
###################################################

debug_expander = st.expander("   ")
st.title('Carte des déchets sauvages')
# description longue de la carte
st.markdown("""Retrouvez sur cette carte **les déchets sauvages** signalés par les citoyens de **Mantes-la-Jolie**.""")

display_demo_map = st.sidebar.selectbox("Data", ["Données réelles", "Données de démo"],
                                        help="Les données de démo sont des données générées aléatoirement.", index=1)
map_type_select = st.sidebar.selectbox("Type de carte",
                                       ["Base", "Heatmap (Carte de chaleur)", "Carte cluster"])

with st.spinner("Chargement des données..."):
    if display_demo_map == "Données de démo":
        data = load_data(table_id=TABLE_ID_DEMO)
    else:
        data = load_data(table_id=TABLE_ID_REAL)


if len(data) == 0:
    st.warning("Aucun déchet n'a été signalé pour le moment. La carte sera vide.")
    st.stop()

filtres_expander = st.expander("Filtres")

with st.spinner("Traitement des données..."):
    df_data = pd.json_normalize(data)
    # process data
    df_data['capture_date'] = pd.to_datetime(df_data['capture_date'])
    df_data['capture_date'] = df_data['capture_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # COLOR
    df_data['status.color'] = df_data['status.value'].apply(lambda x: "green" if x == "✅ Déchet Ramassé" else "blue" if x == "📅 Ramassage Planifié" else "black")

    df_data['cat_idx_occurences'] = df_data['cat_idx_occurences'].apply(eval_cat_idx_occurences)
    df_data['sum_cat_idx_occurences'] = df_data['cat_idx_occurences'].apply(
        lambda x: sum(x.values()) if isinstance(x, dict) else 0)
    df_data['n_cat_idx_occurences'] = df_data['cat_idx_occurences'].apply(
        lambda x: len(x.values()) if isinstance(x, dict) else 0)
    df_data['n_bulky'] = df_data['cat_idx_occurences'].apply(
        lambda x: sum([v for k, v in x.items() if k in BULKY_WASTE_IDXS]) if isinstance(x, dict) else 0)

    # cat_idx_occurences -> new column for each cat_idx (1 if present, 0 if not)
    for cat_idx in CATIDX_2_FR_CATNAME.keys():
        df_data[f"cat_idx_{cat_idx}_occurences"] = df_data['cat_idx_occurences'].apply(
            lambda x: x[cat_idx] if isinstance(x, dict) and cat_idx in x.keys() else 0)

    debug_expander.write(df_data)

    options_status: list = ["📍 Déchet Détecté", "📅 Ramassage Planifié", "✅ Déchet Ramassé"]
    # delete "✅ Déchet Ramassé" from options_status
    options_status_cleaned = ["📍 Déchet Détecté", "📅 Ramassage Planifié"]
    debug_expander.write(options_status_cleaned)

    status_filter = filtres_expander.multiselect("Filtrez par status",
                                   options_status, default=options_status_cleaned, help="Filtrez les déchets par status.")
    debug_expander.write(status_filter)
    if len(status_filter) > 0:
        df_data = df_data[df_data['status.value'].isin(status_filter)]
        debug_expander.write("filtered by status")

    #supercat_name_filter = filtres_expander.multiselect(
    #    f"Sélectionnez les déchets à afficher, parmi {len(FR_SUPERCATNAME_2_EN_SUPERCATNAME)} super catégories",
    #    list(FR_SUPERCATNAME_2_EN_SUPERCATNAME.keys()), default=list(FR_SUPERCATNAME_2_EN_SUPERCATNAME.keys()),
    #    help="Filtrez les déchets par type.")
    #debug_expander.write(supercat_name_filter)
    #if len(supercat_name_filter) > 0 and len(supercat_name_filter) < len(FR_SUPERCATNAME_2_EN_SUPERCATNAME):
    #    # if cat_idx_filter is not empty
    #    debug_expander.write("filtered by supercat_name")



# display many kpi
col_kpi1, col_kpi2, col_kpi3, col_kpi4, _ = st.columns([0.15, 0.15, 0.15, 0.15, 0.3])
len_data = len(df_data)
col_kpi1.metric(":camera: Signalements total", len_data, help="Nombre total de signalements (photos) de déchets.")
col_kpi2.metric("Total déchets", df_data['sum_cat_idx_occurences'].sum(),
                help="Nombre total de déchets signalés et présents sur la carte.")
col_kpi3.metric("Déchets encombrants", df_data['n_bulky'].sum(),
                help="Nombre total de déchets encombrants signalés et présents sur la carte.")

map_container = st.container(border=True)
# selection type de carte


with map_container:
    st.markdown("""
            <style>
            iframe {
                width: 100%;
                min-height: 600px;
                height: 100%:
            }
            </style>
            """, unsafe_allow_html=True)
    m = folium.Map(location=[48.9907, 1.7102], zoom_start=13)

    with st.spinner("Génération de la carte de chaleur..."):
        if map_type_select == "Heatmap (Carte de chaleur)":
            HeatMap(data=df_data[['latitude', 'longitude']].values.tolist(), radius=15, blur=20, min_opacity=0.5,
                    max_zoom=1).add_to(m)


        elif map_type_select == "Carte cluster" or map_type_select == "Base":
            m_ = MarkerCluster().add_to(m) if map_type_select == "Carte cluster" else m
            progress_text = "Génération de la carte... Attention, cela peut prendre du temps."
            my_bar = st.progress(0, text=progress_text)
            for i,(idx_row, row_item) in enumerate(df_data.iterrows()):

                id_ = row_item['id']
                lat = row_item['latitude']
                long = row_item['longitude']
                google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{long}"
                photo_url = row_item['photo'][0]['url'] if len(row_item['photo']) > 0 else None
                date = row_item['capture_date']

                status = row_item['status.value']
                status_color = row_item['status.color']
                description = row_item['description']

                is_contain_bulk = True if row_item['n_bulky'] > 0 else False
                if 'cat_idx_occurences' in row_item:
                    try:
                        cat_idx_occurences = row_item['cat_idx_occurences']
                    except:
                        cat_idx_occurences = {}
                    else:
                        cat_idx_occurences = {int(k): int(v) for k, v in cat_idx_occurences.items()}

                sum_cat_idx_occurences = sum(cat_idx_occurences.values())
                if lat is None or long is None:
                    continue
                h4_text = f"{sum_cat_idx_occurences} déchet(s) détecté(s)"

                # ul list of cat_idx_occurences
                cat_idx_occurences_text = "<ul>"
                for cat_idx, count in cat_idx_occurences.items():
                    cat_idx_occurences_text += f"<li>{count} {CATIDX_2_FR_CATNAME[cat_idx]} {CATIDX_2_EMOJI[cat_idx]}</li>"
                cat_idx_occurences_text += "</ul>"

                # crop image to square, 150px
                popup_html = f"""<div>
                                        <h4>{h4_text}</h4>  
                                        <img src="{photo_url}" width="150" height="100" style="display:block;margin:auto;"><br>
                                        <b>Status:</b> {status}<br>
                                        <b>Date de capture:</b> {date}<br>
                                        <b>Types de déchets:</b> {cat_idx_occurences_text}<br>
                                        {'<b>Description:</b><br>' if description else ''} {description or ''} 

                                        <b><a href="{google_maps_url}" target="_blank">Itinéraire Google Maps</a></b>
                                    </div>
                                """

                iframe = folium.IFrame(popup_html, width=225, height=250)
                popup = folium.Popup(iframe, max_width=300)

                if 60 in cat_idx_occurences.keys() or 61 in cat_idx_occurences.keys():
                    icon_name = "trash-can"
                # if 63, 64, 65 ... 68 in cat_idx_occurences.keys():
                elif is_contain_bulk:
                    icon_name = "couch"
                else:
                    icon_name = "recycle"


                icon = folium.Icon(color=status_color, icon=icon_name, prefix="fa")
                folium.Marker([lat, long], popup=popup, icon=icon).add_to(m_)
                my_bar.progress(i / len_data)
            my_bar.empty()

    folium_static(m, width=None, height=600)
