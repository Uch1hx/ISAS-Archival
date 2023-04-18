from PIL import Image
import os

# set the maximum file size in bytes (1 MB = 1,000,000 bytes)
max_size = 1000000

# set the directory path where the images are stored
directory_path = input("Enter Path: ")

# loop through all the files in the directory
for filename in os.listdir(directory_path):
    filepath = os.path.join(directory_path, filename)
    
    # check if the file is an image
    if filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".png"):
        # open the image
        img = Image.open(filepath)
        
        # get the current file size
        current_size = os.path.getsize(filepath)
        
        # if the current file size is already under 1 MB, skip this file
        if current_size <= max_size:
            continue
        
        # get the current quality value or set a default value of 80
        quality = img.info.get('quality', 90)
        
        # reduce the quality of the image until it is under 1 MB
        while current_size > max_size:
            img.save(filepath, optimize=True, quality=quality-10)
            print("Processing...",filename)
            current_size = os.path.getsize(filepath)
            quality -= 10
        
        # close the image
        img.close()
