from pydantic import BaseModel, Field
from typing import List, Optional

# class boxes (label, y, y, w, h)

class DetectionRequest(BaseModel):
    image_url : str = Field(..., description="Image url to detect objects from.")
    confidence: float = Field(0.5, ge=0, le=1, description="Confidence threshold for the predictions.")
    limit: Optional[int] = Field(..., ge=1, description="Maximum number of predictions to return.")


class ObjectDetection(BaseModel):
    orig_image: str
    result_image: str
    bboxes : List[List[float]]

class DetectionResponse(BaseModel):
    detections: List[ObjectDetection]
