from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List
from PIL import Image
import io
from api.schemas.detection_schemas import DetectionResponse, ObjectDetection
from src.detection.utils import __version__ as model_version
from src.detection.utils import run_detection_from_array, read_imagefile, yolo_boxes_to_list
import numpy as np
import os
from datetime import datetime
import tempfile
from PIL import Image, ImageOps, ImageDraw, ImageFont

router = APIRouter()


class DetectionRequest(BaseModel):
    file: UploadFile = File(..., description="Image à analyser.")
    confidence: float = Field(0.5, ge=0, le=1, description="Confidence threshold for the predictions.")
    limit: Optional[int] = Field(None, ge=1, description="Maximum number of predictions to return.")
    date: datetime = Field(default_factory=datetime.now, description="Date de la détection.")


@router.post("/image", response_model=DetectionResponse)
async def detect(file: UploadFile = File(..., description="Image à analyser."),
                 confidence: float = 0.5,
                 limit: Optional[int] = None):
    """
    Lance la détection d'objets sur une image encodée en base64 et renvoie les résultats
    """

    bgr_image_np = read_imagefile(await file.read())
    YYYYMMDD = datetime.now().strftime("%Y-%m-%d")
    image_name = file.filename

    print(">>>> Running detection on image.")

    try:
        output_detections, save_dir = run_detection_from_array(bgr_image_np, confidence_threshold=confidence,
                                                           xp_name=f"{YYYYMMDD}/{image_name}")
    except Exception as e:
        raise HTTPException(status_code=422, detail="Error during detection : " + str(e))

    if output_detections is None:
        raise HTTPException(status_code=404, detail="No detections found.")

    output_image_path = os.path.join(save_dir, "image0.jpg")

    return DetectionResponse(count=len(output_detections.boxes),
                             detections=yolo_boxes_to_list(output_detections.boxes),
                             out_image_path=output_image_path
                             )


# ~ endpoint de santé
@router.get("/health")
async def health():
    """
    Vérifier si l'API est en ligne et fonctionnelle.
    """
    return {"status": "ok", "model_version": model_version}
