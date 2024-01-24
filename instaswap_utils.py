import os
from PIL import Image
import numpy as np
import torch
import cv2
import logging
import hashlib
from insightface.app.common import Face
from safetensors.torch import save_file, safe_open


def tensor_to_pil(img_tensor, batch_index=0):
    # Convert tensor of shape [batch_size, channels, height, width] at the batch_index to PIL Image
    img_tensor = img_tensor[batch_index].unsqueeze(0)
    i = 255. * img_tensor.cpu().numpy()
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8).squeeze())
    return img


def batch_tensor_to_pil(img_tensor):
    # Convert tensor of shape [batch_size, channels, height, width] to a list of PIL Images
    return [tensor_to_pil(img_tensor, i) for i in range(img_tensor.shape[0])]


def pil_to_tensor(image):
    # Takes a PIL image and returns a tensor of shape [1, height, width, channels]
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image).unsqueeze(0)
    if len(image.shape) == 3:  # If the image is grayscale, add a channel dimension
        image = image.unsqueeze(-1)
    return image


def batched_pil_to_tensor(images):
    # Takes a list of PIL images and returns a tensor of shape [batch_size, height, width, channels]
    return torch.cat([pil_to_tensor(image) for image in images], dim=0)


def img2tensor(imgs, bgr2rgb=True, float32=True):

    def _totensor(img, bgr2rgb, float32):
        if img.shape[2] == 3 and bgr2rgb:
            if img.dtype == 'float64':
                img = img.astype('float32')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img.transpose(2, 0, 1))
        if float32:
            img = img.float()
        return img

    if isinstance(imgs, list):
        return [_totensor(img, bgr2rgb, float32) for img in imgs]
    else:
        return _totensor(imgs, bgr2rgb, float32)


def tensor2img(tensor, rgb2bgr=True, out_type=np.uint8, min_max=(0, 1)):

    if not (torch.is_tensor(tensor) or (isinstance(tensor, list) and all(torch.is_tensor(t) for t in tensor))):
        raise TypeError(f'tensor or list of tensors expected, got {type(tensor)}')

    if torch.is_tensor(tensor):
        tensor = [tensor]
    result = []
    for _tensor in tensor:
        _tensor = _tensor.squeeze(0).float().detach().cpu().clamp_(*min_max)
        _tensor = (_tensor - min_max[0]) / (min_max[1] - min_max[0])

        n_dim = _tensor.dim()
        if n_dim == 4:
            img_np = make_grid(_tensor, nrow=int(math.sqrt(_tensor.size(0))), normalize=False).numpy()
            img_np = img_np.transpose(1, 2, 0)
            if rgb2bgr:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 3:
            img_np = _tensor.numpy()
            img_np = img_np.transpose(1, 2, 0)
            if img_np.shape[2] == 1:  # gray image
                img_np = np.squeeze(img_np, axis=2)
            else:
                if rgb2bgr:
                    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        elif n_dim == 2:
            img_np = _tensor.numpy()
        else:
            raise TypeError('Only support 4D, 3D or 2D tensor. ' f'But received with dimension: {n_dim}')
        if out_type == np.uint8:
            # Unlike MATLAB, numpy.unit8() WILL NOT round by default.
            img_np = (img_np * 255.0).round()
        img_np = img_np.astype(out_type)
        result.append(img_np)
    if len(result) == 1:
        result = result[0]
    return result

def move_path(old_path, new_path):
    if os.path.exists(old_path):
        try:
            models = os.listdir(old_path)
            for model in models:
                move_old_path = os.path.join(old_path, model)
                move_new_path = os.path.join(new_path, model)
                os.rename(move_old_path, move_new_path)
            os.rmdir(old_path)
        except Exception as e:
            print(f"Error: {e}")
            new_path = old_path

def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

def get_image_md5hash(image: Image.Image):
    md5hash = hashlib.md5(image.tobytes())
    return md5hash.hexdigest()

def save_face_model(face: Face, filename: str) -> None:
    try:
        tensors = {
            "bbox": torch.tensor(face["bbox"]),
            "kps": torch.tensor(face["kps"]),
            "det_score": torch.tensor(face["det_score"]),
            "landmark_3d_68": torch.tensor(face["landmark_3d_68"]),
            "pose": torch.tensor(face["pose"]),
            "landmark_2d_106": torch.tensor(face["landmark_2d_106"]),
            "embedding": torch.tensor(face["embedding"]),
            "gender": torch.tensor(face["gender"]),
            "age": torch.tensor(face["age"]),
        }
        save_file(tensors, filename)
        print(f"Face model has been saved to '{filename}'")
    except Exception as e:
        print(f"Error: {e}")

def load_face_model(filename: str):
    face = {}
    with safe_open(filename, framework="pt") as f:
        for k in f.keys():
            face[k] = f.get_tensor(k).numpy()
    return Face(face)
