from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class VizParams:
    draw_contours: bool = True
    overlay_color: tuple[int, int, int] = (255, 0, 0)
    overlay_thickness: int = 1
    alpha_overlay: float = 0.35
    label_color: tuple[int, int, int] = (0, 255, 0)
    grid: bool = False
    show_windows: bool = False 

def to_color(gray_or_color):
    if len(gray_or_color.shape) == 2:
        return cv2.cvtColor(gray_or_color, cv2.COLOR_GRAY2BGR)
    return gray_or_color.copy()

def draw_contour_overlay(base_img, contours: List[np.ndarray], viz: VizParams):
    color = to_color(base_img)
    if viz.draw_contours and contours:
        cv2.drawContours(color, contours, -1, viz.overlay_color, viz.overlay_thickness)
    return color

def put_count_text(img, count: int, viz: VizParams):
    out = to_color(img)
    cv2.putText(out, f"impurities: {count}", (12, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, viz.label_color, 2, cv2.LINE_AA)
    return out
