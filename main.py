from fastapi import FastAPI
from api.endpoints import detection
import uvicorn

app = FastAPI(
    title="Mantes + Propre API 🌍",
    description="API pour la détection des déchets dans la ville de Mantes-la-Jolie, utilisant YOLOv8s. 🚀",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Développeur Mantes Plus Propre",
        "url": "http://mantespluspropre.com/contact",
        "email": "contact@mantespluspropre.com",
    },
    license_info={
        "name": "Licence MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Ajout des routes à l'application
app.include_router(detection.router, tags=["Détection"], prefix="/detect")

# Endpoint principal pour vérifier que l'API fonctionne
@app.get("/", tags=["Accueil"])
def read_root():
    return {"message": "Bienvenue sur l'API Mantes Plus Propre! 🎉"}

# Point d'entrée pour l'exécution avec Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
