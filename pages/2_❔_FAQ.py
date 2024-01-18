import streamlit as st
st.subheader("F.A.Q")
with st.expander("C'est quoi un déchet sauvage ?", expanded=True):
    st.write("""
    Un déchet sauvage est un déchet abandonné par un individu dans un lieu public ou privé, sans autorisation du propriétaire du lieu, et sans utiliser les dispositifs mis à disposition pour le tri et la collecte des déchets.
    Cela inclue les emballages, les bouteilles, les canettes, et autres résidus qui ne sont pas correctement disposés dans des poubelles ou des centres de recyclage. 
    """)


with st.expander("Comment fonctionne l'application ?"):
    st.write("""
    L'application est composée de deux parties : 
    - Une partie détection qui permet de détecter les déchets sur une image #todo mettre des gifs
    - Une partie cartographie qui permet de visualiser les déchets détectés sur une carte
    """)