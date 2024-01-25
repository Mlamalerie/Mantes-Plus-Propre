from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List
from api.schemas.detection_schemas import DetectionResponse, ObjectDetection
from src.detection.utils import __version__ as model_version
import os
from datetime import datetime

router = APIRouter()


@router.post("/image", response_model=DetectionResponse)
async def blur(file: UploadFile = File(..., description="Image à analyser."),
               confidence: float = 0.5):
    """
    Lance la détection d'objets sur une image encodée en base64 et renvoie les résultats
    """
    pass


# ~ endpoint de santé
@router.get("/health")
async def health():
    """
    Vérifier si l'API est en ligne et fonctionnelle.
    """
    return {"status": "ok"}
