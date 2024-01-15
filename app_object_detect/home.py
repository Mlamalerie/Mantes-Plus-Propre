import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def home():
    st.header('Page d\'accueil')
    st.write('Bienvenue sur l\'application de détection des déchets sauvages de Mantes-La-Jolie.')
        
    # Visualisation des données
    st.write('Statistiques et informations récentes...')

    meta_data = pd.read_csv('meta_df.csv')

    col1, col2 = st.columns(2)
    col1.metric(label="Nombre de Catégories", value=meta_data['cat_name'].nunique())
    col2.metric(label="Nombre de Supercatégories", value=meta_data['supercategory'].nunique())
    # Histogramme de la Répartition des Catégories
    fig1, ax = plt.subplots()
    meta_data['cat_name'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Répartition des Catégories')
    ax.set_xlabel('Catégorie')
    ax.set_ylabel('Fréquence')
    #st.pyplot(fig1)
    
    # Histogramme de la Répartition des Super-Catégories
    fig2, ax = plt.subplots()
    meta_data['supercategory'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Répartition des Super-Catégories')
    ax.set_xlabel('Super-Catégorie')
    ax.set_ylabel('Fréquence')
    #st.pyplot(fig2)

    #Boîte à Moustaches des Dimensions des Images
    fig3, ax = plt.subplots()
    meta_data[['img_width', 'img_height']].plot(kind='box', ax=ax)
    ax.set_title('Distribution des Dimensions des Images')
    ax.set_ylabel('Pixels')
    #st.pyplot(fig3)

    #Scatter Plot des Positions des Annotations
    fig4, ax = plt.subplots()
    meta_data.plot(kind='scatter', x='x', y='y', alpha=0.5, ax=ax)
    ax.set_title('Position des Annotations sur les Images')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    #st.pyplot(fig4)

    # Affichage des graphiques dans des colonnes
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
        st.pyplot(fig3)
    with col2:
        st.pyplot(fig2)
        st.pyplot(fig4)
