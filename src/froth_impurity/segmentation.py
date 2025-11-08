from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class SegmentParams:
    method: str = "dynamic"     # "dynamic" | "otsu" | "fixed" | "adaptive"
    k_dynamic: float = 0.834
    fixed_thresh: int = 140
    invert: bool = True
    morph_open_kernel: int = 2
    morph_open_iterations: int = 1
    adaptive_block_size: int = 35
    adaptive_C: int = -5

def _dynamic_threshold_value(gray: np.ndarray, k: float) -> int:
    mean = float(np.mean(gray))
    std = float(np.std(gray))
    t = int(max(0, min(255, round(mean - k * std))))
    return t

def threshold_mask(gray: np.ndarray, p: SegmentParams) -> np.ndarray:
    if p.method == "dynamic":
        t = _dynamic_threshold_value(gray, p.k_dynamic)
        _, m = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
    elif p.method == "otsu":
        _, m = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif p.method == "fixed":
        _, m = cv2.threshold(gray, int(p.fixed_thresh), 255, cv2.THRESH_BINARY)
    elif p.method == "adaptive":
        block = max(3, p.adaptive_block_size | 1)  # must be odd
        m = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, block, p.adaptive_C)
    else:
        raise ValueError(f"Unknown method: {p.method}")

    # Morphological open to remove speckle noise
    if p.morph_open_kernel > 0 and p.morph_open_iterations > 0:
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (p.morph_open_kernel, p.morph_open_kernel))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k, iterations=p.morph_open_iterations)

    if p.invert:
        m = cv2.bitwise_not(m)

    return m
