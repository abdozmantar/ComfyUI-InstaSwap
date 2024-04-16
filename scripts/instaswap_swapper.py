#----------------------------------------------#
# INSTASWAP FAST FACE SWAPPER NODE FOR COMFYUI #
#                                              #
#                         by abdozmantar       #
#                             2024             #
#                                              #
#         GNU GENERAL PUBLIC LICENSE           #
#----------------------------------------------#

import copy
import os
import shutil

from dataclasses import dataclass
from typing import List, Union

import cv2
import numpy as np

from PIL import Image
import insightface
from insightface.app.common import Face

try:
    import torch.cuda as cuda
except:
    cuda = None

from scripts.instaswap_logger import logger
from instaswap_utils import move_path, get_image_md5hash
import folder_paths
import warnings

np.warnings = warnings
np.warnings.filterwarnings('ignore')

if cuda is not None:
    if cuda.is_available():
        providers = ["CUDAExecutionProvider"]
    else:
        providers = ["CPUExecutionProvider"]
else:
    providers = ["CPUExecutionProvider"]

models_path_old = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
insightface_path_old = os.path.join(models_path_old, "insightface")
insightface_models_path_old = os.path.join(insightface_path_old, "models")

models_path = folder_paths.models_dir
insightface_path = os.path.join(models_path, "insightface")
insightface_models_path = os.path.join(insightface_path, "models")

if os.path.exists(models_path_old):
    move_path(insightface_models_path_old, insightface_models_path)
    move_path(insightface_path_old, insightface_path)
    move_path(models_path_old, models_path)
if os.path.exists(insightface_path) and os.path.exists(insightface_path_old):
    shutil.rmtree(insightface_path_old)
    shutil.rmtree(models_path_old)

FS_MODEL = None
CURRENT_FS_MODEL_PATH = None
ANALYSIS_MODEL = None
SOURCE_FACES = None
SOURCE_IMAGE_HASH = None
TARGET_FACES = None
TARGET_IMAGE_HASH = None

def get_current_faces_model():
    global SOURCE_FACES
    return SOURCE_FACES

def getAnalysisModel():
    global ANALYSIS_MODEL
    if ANALYSIS_MODEL is None:
        ANALYSIS_MODEL = insightface.app.FaceAnalysis(
            name="buffalo_l", providers=providers, root=insightface_path
        )
    return ANALYSIS_MODEL


def getFaceSwapModel(model_path: str):
    global FS_MODEL
    global CURRENT_FS_MODEL_PATH
    if CURRENT_FS_MODEL_PATH is None or CURRENT_FS_MODEL_PATH != model_path:
        CURRENT_FS_MODEL_PATH = model_path
        FS_MODEL = insightface.model_zoo.get_model(model_path, providers=providers)

    return FS_MODEL


def get_face_gender(
        face,
        face_index,
        gender_condition,
        operated: str
):
    gender = [
        x.sex
        for x in face
    ]
    gender.reverse()
    face_gender = gender[face_index]
    logger.job("%s Face %s: Detected Gender -%s-", operated, face_index, face_gender)
    if (gender_condition == 1 and face_gender == "F") or (gender_condition == 2 and face_gender == "M"):
        logger.job("Pass : Gender identification confirmed as matching the specified condition")
        try:
            return sorted(face, key=lambda x: x.bbox[0])[face_index], 0
        except IndexError:
            return None, 0
    else:
        logger.job("Halt : Gender identification not confirmed as matching the specified condition")
        return sorted(face, key=lambda x: x.bbox[0])[face_index], 1


def half_det_size(det_size):
    logger.job("Attempting to reduce the det_size parameter by half")
    return (det_size[0] // 2, det_size[1] // 2)

def analyze_faces(img_data: np.ndarray, det_size=(640, 640)):
    face_analyser = copy.deepcopy(getAnalysisModel())
    face_analyser.prepare(ctx_id=0, det_size=det_size)
    return face_analyser.get(img_data)

def get_face_single(img_data: np.ndarray, face, face_index=0, det_size=(640, 640), gender_source=0, gender_target=0):

    buffalo_path = os.path.join(insightface_models_path, "buffalo_l.zip")
    if os.path.exists(buffalo_path):
        os.remove(buffalo_path)

    if gender_source != 0:
        if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
            det_size_half = half_det_size(det_size)
            return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)
        return get_face_gender(face,face_index,gender_source,"Source")

    if gender_target != 0:
        if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
            det_size_half = half_det_size(det_size)
            return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)
        return get_face_gender(face,face_index,gender_target,"Target")
    
    if len(face) == 0 and det_size[0] > 320 and det_size[1] > 320:
        det_size_half = half_det_size(det_size)
        return get_face_single(img_data, analyze_faces(img_data, det_size_half), face_index, det_size_half, gender_source, gender_target)

    try:
        return sorted(face, key=lambda x: x.bbox[0])[face_index], 0
    except IndexError:
        return None, 0

