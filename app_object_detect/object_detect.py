import streamlit as st
from PIL import Image
import cv2
import tempfile
import numpy as np
#from airtable import Airtable
from tqdm import tqdm
import requests
import cloudinary
import cloudinary.uploader

#connexion avec la base de donnees baserow
api_url = 'https://api.baserow.io/api/database/rows/table/234485/?user_field_names=true'
api_key = 'TdUiddzmMMlNF1yCdHCGu15DBIZFknp7'
def get_baserow_data(api_url, api_key):
    headers = {"Authorization": f"Token {api_key}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erreur lors de la récupération des données de Baserow")


def object_detect():
    st.title('Détection de déchets')

    choix = st.radio("Choisissez le mode d'entrée :", ('Uploader une Image', 'Uploader une Vidéo', 'Caméra Vidéo'))

    if choix == 'Uploader une Image':
        uploaded_image = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
           col1, col2 = st.columns(2)
           with col1 : 
                image = Image.open(uploaded_image)
                st.image(image, caption='Image uploadée', use_column_width=True)
                st.button('Cliquez Ici pour Détecter l\'objet')
            # Traitement de détection d'objets
            #if st.button('Détecter l\'objet'):
                # Code pour la détection d'objet sur l'image
            #detect_button = st.button('Cliquez Ici pour Détecter l\'objet')
            # Traitement de détection d'objets
            #if st.button('Détecter l\'objet'):
                # Code pour la détection d'objet sur l'image

    elif choix == 'Uploader une Vidéo':
        uploaded_video = st.file_uploader("Choisissez une vidéo...", type=["mp4", "avi", "mov"])
        if uploaded_video is not None:
            col1, col2 = st.columns(2)
            with col1 :
                #video = Image.open(uploaded_video)
                st.video(uploaded_video, caption='Vidéo Uploadée', use_column_width=True)
            #if st.button('Détecter l\'objet'):
                # Code pour la détection d'objet sur la vidéo

    #elif choix == 'Caméra Vidéo':
        # Code pour la capture vidéo de la caméra
        #if st.button('Détecter l\'objet'):
            # Code pour la détection d'objet à partir de la caméra


    