import os
from PIL import Image

# Ask user for path
path = input("Enter path to directory: ")

# Loop through all files in directory
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    # Check if file is a TIFF
    if os.path.isfile(filepath) and filename.lower().endswith('.tif'):
        print(f"Processing {filename}...")
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
        print(f"Deleted {filename}")
