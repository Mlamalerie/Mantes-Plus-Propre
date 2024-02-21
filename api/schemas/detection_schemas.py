from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ObjectDetection(BaseModel):
    cls: int = Field(..., description="Class of the object detected.")
    xywh : List[float] = Field(..., description="Bounding box coordinates (x1, y1, w, h).")
    conf: float = Field(..., description="Confidence of the prediction.", ge=0, le=1)

class DetectionResponse(BaseModel):
    count: int
    detections: List[ObjectDetection]
    image : str = Field(..., description="Image en base64 avec les détections.")
    date: datetime = Field(default_factory=datetime.now, description="Date de la détection.")

    out_image_path : str = Field(..., description="Path to the output image.")

