import numpy as np
from processImage import applyCustomColormap

def test_apply_custom_colormap():
    image_array = np.random.randint(0, 256, size=(10, 10), dtype=np.uint8)
    colored_image = applyCustomColormap(image_array)
    assert colored_image.shape == (10, 10, 3)
    assert colored_image.dtype == np.uint8
