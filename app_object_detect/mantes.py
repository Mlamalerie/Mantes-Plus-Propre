import folium
import pandas as pd

# Charger les données depuis le fichier CSV
file_path = 'Mantes_la_Jolie_Coordinates.csv'
data = pd.read_csv(file_path)

# Créer une carte centrée autour de Mantes-la-Jolie
mantes_la_jolie_map = folium.Map(location=[48.9907, 1.7102], zoom_start=13)

# Ajouter les points à la carte
for idx, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Point {idx+1}: ({row['Latitude']}, {row['Longitude']})"
    ).add_to(mantes_la_jolie_map)

# Sauvegarder la carte en tant que fichier HTML
map_file = 'Mantes_la_Jolie_Map.html'
mantes_la_jolie_map.save(map_file)

print(f"La carte a été sauvegardée en tant que {map_file}. Vous pouvez l'ouvrir avec un navigateur web.")
