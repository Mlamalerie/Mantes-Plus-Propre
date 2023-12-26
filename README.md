# "Mantes + Propre" 

> Agissons ensemble pour une mantes plus jolie !


## Installation

Après avoir crée un venv, utilisez la commande `pip install -r requirements.txt` pour installer les dépendances.

Ensuite, créez un fichier `.env` à la racine du projet et ajoutez-y les variables suivantes :

```
REPLICATE_API_TOKEN=your_replicate_api_token # for the generation of cartoon

```

## Lancement

Pour lancer l'application, utilisez la commande `python streamlit run app.py`.

## Structure du projet

``` 
.
├── README.md
├── app.py 
├── requirements.txt
├── .env
├── assets # Contient les assets de l'application et autres fichiers statiques (css, js, images, etc.)

├── pages # Contient les pages de l'application
│   ├── __init__.py