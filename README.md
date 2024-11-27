# pixel-animator
Open-source tool for animating pixel art stills

must import: 
argparse, dotenv, PIL, numpy

options:
  -h, --help            show this help message and exit
  -origin ORIGIN        Path to the input image file (must exist)
  -destination DESTINATION
                        Directory to save the processed image (must exist and be writable)
  --shift-size SHIFT_SIZE
                        Pixel shift size
  -opacity OPACITY      Opacity percentage
  -recolor              Enable recoloring with specified color
  -color COLOR          Recolor RGB values (comma-separated)
  --sprite-sheet        for adding all output to a horizontal sprite-sheet
