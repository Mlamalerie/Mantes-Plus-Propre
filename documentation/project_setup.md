## Prérequis

- Python 3.10.13 : Vous ferez attention à utiliser la bonne version de Python.
- Bibliothèques requises dans `requirements.txt`

## Installation

1. **Clonez le dépôt**  
   Clonez le dépôt GitHub sur votre machine locale en utilisant :
   ```
   git clone https://github.com/Mlamalerie/Mantes-Plus-Propre.git
   ```

2. **Installez les Dépendances**  
   Naviguez vers le répertoire du projet et installez les dépendances :
   ```
   cd Mantes-Plus-Propre
   pip install -r requirements.txt
   ```
3. **Créez un fichier `.env`**  
   Créez un fichier `.env` à la racine du projet et ajoutez-y les variables suivantes :

   ```
   REPLICATE_API_TOKEN=your_replicate_api_token # for the generation of cartoon
   BASEROW_DB_API_TOKEN=your_baserow_db_api_token # access to the baserow database
   ```

## Déploiement

### Construction des images Docker

```shell
# Construire l'image Docker pour le backend
docker build -t image-mpp-api -f Dockerfile-api .
# Construire l'image Docker pour le frontend
docker build -t image-mpp-app -f Dockerfile-app .
```

### Démarrage des conteneurs

Démarrer les deux services dans des conteneurs Docker distincts.

```shell
# --- Démarrer le serveur FastAPI
echo "Démarrage du serveur FastAPI..."
docker run --name mpp-api -p 8000:8000 -v shared_volume:/app/.inference image-mpp-api
#docker run --name mpp-api -p 8000:8000 -v "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\.inference":/app/.inference image-api-mpp

# --- Démarrer le serveur Streamlit
echo "Démarrage du serveur Streamlit..."
docker run --name mpp-app -p 8501:8501 -v shared_volume:/app/.inference image-mpp-app
#docker run --name mpp-app -p 8501:8501 -v "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\.inference":/app/.inference image-app-mpp


echo "Les serveurs sont démarrés."
```

Utiliser `docker-compose` pour démarrer les deux services dans des conteneurs Docker distincts.

```shell
# --- Démarrer les deux services dans des conteneurs Docker distincts
docker-compose up -d
```

### Push des images sur Docker Hub

```shell
# --- Push de l'image API
docker tag image-mpp-api mlamali/image-mpp-api:latest
docker push mlamali/image-mpp-api:latest

# --- Push de l'image APP
docker tag image-mpp-app mlamali/image-mpp-app:latest
docker push mlamali/image-mpp-app:latest
```

### Déploiement sur Heroku

```shell
# --- Connexion à Heroku
heroku login

# --- Création de l'application
heroku create mpp-app

# --- Push de l'image API
heroku container:push web -a mpp-app

# --- Déploiement de l'image API
heroku container:release web -a mpp-app

# --- Push de l'image APP
heroku container:push web -a mpp-app

# --- Déploiement de l'image APP
heroku container:release web -a mpp-app
```

Si docker prend trop de place sur votre machine, vous pouvez utiliser la commande `docker system prune` pour supprimer les images inutilisées.
https://stackoverflow.com/questions/39878939/docker-filling-up-storage-on-macos
