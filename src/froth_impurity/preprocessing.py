from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class CLAHEParams:
    enabled: bool = True
    clip_limit: float = 2.0
    tile_grid_size: int = 8

def to_gray(img_color_bgr):
    if len(img_color_bgr.shape) == 2:
        return img_color_bgr
    return cv2.cvtColor(img_color_bgr, cv2.COLOR_BGR2GRAY)

def apply_clahe(gray: np.ndarray, params: CLAHEParams) -> np.ndarray:
    if not params.enabled:
        return gray
    clahe = cv2.createCLAHE(clipLimit=float(params.clip_limit),
                            tileGridSize=(int(params.tile_grid_size), int(params.tile_grid_size)))
    return clahe.apply(gray)

def preprocess_gray(img_color_bgr, clahe_params: CLAHEParams) -> np.ndarray:
    gray = to_gray(img_color_bgr)
    gray = apply_clahe(gray, clahe_params)
    return gray
