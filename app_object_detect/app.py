import streamlit as st
from object_detect import object_detect
import json
from mapp import mapp
from home import home
from sensibilisation import sensibilisation


# css
# Chemin vers votre fichier CSS
#css_file = 'path/to/css_file.css'
logo_path = 'assets/logo.png'
st.sidebar.image(logo_path, use_column_width=True)

st.sidebar.title('Navigation vers les pages')
page = st.sidebar.radio('Choisir une page', ['Accueil','Détection Objets', 'Mapping Objets', 'Sensibilisation'])

# Chargement de la clé API depuis config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    api_key = config['API_KEY_OPENAI'] 


if page == 'Accueil':
    home()
elif page == 'Détection Objets':
    object_detect()
elif page == 'Mapping Objets':
    mapp()
elif page == 'Sensibilisation':
    sensibilisation()


