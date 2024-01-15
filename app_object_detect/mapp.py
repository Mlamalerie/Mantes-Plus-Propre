import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Paramètres de l'API Baserow
api_url = 'https://api.baserow.io/api/database/rows/table/234485/?user_field_names=true'
api_key = 'TdUiddzmMMlNF1yCdHCGu15DBIZFknp7'

# Fonction pour récupérer les données de Baserow
def get_baserow_data(api_url, api_key):
    headers = {"Authorization": f"Token {api_key}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erreur lors de la récupération des données de Baserow")

# Fonction principale pour créer la carte
def mapp():
    st.title('Carte des déchets sauvages')
    
    try:
        data = get_baserow_data(api_url, api_key)['results']
        m = folium.Map(location=[48.9907, 1.7102], zoom_start=13)

        for item in data:
            lat = item.get('Latitude')
            long = item.get('Longitude')
            photo_url = item['photo'][0]['url'] if item.get('photo') else None
            date = item.get('capture_date')
            status = item.get('status', {}).get('value', 'Statut inconnu')
            description = item.get('description', 'Pas de description')

            if lat and long and photo_url and date and status and description:
                popup_html = f"""
                    <div>
                        <img src="{photo_url}" width="150" height="100" style="display:block;margin:auto;"><br>
                        <b>Date de capture:</b> {date}<br>
                        <b>Status:</b> {status}<br>
                        <b>Description:</b> {description}
                    </div>
                """
                iframe = folium.IFrame(popup_html, width=200, height=250)
                popup = folium.Popup(iframe, max_width=300)
                folium.Marker([lat, long], popup=popup).add_to(m)

        folium_static(m)

    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")


