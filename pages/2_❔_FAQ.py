import streamlit as st
from src.category_utils import CATIDX_2_FR_CATNAME, CATIDX_2_EMOJI, BULKY_WASTE_IDXS, CATIDX_2_FR_SUPERCATNAME
from PIL import Image

logo_path = "./assets/logo.png"
page_logo = Image.open(logo_path)
st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=page_logo,
    initial_sidebar_state="expanded",
    layout="wide",
)

st.header("F.A.Q")

with st.expander("C'est quoi un déchet sauvage ?", expanded=True):
    st.write("""
    Un déchet sauvage est un déchet abandonné par un individu dans un lieu public ou privé, sans autorisation du propriétaire du lieu, et sans utiliser les dispositifs mis à disposition pour le tri et la collecte des déchets.
    Cela inclue les emballages, les bouteilles, les canettes, et autres résidus qui ne sont pas correctement disposés dans des poubelles ou des centres de recyclage. 
    """)


with st.expander("Comment fonctionne l'application ?"):
    st.write("""
    L'application est composée de deux parties : 
    - Une partie détection qui permet de détecter les déchets sur une image #todo mettre des gifs
    - Une partie cartographie qui permet de visualiser les déchets détectés sur une carte
    """)

with st.expander("Comment signaler un déchet ?"):
    st.write("""
    Pour signaler un déchet, il suffit de prendre une photo de celui-ci et de la télécharger sur l'application. 
    La photo sera alors analysée par un modèle de machine learning qui détectera le déchet et le signalera sur la carte.
    """)

with st.expander("Quels type de déchets sont détectés ?"):
    txt = "L'application détecte les déchets suivants :"
    for idx, cat_name in CATIDX_2_FR_CATNAME.items():
        txt += f"\n- {cat_name} {CATIDX_2_EMOJI[idx]} ({CATIDX_2_FR_SUPERCATNAME[idx]})"
    st.write(txt)

with st.expander("Comment les données collectées sont-elles utilisées ?"):
    st.write("""
    Les données collectées sont utilisées pour améliorer la détection des déchets et pour aider la ville de Mantes-la-Jolie à mieux gérer ses déchets.
    """)

with st.expander("Puis-je utiliser l'application sans connexion internet ?"):
    st.write("""
    Non, l'application nécessite une connexion internet pour fonctionner.
    """)

with st.expander("L'application est-elle gratuite ?"):
    st.write("""
    Oui, l'application est gratuite.
    """)

with st.expander("Comment l'application contribue-t-elle à la lutte contre la pollution par les déchets ?"):
    st.write("""
    L'application permet de signaler les déchets sauvages à la ville de Mantes-la-Jolie pour qu'elle puisse les ramasser et les recycler. 
    """)





