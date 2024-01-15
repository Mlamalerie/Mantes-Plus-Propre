import requests
import pandas as pd

api_url = 'https://api.baserow.io/api/database/rows/table/234485/?user_field_names=true'
api_key = 'TdUiddzmMMlNF1yCdHCGu15DBIZFknp7'
pd.set_option('display.max_columns', None)

def get_baserow_data(api_url, api_key):
    headers = {"Authorization": f"Token {api_key}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        # Supposons que les données sont stockées dans une clé 'results'
        if 'results' in data:
            df = pd.DataFrame(data['results'])
        else:
            df = pd.DataFrame(data)  # Si les données ne sont pas dans 'results'

        print("Données récupérées :", df)
        return df
    else:
        raise Exception("Erreur lors de la récupération des données de Baserow")

df = get_baserow_data(api_url, api_key)
