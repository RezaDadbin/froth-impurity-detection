from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml
import numpy as np
import cv2
from .io import read_color, read_gray, ensure_dir, write_image, pair_output_paths
from .preprocessing import preprocess_gray, CLAHEParams
from .segmentation import threshold_mask, SegmentParams
from .contours import find_and_filter_contours, FilterParams
from .visualize import draw_contour_overlay, put_count_text, VizParams

@dataclass
class PathsConfig:
    input_dir: Path
    output_dir: Path

@dataclass
class Config:
    paths: PathsConfig
    clahe: CLAHEParams
    seg: SegmentParams
    filt: FilterParams
    viz: VizParams
    export_mask: bool = True
    export_overlay: bool = True

def load_config(path: str | Path) -> Config:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)

    paths = PathsConfig(
        input_dir=Path(cfg["paths"]["input_dir"]),
        output_dir=Path(cfg["paths"]["output_dir"]),
    )
    clahe = CLAHEParams(**cfg.get("preprocess", {}).get("clahe", {}))
    seg = SegmentParams(**cfg.get("segment", {}))
    filt = FilterParams(**cfg.get("filter", {}))
    viz = VizParams(**cfg.get("visualize", {}))
    export = cfg.get("export", {})
    return Config(paths, clahe, seg, filt, viz,
                  export_mask=bool(export.get("save_mask", True)),
                  export_overlay=bool(export.get("save_overlay", True)))

def process_image(img_path: Path, cfg: Config):
    # Read
    color = read_color(img_path)

    # Preprocess (gray + CLAHE)
    gray = preprocess_gray(color, cfg.clahe)

    # Segment
    mask = threshold_mask(gray, cfg.seg)

    # Contours + filter by area
    contours, count = find_and_filter_contours(mask, cfg.filt)

    # Visualize overlay
    overlay = draw_contour_overlay(color, contours, cfg.viz)
    overlay = put_count_text(overlay, count, cfg.viz)

    return {
        "gray": gray,
        "mask": mask,
        "overlay": overlay,
        "count": int(count),
    }

def save_outputs(img_path: Path, outputs: dict, out_dir: Path, cfg: Config):
    mask_path, overlay_path, _ = pair_output_paths(img_path, out_dir)
    ensure_dir(out_dir)
    if cfg.export_mask:
        write_image(mask_path, outputs["mask"])
    if cfg.export_overlay:
        write_image(overlay_path, outputs["overlay"])
    return mask_path, overlay_path
