
# Tutoriel d'Utilisation de l'API "Mantes Plus Propre"

Bienvenue dans le guide rapide pour utiliser et exécuter l'API "Mantes Plus Propre". Cette API est construite en utilisant FastAPI et permet de détecter des déchets à partir d'images en utilisant le modèle YOLOv8s.


## Exécution de l'API

Après avoir installé le projet correctement (voir [ici](project_setup.md)), vous pouvez exécuter l'API.

Pour exécuter l'API localement :

1. **Lancer le Serveur**  
   Utilisez la commande suivante pour démarrer le serveur FastAPI :
   ```
   uvicorn main:app --reload
   ```

2. **Accéder à l'API**  
   Une fois le serveur lancé, vous pouvez accéder à l'API à l'adresse : [http://localhost:8000](http://localhost:8000)

3. **Documentation Interactive**  
   FastAPI fournit une documentation interactive. Vous pouvez y accéder à : [http://localhost:8000/docs](http://localhost:8000/docs)

## Utilisation de l'API

- **Endpoint de Détection** : `/detect`  
  Envoyez une image encodée en base64 pour détecter les déchets. Utilisez le format POST avec le contenu JSON correspondant.

- **Endpoints de Santé et de Métadonnées** : `/health`, `/model/metadata`  
  Ces endpoints fournissent des informations sur l'état de l'API et des détails sur le modèle utilisé.

---

N'hésitez pas à expérimenter avec l'API et à fournir des retours pour améliorer le projet. Bonne chance ! 🚀

---
