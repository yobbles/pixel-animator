from PIL import Image
import numpy as np
import os
import sys

def get_valid_size():
    while True:
        size = input("Enter image size (8, 16, 32, or 64): ")
        if size in ['8', '16', '32', '64']:
            return int(size)
        print("Invalid size. Please enter 8, 16, 32, or 64.")

def get_valid_file_path():
    while True:
        file_path = input("Enter the path to your image file: ")
        if os.path.exists(file_path):
            return file_path
        print("File not found. Please enter a valid file path.")

def get_valid_output_folder():
    while True:
        folder_path = input("Enter the output folder path: ")
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Created output directory: {folder_path}")
                return folder_path
            except Exception as e:
                print(f"Error creating directory: {e}")
                continue
        # If folder exists, check if it's writable
        if os.access(folder_path, os.W_OK):
            return folder_path
        print("Cannot write to this folder. Please enter a valid folder path.")

def shift_image_left_up_wraparound(image_path, image_size):
    # Open and convert image to RGBA
    img = Image.open(image_path).convert('RGBA')
    
    # Verify image dimensions
    if img.size != (image_size, image_size):
        raise ValueError(f"Image must be {image_size}x{image_size} pixels")
    
    # Convert to numpy array
    pixel_array = np.array(img)
    
    # Create a new blank array of the specified size
    new_array = np.zeros((image_size, image_size, 4), dtype=np.uint8)
    new_array[:, :, 3] = 0  # Set alpha channel to transparent
    
    # Copy pixels with wraparound
    for y in range(image_size):
        for x in range(image_size):
            source_y = (y + 1) % image_size
            source_x = (x + 1) % image_size
            new_array[y, x] = pixel_array[source_y, source_x]
    
    return new_array

def main():
    try:
        # Get user input
        image_size = get_valid_size()
        input_path = get_valid_file_path()
        output_folder = get_valid_output_folder()
        input_filename = os.path.basename(input_path)
        for i in range(0, image_size):
            # Process the image
            
            if i > 1:
                input_path = output_path #Use previous for loops output path as input 
            try:
                shifted_array = shift_image_left_up_wraparound(input_path, image_size)
            except ValueError as e:
                print(f"Error: {e}")
                return
            except Exception as e:
                print(f"Error processing image: {e}")
                return
            
            # Create output filename
            
            filename_without_ext = os.path.splitext(input_filename)[0]
            output_path = os.path.join(output_folder, f"{filename_without_ext}_shifted-{i}.png")
            
            # Save the result
            try:
                result_image = Image.fromarray(shifted_array)
                result_image.save(output_path)
                print(f"Successfully saved shifted image to: {output_path}")
            except Exception as e:
                print(f"Error saving image: {e}")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()