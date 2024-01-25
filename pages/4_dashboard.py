import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time 
import plotly.express as px 
import numpy as np 
import requests

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

def home():
    st.title('Detection des Dechets - Dashboard')
    st.write('Bienvenue sur l\'application de détection des déchets sauvages de Mantes-La-Jolie.')
        
    # Visualisation des données
    st.write('Real-Time / Live Data Dashboard')
    data = get_baserow_data(api_url, api_key)['results']
    df = pd.DataFrame(data)
    st.markdown("### Detailed Data from Baserow View")
    st.dataframe(df)
    time.sleep(1)