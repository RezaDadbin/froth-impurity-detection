# 🫧 Froth Impurity Detector

## 📘 Overview

**Froth Impurity Detector** is a computer vision project using **OpenCV** and **Python** to detect and count impurities (dark particles) in froth or foam images. 
It works completely offline and automatically generates binary masks, overlay images, and CSV summaries.

---

## ⚙️ How It Works

1. **Preprocessing:** Converts images to grayscale and applies CLAHE to enhance contrast.
2. **Dynamic Thresholding:** Computes a threshold `T = mean - k * std` to segment dark regions.
3. **Morphology:** Performs a small open operation to remove noise, then inverts the binary mask.
4. **Contour Filtering:** Finds all contours and filters by area to count impurities.
5. **Visualization:** Draws red contours over the original image and writes impurity counts.

---

## 🧰 Installation

```bash
git clone https://github.com/<your-username>/froth-impurity-detector.git
cd froth-impurity-detector
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🖥️ Usage

### ▶️ Process a Single Image

Run this **from the project root** (where `src/` is located):

```bash
python -m src.froth_impurity.cli --image data/input/froth_sample1.jpg --cfg configs/default.yaml
```

This will generate:
- `data/output/froth_sample1_mask.png` → binary impurity mask  
- `data/output/froth_sample1_overlay.png` → annotated image with contours  
- `data/output/results.csv` → table with impurity counts  

### 📁 Process an Entire Folder

```bash
python -m src.froth_impurity.cli --folder data/input --cfg configs/default.yaml
```

All `.jpg`, `.png`, and `.tif` images in `data/input/` will be processed.  
Results will appear in `data/output/` automatically.

---

## ⚙️ Configuration (`configs/default.yaml`)

```yaml
paths:
  input_dir: "data/input"
  output_dir: "data/output"

preprocess:
  clahe:
    enabled: true
    clip_limit: 2.0
    tile_grid_size: 8

segment:
  k_dynamic: 0.834
  invert: true
  morph_open_kernel: 2
  morph_open_iterations: 1

filter:
  min_area_px: 5
  max_area_px: 11

visualize:
  overlay_color: [255, 0, 0]
  overlay_thickness: 1
  alpha_overlay: 0.35
```

You can edit this file to fine-tune detection behavior.

---

## 📂 Folder Layout

```
froth-impurity-detector/
├── configs/
│   └── default.yaml
├── src/froth_impurity/
│   ├── cli.py
│   ├── pipeline.py
│   ├── segmentation.py
│   ├── preprocessing.py
│   ├── visualize.py
│   └── contours.py
├── data/
│   ├── input/   ← put your froth images here
│   └── output/  ← results saved here
└── requirements.txt
```

---

## 📦 Data Folders

- **`data/input/`** → place your test images here, e.g.
  ```
  data/input/
  ├── froth_sample1.jpg
  ├── froth_sample2.png
  ```

- **`data/output/`** → created automatically when you run the script.
  It will contain:
  ```
  data/output/
  ├── froth_sample1_mask.png
  ├── froth_sample1_overlay.png
  └── results.csv
  ```

---

## 🧠 Tips

- Increase `segment.k_dynamic` → detects fewer (stricter) impurities.  
- Decrease `segment.k_dynamic` → detects more impurities.  
- If impurities appear **bright**, set `segment.invert: false`.  
- Adjust `filter.min_area_px` / `max_area_px` for your particle size.  

---

## 🧑‍💻 Author

- **Reza Dadbin** — GitHub: https://github.com/RezaDadbin
- **Sina Lotfi** — GitHub: https://github.com/cinaLotfi

---

## 🏁 Summary

A fully local, configurable OpenCV pipeline for impurity detection in froth surfaces.  
Accurate, extendable, and perfect for research or production-level froth analysis.

---
