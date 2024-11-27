import os
import argparse
import numpy as np
from PIL import Image
import dotenv
from typing import List

def validate_input_file(filepath: str) -> str:
    """
    Validate that the input file exists and is a file.
    
    Args:
        filepath (str): Path to the input file
    
    Returns:
        str: Absolute path to the input file
    
    Raises:
        argparse.ArgumentTypeError: If file does not exist or is not a file
    """
    # Expand user and relative paths
    full_path = os.path.abspath(os.path.expanduser(filepath))
    
    # Check if file exists and is a file (not a directory)
    if not os.path.isfile(full_path):
        raise argparse.ArgumentTypeError(f"Input file does not exist: {full_path}")
    
    return full_path

def validate_output_directory(dirpath: str) -> str:
    """
    Validate that the output directory exists and is writable.
    
    Args:
        dirpath (str): Path to the output directory
    
    Returns:
        str: Absolute path to the output directory
    
    Raises:
        argparse.ArgumentTypeError: If directory does not exist or is not writable
    """
    # Expand user and relative paths
    full_path = os.path.abspath(os.path.expanduser(dirpath))
    
    #If folder does not exist try to make one
    if not os.path.exists(full_path):
        try:
            os.makedirs(full_path)
            print(f"Created output directory: {full_path}")
            return full_path
        except Exception as e:
            print(f"Error creating directory: {e}")
            return
    # Check if directory is writable
    if not os.access(full_path, os.W_OK):
        raise argparse.ArgumentTypeError(f"Output directory is not writable: {full_path}")
    
    return full_path