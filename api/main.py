from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import detection, blurring
import uvicorn

app = FastAPI(
    title="Mantes + Propre API 🌍",
    description="API pour la détection des déchets dans la ville de Mantes-la-Jolie, utilisant YOLOv8s. 🚀",
    version="2024.01.1",
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

# the backend must have a list of « allowed origins »
origins = [
    "http://localhost",
    "http://localhost:8080"


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# Ajout des routes à l'application
app.include_router(detection.router, tags=["Détection"], prefix="/detect")
app.include_router(blurring.router, tags=["Annonymisation"], prefix="/blur")

# Endpoint principal pour vérifier que l'API fonctionne
@app.get("/", tags=["Accueil"])
def read_root():
    return {"message": "Bienvenue sur l'API Mantes Plus Propre! 🎉"}

# Point d'entrée pour l'exécution avec Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
