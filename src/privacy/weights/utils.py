import os

BASEDIR = os.path.dirname(__file__).replace("\\", "/")

class EGOBLUR_WEIGHTS:
    # absolute path
    FACE_MODEL_PATH = f"{BASEDIR}/ego_blur_face.jit"
    LP_MODEL_PATH = f"{BASEDIR}/ego_blur_lp.jit"

