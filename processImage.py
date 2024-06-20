import numpy as np
import matplotlib.pyplot as plt

def applyCustomColormap(imageArray):
    # Apply custom colormap (using 'viridis' as an example)
    colormap = plt.get_cmap('viridis')
    coloredImage = colormap(imageArray)
    return (coloredImage[:, :, :3] * 255).astype(np.uint8)
