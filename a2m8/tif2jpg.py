import os
from PIL import Image
from PyQt5 import QtWidgets, QtCore

def do_tif2jpg(path, terminal):
    # Loop through all files in directory
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        # Check if file is a TIFF
        if os.path.isfile(filepath) and filename.lower().endswith('.tif'):
            terminal.appendPlainText(f"Processing {filename}...")
            # Open TIFF image
            img = Image.open(filepath)

            # Convert to JPEG
            new_filename = os.path.splitext(filename)[0] + ".jpg"
            new_filepath = os.path.join(path, new_filename)
            img.save(new_filepath)

            # Close image file
            img.close()

            # Remove original file
            os.remove(filepath)
            terminal.appendPlainText(f"Deleted {filename}")
