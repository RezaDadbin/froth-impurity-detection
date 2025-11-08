from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Tuple
import cv2
import os

IMG_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMG_EXTS

def list_images(folder: Path) -> List[Path]:
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.is_file() and is_image(p)])

def read_gray(path: Path):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img

def read_color(path: Path):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img

def ensure_dir(path: Path) -> Path:
    Path(path).mkdir(parents=True, exist_ok=True)
    return Path(path)

def write_image(path: Path, img) -> None:
    ensure_dir(path.parent)
    cv2.imwrite(str(path), img)

def stem_no_ext(p: Path) -> str:
    return p.stem

def pair_output_paths(input_path: Path, out_dir: Path) -> Tuple[Path, Path, Path]:
    """
    Returns (mask_path, overlay_path, csv_path_for_folder)
    csv_path_for_folder is the folder-level path; caller aggregates.
    """
    name = stem_no_ext(input_path)
    mask_path = Path(out_dir) / f"{name}_mask.png"
    overlay_path = Path(out_dir) / f"{name}_overlay.png"
    csv_path = Path(out_dir) / "results.csv"
    return mask_path, overlay_path, csv_path
