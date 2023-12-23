import os

def run_command(cmd):
    print(cmd)
    os.system(cmd)


FACE_MODEL_PATH = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\ai\ego_blur\ego_blur_face.jit"
LP_MODEL_PATH = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\ai\ego_blur\ego_blur_lp.jit"
INPUT_IMAGE_PATH = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\egoblur_demo\img.png"
INPUT_VIDEO_PATH = r"N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\poubelles_marseille_tf1.mp4"
bool_image = True
bool_video = False

# verify if input image
if not os.path.exists(INPUT_IMAGE_PATH) and bool_image:
    print("Input image path does not exist")
    exit()
if not os.path.exists(INPUT_VIDEO_PATH) and bool_video:
    print("Input video path does not exist")
    exit()

OUTPUT_IMAGE_PATH = INPUT_IMAGE_PATH.replace(".png", "_output.png")
OUTPUT_VIDEO_PATH = INPUT_IMAGE_PATH.replace(".png", "_output.mp4")
FACE_MODEL_SCORE_THRESHOLD = 0.7
LP_MODEL_SCORE_THRESHOLD = 0.5
NMS_IOU_THRESHOLD = 0.3
SCALE_FACTOR_DETECTIONS = 1
OUTPUT_VIDEO_FPS = 3

"""python ego_blur.py --face_model_path "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\ego_blur_face.jit" --lp_model_path "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\ego_blur_lp.jit" --input_image_path "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\voiture.png" --output_image_path "N:\My Drive\KESKIA Drive Mlamali\Mantes-Plus-Propre\assets\voiture output.png" --face_model_score_threshold 0.9 --lp_model_score_threshold 0.6 --nms_iou_threshold 0.3 --scale_factor_detections 1 --output_video_fps 3"""

cmd = f'python ego_blur.py --face_model_path "{FACE_MODEL_PATH}" --lp_model_path "{LP_MODEL_PATH}"'
if bool_image:
    cmd += f' --input_image_path "{INPUT_IMAGE_PATH}" --output_image_path "{OUTPUT_IMAGE_PATH}"'
if bool_video:
    cmd += f' --input_video_path "{INPUT_VIDEO_PATH}" --output_video_path "{OUTPUT_VIDEO_PATH}" --output_video_fps {OUTPUT_VIDEO_FPS}'

cmd += f' --face_model_score_threshold {FACE_MODEL_SCORE_THRESHOLD} --lp_model_score_threshold {LP_MODEL_SCORE_THRESHOLD} --nms_iou_threshold {NMS_IOU_THRESHOLD} --scale_factor_detections {SCALE_FACTOR_DETECTIONS}'

run_command(cmd)
