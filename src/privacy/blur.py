import os
from src.privacy.weights.utils import EGOBLUR_WEIGHTS


def _run_command(cmd):
    print(cmd)
    os.system(cmd)

# create a fonction for all this
def blur_image(image_path: str,
               face_model_score_threshold: float = 0.7,lp_model_score_threshold: float = 0.5,
               nms_iou_threshold: float = 0.3,
               scale_factor_detections: float = 1,
               verbose: bool = False):
    if not os.path.exists(image_path):
        raise ValueError(f"Image path does not exist: {image_path}")

    FACE_MODEL_PATH, LP_MODEL_PATH = EGOBLUR_WEIGHTS.FACE_MODEL_PATH, EGOBLUR_WEIGHTS.LP_MODEL_PATH
    if not os.path.exists(FACE_MODEL_PATH):
        raise ValueError(f"Face model path does not exist: {FACE_MODEL_PATH}")
    if not os.path.exists(LP_MODEL_PATH):
        raise ValueError(f"LP model path does not exist: {LP_MODEL_PATH}")

    print(f">>> Blurring image {image_path}...")
    ext = os.path.splitext(image_path)[1]
    output_path = image_path.replace(ext, f"_blurred{ext}")
    cmd = f'python ego_blur.py --face_model_path "{FACE_MODEL_PATH}" --lp_model_path "{LP_MODEL_PATH}"'
    cmd += f' --input_image_path "{image_path}" --output_image_path "{output_path}"'
    cmd += f' --face_model_score_threshold {face_model_score_threshold} --lp_model_score_threshold {lp_model_score_threshold} --nms_iou_threshold {nms_iou_threshold} --scale_factor_detections {scale_factor_detections}'
    _run_command(cmd)
    if verbose:
        print(f"> Done. Image blurred and saved to {output_path}")

    return output_path


if __name__ == "__main__":
    image_path = "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\images_demo\egoblur_demo\img_4.png"
    out = blur_image(image_path)
    # check if image exists
    if not os.path.exists(out):
        raise ValueError(f"Output image does not exist: {out}")
