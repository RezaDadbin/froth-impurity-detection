from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class FilterParams:
    min_area_px: int = 5
    max_area_px: int = 11  # small by your notebook; feel free to raise later

def find_and_filter_contours(mask: np.ndarray, f: FilterParams) -> Tuple[List[np.ndarray], int]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in contours:
        a = cv2.contourArea(c)
        if a < f.min_area_px:
            continue
        if f.max_area_px and a > f.max_area_px:
            continue
        out.append(c)
    return out, len(out)
