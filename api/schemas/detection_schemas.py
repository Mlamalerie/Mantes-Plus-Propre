from pydantic import BaseModel
from typing import List

class DetectionRequest(BaseModel):
    image: str  # Image encodée en base64

class ObjectDetection(BaseModel):
    cls: str
    confidence: float
    bbox: List[float]  # Format [x_min, y_min, x_max, y_max]

class DetectionResponse(BaseModel):
    detections: List[ObjectDetection]
