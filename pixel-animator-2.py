import numpy as np
import os
import sys
from PIL import Image

from size_shift import expand_image
from input_args import initialize_args
from recolor import * 

def shift_image_left_up_wraparound(og_array, image_size):

    
    # Create a new blank array of the specified size
    new_array = np.zeros((image_size, image_size, 4), dtype=np.uint8)
    new_array[:, :, 3] = 0  # Set alpha channel to transparent
    
    # Copy pixels with wraparound
    for y in range(image_size):
        for x in range(image_size):
            source_y = (y + 1) % image_size
            source_x = (x + 1) % image_size
            new_array[y, x] = og_array[source_y, source_x]
    
    return new_array

def main():
    parser = initialize_args()      #Get the flags that the user set, either in the .env file or manually in command line
    args = parser.parse_args()
    print(args)
    #Open the file to get file size
    try:
        img = Image.open(args.origin).convert('RGBA')           # Open and convert image to RGBA
        image_width, image_height = img.size
        image_size = image_width * image_height  # Total number of pixels

        # Convert  image to numpy array
        pixel_array = np.array(img)
    except FileNotFoundError: print(f"Error: File not found at {args.origin}"); sys.exit(1) #Make sure file is at filepath
    except IOError: print(f"Error: Unable to open image file at {args.origin}"); sys.exit(1) #Make sure file is readable

    if args.opacity < 1: 
        #We call the opacity function
        print("opacity called")
        pixel_array = adjust_opacity(pixel_array, args.opacity) #only adjust opacity once, otherwise image dissapears
    
    #Enlarge the image if called with enlarge flag. 
    if args.shift_size > 0:
        print("shift_size called")
        pixel_array = expand_image(pixel_array, args.shift_size)
        image_height += args.shift_size # Increase image size to reflect current size

    if args.recolor:
        pixel_array = recolor(pixel_array, args.color)

    
    input_path = args.origin
    master_array = np.array([])#For spritesheet
    save_file = True
    for i in range(0, image_height):

        try:
            pixel_array = shift_image_left_up_wraparound(pixel_array, image_height)

        except ValueError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Error processing image: {e}")
            return
            

        if args.sprite_sheet:
            master_array = horizontal_concat(master_array, pixel_array)
            print("master arr", master_array.size)
            print("i", i )
            #Check if this is the last time we shift. If it is, we need to save spritesheet into file. Else we keep going. 
            if i == image_height - 1:
                save_file = True
            else:
                save_file = False

        if save_file: 
        
            # Create output filename
                
            filename_without_ext = os.path.splitext(args.origin)[0]
            filename_without_ext = filename_without_ext.split('\\')[-1] 
            print("filename", filename_without_ext)
            output_path = os.path.join(args.destination, f"{filename_without_ext}_{i}.png")
                
                # Save the result
            try:

                result_image = Image.fromarray(master_array)
                result_image.save(output_path)
                print(f"Successfully saved {filename_without_ext}_{i}.png to: {args.destination}")
            except Exception as e:
                print(f"Error saving image: {e}")
                
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                sys.exit(1)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                sys.exit(1)



def horizontal_concat(arr1, arr2):
    if arr1.size == 0:
        return arr2
    if arr1.shape[0] != arr2.shape[0]:
        raise ValueError("Arrays must have the same number of rows")
    return np.hstack((arr1, arr2))



if __name__ == "__main__":
    main()
