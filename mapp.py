import streamlit as st
import requests
import pandas as pd
import json
import folium
from tqdm import tqdm
from streamlit_folium import folium_static

api_url = 'https://api.baserow.io/api/database/rows/table/234485/?user_field_names=true'
api_key = 'TdUiddzmMMlNF1yCdHCGu15DBIZFknp7'

# connexion à baserow.io
def get_baserow_data(api_url, api_key):
    headers = {"Authorization": f"Token {api_key}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erreur lors de la récupération des données de Baserow")


st.title('Carte des déchets sauvages')


data = get_baserow_data(api_url, api_key)['results']
st.dataframe(pd.DataFrame(data))
m = folium.Map(location=[48.9900, 1.7200], zoom_start=14)  # Remplacez par vos propres coordonnées
folium_static(m)

for idx, point in tqdm(enumerate(data)):
    if not point['photo']:
        continue

    image_url = point['photo'][0]["thumbnails"]["small"]["url"] # card_cover
    st.write(image_url)

    iframe = folium.IFrame('<img src="{}" style="width:100%;">'.format(image_url),width=100, height=100)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker([point['lat'], point['long']], popup=popup).add_to(m)







