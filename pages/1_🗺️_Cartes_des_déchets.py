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

###################################################
# PAGE CONFIG and SIDEBAR #########################
###################################################

st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=None,
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
        print(value, type(value))
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

debug_expander = st.expander("Debug")
st.title('Carte des déchets sauvages')
# description longue de la carte
st.markdown("""Retrouvez sur cette carte **les déchets sauvages** signalés par les citoyens de **Mantes-la-Jolie**.""")

display_demo_map = st.sidebar.selectbox("Data", ["Données réelles", "Données de démo"],
                                        help="Les données de démo sont des données générées aléatoirement.", index=1)
map_type_select = st.sidebar.selectbox("Type de carte",
                                       ["Carte", "Carte cluster", "Carte de chaleur", "Carte de chaleur avec temps"])

with st.spinner("Chargement des données..."):
    if display_demo_map == "Données de démo":
        data = load_data(table_id=TABLE_ID_DEMO)
    else:
        data = load_data(table_id=TABLE_ID_REAL)
    len_data = len(data)

if len_data == 0:
    st.warning("Aucun déchet n'a été signalé pour le moment.")
    st.stop()

filtres_expander = st.expander("Filtres")

with st.spinner("Traitement des données..."):
    df_data = pd.json_normalize(data)
    # process data
    # df_data['capture_date'] = pd.to_datetime(df_data['capture_date'])

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

    options_status: list = df_data['status.value'].unique().tolist()

    status_filter = filtres_expander.multiselect("Filtrez par status",
                                   options_status, default=options_status, help="Filtrez les déchets par status.")
    supercat_name_filter = filtres_expander.multiselect(
        f"Sélectionnez les déchets à afficher, parmi {len(FR_SUPERCATNAME_2_EN_SUPERCATNAME)} super catégories",
        list(FR_SUPERCATNAME_2_EN_SUPERCATNAME.keys()), default=list(FR_SUPERCATNAME_2_EN_SUPERCATNAME.keys()),
        help="Filtrez les déchets par type.")
    if len(status_filter) > 0 and len(status_filter) < len(options_status):
        df_data = df_data[df_data['status.value'].isin(status_filter)]

# display many kpi
col_kpi1, col_kpi2, col_kpi3, col_kpi4, _ = st.columns([0.15, 0.15, 0.15, 0.15, 0.3])

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
        if map_type_select == "Carte de chaleur":
            HeatMap(data=df_data[['latitude', 'longitude']].values.tolist(), radius=15, blur=20, min_opacity=0.5,
                    max_zoom=1).add_to(m)


        elif map_type_select == "Carte cluster" or map_type_select == "Carte":
            m_ = MarkerCluster().add_to(m) if map_type_select == "Carte cluster" else m
            progress_text = "Génération de la carte... Attention, cela peut prendre du temps."
            my_bar = st.progress(0, text=progress_text)
            for i, row_item in df_data.iterrows():
                id_ = row_item['id']
                lat = row_item['latitude']
                long = row_item['longitude']
                photo_url = row_item['photo'][0]['url'] if len(row_item['photo']) > 0 else None
                date = row_item['capture_date']
                status = row_item['status.value']
                status_color = row_item['status.color']
                description = row_item['description']
                if 'cat_idx_occurences' in row_item:
                    try:

                        cat_idx_occurences = eval(row_item['cat_idx_occurences'])
                    except:
                        cat_idx_occurences = {}
                    else:
                        cat_idx_occurences = {int(k): int(v) for k, v in cat_idx_occurences.items()}

                sum_cat_idx_occurences = sum(cat_idx_occurences.values())
                if lat is None or long is None:
                    continue
                h4_text = f"{sum_cat_idx_occurences} déchet(s) détecté(s)"

                # crop image to square, 150px
                popup_html = f"""<div>
                                        <img src="{photo_url}" width="150" height="100" style="display:block;margin:auto;"><br>
                                        <b>Date de capture:</b> {date}<br>
                                        <b>Status:</b> {status}<br>
                                        <b>Description:</b> {description}
                                    </div>
                                """

                iframe = folium.IFrame(popup_html, width=200, height=250)
                popup = folium.Popup(iframe, max_width=300)
                # todo : UserWarning: color argument of Icon should be one of: {'purple', 'black', 'pink', 'darkgreen', 'beige', 'orange', 'darkpurple', 'darkblue', 'lightgray', 'lightblue', 'blue', 'lightgreen', 'red', 'lightred', 'cadetblue', 'darkred', 'white', 'gray', 'green'}
                icon = folium.Icon(color=status_color, icon='trash')
                folium.Marker([lat, long], popup=popup, icon=icon).add_to(m_)
                my_bar.progress(i / len_data)
            my_bar.empty()

    folium_static(m, width=None, height=600)
