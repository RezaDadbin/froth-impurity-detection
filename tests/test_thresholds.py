import numpy as np
from src.froth_impurity.segmentation import SegmentParams, threshold_mask

def test_dynamic_threshold_runs():
    # synthetic gradient image
    gray = np.linspace(0, 255, 256, dtype=np.uint8).reshape(16, 16)
    p = SegmentParams(method="dynamic", k_dynamic=0.8, invert=True, morph_open_kernel=0, morph_open_iterations=0)
    m = threshold_mask(gray, p)
    assert m.shape == gray.shape
    assert m.dtype == np.uint8