def swap_face(
    source_img: Union[Image.Image, None],
    target_img: Image.Image,
    model: Union[str, None] = None,
    source_faces_index: List[int] = [0],
    faces_index: List[int] = [0],
    gender_source: int = 0,
    gender_target: int = 0,
    face_model: Union[Face, None] = None,
):
    global SOURCE_FACES, SOURCE_IMAGE_HASH, TARGET_FACES, TARGET_IMAGE_HASH
    result_image = target_img

    if model is not None:

        if isinstance(source_img, str):  # source_img is a base64 string
            import base64, io
            if 'base64,' in source_img:  # check if the base64 string has a data URL scheme
                # split the base64 string to get the actual base64 encoded image data
                base64_data = source_img.split('base64,')[-1]
                # decode base64 string to bytes
                img_bytes = base64.b64decode(base64_data)
            else:
                # if no data URL scheme, just decode
                img_bytes = base64.b64decode(source_img)
            
            source_img = Image.open(io.BytesIO(img_bytes))
            
        target_img = cv2.cvtColor(np.array(target_img), cv2.COLOR_RGB2BGR)

        if source_img is not None:

            source_img = cv2.cvtColor(np.array(source_img), cv2.COLOR_RGB2BGR)

            source_image_md5hash = get_image_md5hash(source_img)

            if SOURCE_IMAGE_HASH is None:
                SOURCE_IMAGE_HASH = source_image_md5hash
                source_image_same = False
            else:
                source_image_same = True if SOURCE_IMAGE_HASH == source_image_md5hash else False
                if not source_image_same:
                    SOURCE_IMAGE_HASH = source_image_md5hash

            logger.info("Source face input hash = %s", SOURCE_IMAGE_HASH)
            logger.info("Source face input is equal ? %s", source_image_same)

            if SOURCE_FACES is None or not source_image_same:
                logger.job("[Analyzing source face input]")
                source_faces = analyze_faces(source_img)
                SOURCE_FACES = source_faces
            elif source_image_same:
                logger.job("Utilizing hashed model for source faces")
                source_faces = SOURCE_FACES

        elif face_model is not None:

            source_faces_index = [0]
            logger.job("Utilizing the pre-loaded model for source faces")
            source_face_model = [face_model]
            source_faces = source_face_model

        else:
            logger.error("Unable to identify any source entities")

        if source_faces is not None:

            target_image_md5hash = get_image_md5hash(target_img)

            if TARGET_IMAGE_HASH is None:
                TARGET_IMAGE_HASH = target_image_md5hash
                target_image_same = False
            else:
                target_image_same = True if TARGET_IMAGE_HASH == target_image_md5hash else False
                if not target_image_same:
                    TARGET_IMAGE_HASH = target_image_md5hash

            logger.info("Target face input Hash = %s", TARGET_IMAGE_HASH)
            logger.info("Target face input is equal ? %s", target_image_same)
            
            if TARGET_FACES is None or not target_image_same:
                logger.job("[Analyzing target face input]")
                target_faces = analyze_faces(target_img)
                TARGET_FACES = target_faces
            elif target_image_same:
                logger.job("Utilizing hashed model for target faces")
                target_faces = TARGET_FACES

            if source_img is not None:
                source_face, wrong_gender = get_face_single(source_img, source_faces, face_index=source_faces_index[0], gender_source=gender_source)
            else:
                source_face = sorted(source_faces, key=lambda x: x.bbox[0])[source_faces_index[0]]
                wrong_gender = 0

            if len(source_faces_index) != 0 and len(source_faces_index) != 1 and len(source_faces_index) != len(faces_index):
                logger.job(f'The number of Source Faces should be zero (default), singular, or equal to the number of target faces')
            elif source_face is not None:
                result = target_img
                model_path = model_path = os.path.join(insightface_path, model)
                face_swapper = getFaceSwapModel(model_path)

                source_face_idx = 0

                for face_num in faces_index:
                    if len(source_faces_index) > 1 and source_face_idx > 0:
                        source_face, wrong_gender = get_face_single(source_img, source_faces, face_index=source_faces_index[source_face_idx], gender_source=gender_source)
                    source_face_idx += 1

                    if source_face is not None and wrong_gender == 0:
                        target_face, wrong_gender = get_face_single(target_img, target_faces, face_index=face_num, gender_target=gender_target)
                        if target_face is not None and wrong_gender == 0:
                            logger.job(f"Swapping face(s)...")
                            result = face_swapper.get(result, target_face, source_face)
                        elif wrong_gender == 1:
                            wrong_gender = 0
                            if source_face_idx == len(source_faces_index):
                                result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                                return result_image
                        else:
                            logger.job(f"No target face found for {face_num}")
                    elif wrong_gender == 1:
                        wrong_gender = 0
                        if source_face_idx == len(source_faces_index):
                            result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                            return result_image
                    else:
                        logger.job(f"No source face found for face number : {source_face_idx}.")

                result_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

            else:
                logger.job("Provided index contains no source face(s)")
        else:
            logger.job("No source face(s) detected")
    return result_image
