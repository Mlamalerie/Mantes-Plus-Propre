import streamlit as st
from PIL import Image

logo_path = "./assets/logo.png"
page_logo = Image.open(logo_path)
st.set_page_config(
    page_title="Mantes + Propre",
    page_icon=page_logo,
    initial_sidebar_state="expanded",

)

st.title("A propos de Mantes + Propre")

st.subheader("Contexte et motivation")

col1, col2 = st.columns([0.6, 0.4])

col1.write("""La ville de Mantes-la-Jolie est confrontée à un défi environnemental significatif en raison de la prolifération des déchets sauvages. Ces déchets constituent une source majeure de pollution visuelle et environnementale, dégradant la beauté et la salubrité de la ville. """)
col1.write("""> Dans le cadre d'un challenge national : KESK'IA, nous avons décidé de relever ce défi en proposant une solution innovante pour lutter contre les déchets sauvages. """)
col1.write("""
L'objectif de notre projet est de mettre en œuvre une solution innovante utilisant le machine learning pour identifier, classifier et cartographier ces déchets, facilitant ainsi leur gestion par les services municipaux et améliorant la propreté urbaine.
""")
col2.image("assets/pretty_mantes.png", caption="Vue de Mantes-la-Jolie, by @prettymaps")

st.subheader("Notre Equipe")
# Mlamali, Cecilia, Hajar, Nelly, Jallal
st.write("""
- Cecilia, Chef de projet
- Hajar, Assistant chef de projet
- Mlamali, Data Scientist / ML Engineer
- Nelly, Data Analyst / Data Engineer
- Jallal, Data Scientist
""")

st.divider()







