from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List
from PIL import Image
import io
from src.detection.utils import __version__ as model_version
from src.detection.utils import run_detection_from_array, read_imagefile
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


class ObjectDetection(BaseModel):
    cls: int = Field(..., description="Class of the object detected.")
    x1: float = Field(..., description="x1 coordinate of the bounding box.")
    y1: float = Field(..., description="y1 coordinate of the bounding box.")
    x2: float = Field(..., description="x2 coordinate of the bounding box.")
    y2: float = Field(..., description="y2 coordinate of the bounding box.")
    conf: float = Field(..., description="Confidence of the prediction.", ge=0, le=1)


class DetectionResponse(BaseModel):
    count: int
    detections: List[ObjectDetection]
    date: datetime = Field(default_factory=datetime.now, description="Date de la détection.")

    out_image_path : str = Field(..., description="Path to the output image.")


def yolo_boxes_to_list(boxes) -> List[ObjectDetection]:
    result = []
    if boxes is None:
        return result
    for i_det, box in enumerate(boxes):
        xyxy = box.xywh.cpu().numpy().flatten()  # Aplatir le tableau
        x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]

        cls = int(box.cls.cpu().numpy().item())
        conf = box.conf.cpu().numpy().item()

        result.append(ObjectDetection(cls=cls, x1=x1, y1=y1, x2=x2, y2=y2, conf=conf))
    return result


@router.post("/image", response_model=DetectionResponse)
async def detect(file: UploadFile = File(..., description="Image à analyser."),
                 confidence: float = 0.3,
                 limit: Optional[int] = None):
    """
    Lance la détection d'objets sur une image encodée en base64 et renvoie les résultats
    """
    bgr_image_np = read_imagefile(await file.read())
    YYYYMMDD = datetime.now().strftime("%Y-%m-%d")
    image_name = file.filename
    output_detections, save_dir = run_detection_from_array(bgr_image_np, confidence_threshold=confidence,
                                                           xp_name=f"{YYYYMMDD}/{image_name}")

    if output_detections is None:
        raise HTTPException(status_code=404, detail="No detections found.")
    output_image_path = os.path.join(save_dir, "image0.jpg")
    if not os.path.exists(output_image_path):
        raise HTTPException(status_code=404, detail="No detections found.")

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
