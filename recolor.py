from PIL import Image as Image
import numpy as np

def recolor(og_image, target_color):


    image_len = len(og_image) 
    # Create a new blank array of the specified size
    new_array = np.zeros((image_len, image_len, 4), dtype=np.uint8)
    new_array[:, :, 3] = 0  # Set alpha channel to transparent
    
    # Recolor pixels
    for y in range(image_len):
        for x in range(image_len):
            # Get the current pixel
            current_pixel = og_image[y, x]
            
            # Check if pixel is not white or transparent
            is_not_white_or_transparent = (
                # Not transparent (alpha > 0)
                current_pixel[3] > 0 and 
                # Not white (all RGB channels at maximum)
                not np.all(current_pixel[:3] == 255)
            )
            
            if is_not_white_or_transparent:
                # Copy pixel with new color
                new_array[y, x, 0] = target_color[0]  # Red
                new_array[y, x, 1] = target_color[1]  # Green
                new_array[y, x, 2] = target_color[2]  # Blue
                new_array[y, x, 3] = current_pixel[3]  # Preserve original alpha
            else:
                # Keep original pixel if white or transparent
                new_array[y, x] = current_pixel
    
    return new_array


def is_not_white_or_transparent(pixel, white_threshold=250, alpha_threshold=10):
    return (
        pixel[3] > alpha_threshold and  # Significant opacity
        not np.all(pixel[:3] >= white_threshold)  # Not near-white
    )


def adjust_opacity(og_image, opacity_percentage):
    """
    Adjusts opacity of an image to specified %
    
    Params:
        og_image : numpy.ndarray
            Original image array in RGBA format
        opacity_percentage : float
            Desired opacity percentage (0.0 to 1.0)
    
    Returns:
        numpy.ndarray :
            Image array with adjusted opacity
    """
    # Copy original image to avoid input modification and a crash
    adjusted_image = og_image.copy()
    
    # Validate opacity percentage
    if not 0.0 <= opacity_percentage <= 1.0:
        raise ValueError("Opacity percentage must be between 0.0 and 1.0")
    
    # Calculate new alpha values
    # Multiply existing alpha channel by the opacity percentage
    adjusted_image[:, :, 3] = (adjusted_image[:, :, 3] * opacity_percentage).astype(np.uint8)
    
    return adjusted_image