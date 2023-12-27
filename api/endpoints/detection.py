from fastapi import APIRouter, HTTPException
from api.schemas.detection_schemas import DetectionRequest, DetectionResponse

router = APIRouter()

# ~ endpoint de détection d'objets
@router.post("/", response_model=DetectionResponse)
async def detect(request: DetectionRequest):
    """
    Lance la détection d'objets sur une image encodée en base64 et renvoie les résultats
    """
    print(request.image)
    #try:
    #    detections = run_detection(request.image)  # Assurez-vous que cette fonction traite l'image encodée en base64 et renvoie le format attendu
    #    return DetectionResponse(detections=detections)
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

    return DetectionResponse(detections=[])  # TODO: Remplacez cette ligne par la ligne ci-dessus lorsque vous aurez terminé la fonction run_detection

# ~ endpoint de santé
@router.get("/health")
async def health():
    """
    Vérifier si l'API est en ligne et fonctionnelle.
    """
    #try:
    #    run_detection("test")  # Assurez-vous que cette fonction traite l'image encodée en base64 et renvoie le format attendu
    #    return {"status": "ok"}
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

    return {"status": "ok"}

# ~ endpoint de recupération des meta-données du modèle
@router.get("/model/metadata")
async def model_metadata():
    """
    Récupérer les méta-données du modèle.
    """
    #try:
    #    metadata = get_model_metadata()  # Assurez-vous que cette fonction renvoie les méta-données du modèle
    #    return metadata
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

    return {}

# ~ endpoint de mise à jour du modèle #todo est ce que c'est utile ?
@router.post("/model/update")
async def update_model():
    """
    Mettre à jour le modèle YOLO en chargeant une nouvelle version.
    """
    #try:
    #    update_model()  # Assurez-vous que cette fonction met à jour le modèle
    #    return {"status": "ok"}
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

    return {"status": "ok"}

# ~ endpoint pour les statistiques d'utilisation du modèle
@router.get("/usage/stats")
async def usage_stats():
    """
    Fournir des statistiques sur l'utilisation de l'API, comme le nombre de requêtes traitées.
    """
    #try:
    #    stats = get_usage_stats()  # Assurez-vous que cette fonction renvoie les statistiques d'utilisation du modèle
    #    return stats
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

    return {}