import argparse
import os

from validate_files import validate_input_file,validate_output_directory
import dotenv
from typing import List, Tuple

# Load environment variables
dotenv.load_dotenv()
# Setup argument parser
def initialize_args():
    parser = argparse.ArgumentParser(description="Image Processing Utility")

    # Mandatory input file flag
    parser.add_argument(
        '-origin', 
        type=validate_input_file, 
        required=True,
        help='Path to the input image file (must exist)'
    )
    
    # Mandatory output directory flag
    parser.add_argument(
        '-destination', 
        type=validate_output_directory, 
        required=True,
        help='Directory to save the processed image (must exist and be writable)'
    )

    # Add arguments with default values from .env
    parser.add_argument(
        '--shift-size', 
        type=int, 
        default=int(os.getenv('DEFAULT_SHIFT_SIZE', 0)),  #Defaults to not shifting
        help='Pixel shift size'
    )
    parser.add_argument(
        '-opacity', 
        type=float, 
        default=float(os.getenv('DEFAULT_OPACITY', 1.0)),  #Defaults to not decreasing opacity
        help='Opacity percentage'
    )
    parser.add_argument(
        '-recolor', 
        action='store_true',  # Only applies recoloring if flag is explicitly used
        help='Enable recoloring with specified color'
    )
    parser.add_argument(
        '-color', 
        type=parse_int_list, 
        default=None,  # No default color
        help='Recolor RGB values (comma-separated)'
    )

    parser.add_argument(
        '--sprite-sheet', 
        action='store_true',
        help='for adding all output to a horizontal sprite-sheet'
    )

    return parser

def parse_int_list(s: str) -> List[int]:
    try:
        return [int(x.strip()) for x in s.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Color must be comma-separated integers")
