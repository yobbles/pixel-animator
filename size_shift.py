# File meant for all resizing of the gifs 

import numpy as np

def expand_image(original_image, y):
    """
    Expand a numpy image by adding y rows and columns to the end.
    
    Parameters:
    -----------
    original_image : numpy.ndarray
        The input n x n numpy array to be expanded
    y : int
        Number of rows and columns to add
    
    Returns:
    --------
    numpy.ndimage
        A (n+y) x (n+y) numpy array with added rows and columns
    """
    # Check if the input is a numpy array
    if not isinstance(original_image, np.ndarray):
        raise ValueError("Input must be a numpy array")
    
    # Ensure we're working with a 3D array (height, width, channels)
    if original_image.ndim != 3:
        raise ValueError(f"Input must be a 3D array, got {original_image.ndim} dimensions")
    
    # Get the original dimensions
    height, width, channels = original_image.shape
    
    # For RGBA images, create an expanded array with full transparency
    expanded = np.zeros((height + y, width + y, channels), dtype=original_image.dtype)
    
    # This sets the alpha channel to 0 (fully transparent) for new areas
    expanded[:, :, 3] = 0
    
    # Copy the original image data
    expanded[:height, :width, :] = original_image
    
    return expanded