import streamlit as st
from openai import OpenAI
import json
import requests

file_path = "texte.txt"
# Chargement de la clé API depuis config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    api_key_openai = config['API_KEY_OPENAI']

# Initialisation du client OpenAI
client = OpenAI(api_key=api_key_openai)

# Fonction pour lire le fichier et extraire les paragraphes
def read_paragraphs(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        paragraphes = content.split('###')[1:]  # Ignore le premier élément vide
        return [p.strip() for p in paragraphes]

# Fonction pour générer une image avec l'API DALL-E
def generate_image(paragraphe, api_key):
    response = client.images.generate(
        model="dall-e-3",
        prompt=paragraphe,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    if response.status_code == 200:
        return response.data[0].url  # Retourne l'URL de l'image générée
    else:
        st.error("Erreur lors de la génération de l'image: " + str(response.status_code))
        return None

# Fonction principale pour traiter le fichier TXT et générer des images
def sensibilisation():
    st.title('Générateur d\'images pour la sensibilisation avec DALL-E')

    # Lire le fichier de texte et le diviser en paragraphes
    paragraphes = read_paragraphs('texte.txt')

    # Sélectionner un paragraphe
    paragraphe_choisi = st.selectbox("Choisissez un paragraphe", paragraphes)

    # Bouton pour déclencher la génération d'image
    if st.button('Générer une image'):
        image_url = generate_image(paragraphe_choisi, api_key)
        if image_url:
            st.image(image_url)
