import os
from glob import glob
# class for enum

BASEDIR = os.path.dirname(__file__).replace("\\", "/")

BEST_TACO_YOLOV8_WEIGHTS = f"{BASEDIR}/archives/best yolov8s [taco-dataset (yoloformat) train-3826-val-479-test-479 20231225_22, epochs=100] 20231225_2345.pt"
BEST_MPP_YOLOV8_WEIGHTS = f"{BASEDIR}/best yolov8s [fused-dataset 20240115, epochs=100] 20240118_0113.pt"

AVAILABLE_YOLO_MODELS = {
    "yolov8n (coco)": f"{BASEDIR}/archives/yolov8n.pt",
    "yolov8s (taco)": BEST_TACO_YOLOV8_WEIGHTS,
    "yolov8s (mpp)": BEST_MPP_YOLOV8_WEIGHTS,
}

def get_weights_list(extension: str = None):
    pattern = f"*.{extension}" if extension is not None else "*"
    weights_list = glob(os.path.join(os.path.dirname(__file__), pattern))

    return weights_list



