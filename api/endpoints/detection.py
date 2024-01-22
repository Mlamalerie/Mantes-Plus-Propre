from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List
from api.schemas.detection_schemas import DetectionResponse, ObjectDetection
from src.detection.utils import __version__ as model_version
from src.detection.utils import run_detection_from_array, read_imagefile
import os
from datetime import datetime


def yolo_boxes_to_list(boxes) -> List[ObjectDetection]:
    result = []
    if boxes is None:
        return result
    for i_det, box in enumerate(boxes):
        xywh = box.xywh.cpu().numpy().flatten()  # Aplatir le tableau
        xywh = xywh[0], xywh[1], xywh[2], xywh[3]

        cls = int(box.cls.cpu().numpy().item())
        conf = box.conf.cpu().numpy().item()

        result.append(ObjectDetection(cls=cls, xywh=xywh, conf=conf))
    return result

router = APIRouter()

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



