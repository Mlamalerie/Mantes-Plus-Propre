from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import File, UploadFile
from datetime import datetime

# class boxes (label, y, y, w, h)



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

