from __future__ import annotations
import argparse
from pathlib import Path
import csv
from .io import list_images, pair_output_paths
from .pipeline import load_config, process_image, save_outputs

def _write_csv_header(csv_path: Path):
    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["filename", "count"])

def _append_csv(csv_path: Path, filename: str, count: int):
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([filename, count])

def run_image(image_path: Path, cfg_path: Path):
    cfg = load_config(cfg_path)
    outputs = process_image(image_path, cfg)
    save_outputs(image_path, outputs, cfg.paths.output_dir, cfg)
    # also write CSV for single image
    _, _, csv_path = pair_output_paths(image_path, cfg.paths.output_dir)
    _write_csv_header(csv_path)
    _append_csv(csv_path, image_path.name, outputs["count"])
    print(f"[OK] {image_path.name}: count={outputs['count']}")

def run_folder(folder: Path, cfg_path: Path):
    cfg = load_config(cfg_path)
    images = list_images(folder)
    if not images:
        print(f"[WARN] No images found in {folder}")
        return
    # folder-level CSV
    _, _, csv_path = pair_output_paths(images[0], cfg.paths.output_dir)
    _write_csv_header(csv_path)
    for p in images:
        outputs = process_image(p, cfg)
        save_outputs(p, outputs, cfg.paths.output_dir, cfg)
        _append_csv(csv_path, p.name, outputs["count"])
        print(f"[OK] {p.name}: count={outputs['count']}")
    print(f"[DONE] Results -> {csv_path.parent}")

def main():
    ap = argparse.ArgumentParser(description="Froth impurity detector (OpenCV).")
    ap.add_argument("--cfg", type=Path, default=Path("configs/default.yaml"))
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--image", type=Path, help="Path to a single image")
    g.add_argument("--folder", type=Path, help="Path to a folder of images")
    args = ap.parse_args()

    if args.image:
        run_image(args.image, args.cfg)
    else:
        run_folder(args.folder, args.cfg)

if __name__ == "__main__":
    main()
