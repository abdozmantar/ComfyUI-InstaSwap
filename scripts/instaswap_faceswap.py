#----------------------------------------------#
# INSTASWAP FAST FACE SWAPPER NODE FOR COMFYUI #
#                                              #
#                         by abdozmantar       #
#                             2024             #
#                                              #
#         GNU GENERAL PUBLIC LICENSE           #
#----------------------------------------------#

import os, glob
from PIL import Image
import modules.scripts as scripts

# from modules.upscaler import Upscaler, UpscalerData
from modules import scripts, shared, images, scripts_postprocessing
from modules.processing import (
    StableDiffusionProcessing,
    StableDiffusionProcessingImg2Img,
)

from scripts.instaswap_logger import logger
from scripts.instaswap_swapper import swap_face, get_current_faces_model, analyze_faces
import folder_paths

def get_models():
    models_path = os.path.join(folder_paths.models_dir,"insightface/*")
    models = glob.glob(models_path)
    models = [x for x in models if x.endswith(".onnx") or x.endswith(".pth")]
    return models

class FaceSwapScript(scripts.Script):

    def process(
        self,
        p: StableDiffusionProcessing,
        img,
        enable,
        source_faces_index,
        faces_index,
        model,
        swap_in_source,
        swap_in_generated,
        gender_source,
        gender_target,
        face_model,
    ):
        self.enable = enable
        if self.enable:

            self.source = img    
            self.swap_in_generated = swap_in_generated
            self.gender_source = gender_source
            self.gender_target = gender_target
            self.model = model
            self.face_model = face_model
            self.source_faces_index = [
                int(x) for x in source_faces_index.strip(",").split(",") if x.isnumeric()
            ]
            self.faces_index = [
                int(x) for x in faces_index.strip(",").split(",") if x.isnumeric()
            ]
            if len(self.source_faces_index) == 0:
                self.source_faces_index = [0]
            if len(self.faces_index) == 0:
                self.faces_index = [0]
            
            if self.gender_source is None or self.gender_source == "no":
                self.gender_source = 0
            elif self.gender_source  == "female":
                self.gender_source = 1
            elif self.gender_source  == "male":
                self.gender_source = 2
            
            if self.gender_target is None or self.gender_target == "no":
                self.gender_target = 0
            elif self.gender_target  == "female":
                self.gender_target = 1
            elif self.gender_target  == "male":
                self.gender_target = 2

            if isinstance(p, StableDiffusionProcessingImg2Img) and swap_in_source:
                logger.job(f"Thread Started : Transferring face from source index %s onto the target face index %s.", self.source_faces_index, self.faces_index)

                for i in range(len(p.init_images)):
                    if len(p.init_images) > 1:
                        logger.job(f"--------------- FRAME %s --------------", i)
                    result = swap_face(
                        self.source,
                        p.init_images[i],
                        source_faces_index=self.source_faces_index,
                        faces_index=self.faces_index,
                        model=self.model,
                        gender_source=self.gender_source,
                        gender_target=self.gender_target,
                        face_model=self.face_model,
                    )
                    p.init_images[i] = result
                logger.job("")
                logger.job("-------------- COMPLETED ! --------------")

    def postprocess_batch(self, p, *args, **kwargs):
        if self.enable:
            images = kwargs["images"]

    def postprocess_image(self, p, script_pp: scripts.PostprocessImageArgs, *args):
        if self.enable and self.swap_in_generated:
            if self.source is not None:
                logger.job(f"Thread Started : Transferring face from source index %s onto the target face index %s.s", self.source_faces_index, self.faces_index)
                image: Image.Image = script_pp.image
                result = swap_face(
                    self.source,
                    image,
                    source_faces_index=self.source_faces_index,
                    faces_index=self.faces_index,
                    model=self.model,
                    upscale_options=self.upscale_options,
                    gender_source=self.gender_source,
                    gender_target=self.gender_target,
                )
                try:
                    pp = scripts_postprocessing.PostprocessedImage(result)
                    pp.info = {}
                    p.extra_generation_params.update(pp.info)
                    script_pp.image = pp.image
                except:
                    logger.error(f"Failed to create the image!")
