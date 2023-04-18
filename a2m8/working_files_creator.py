import os
import sys
from PIL import Image
import PyPDF2
import io
from pdf2image import convert_from_path
import PIL
import shutil

PIL.Image.MAX_IMAGE_PIXELS = 933120000


def working_files(path):
    input_folder_path = path
    output_folder_path = os.path.join(parent_dir, "Working Files")
    os.mkdir(output_folder_path)
    count = 0
    if not os.path.isdir(input_folder_path):
        print("Invalid input folder path.")
        sys.exit()

    if not os.path.isdir(output_folder_path):
        print("Invalid output folder path.")
        sys.exit()

    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)
        count += 1
        print(count)
        if os.path.isfile(file_path) and file_path.lower().endswith(".pdf"):
            try:
                images = convert_from_path(file_path)
                output_file_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + '.tiff')
                images[0].save(output_file_path, format='TIFF')
            except PIL.Image.DecompressionBombError:
                output_file_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + '_unchanged.pdf')
                shutil.copy2(file_path, output_file_path)
        elif os.path.isfile(file_path) and file_path.lower().endswith(".tif"):
            output_file_path = os.path.join(output_folder_path, os.path.basename(file_path))
            Image.open(file_path).save(output_file_path)
    print("DONE")


