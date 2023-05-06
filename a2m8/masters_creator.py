import os
import glob
import io
import win32com.client as win32
import pandas as pd
import shutil
import sys
import openpyxl

def convert_word_to_pdf(file):
    """Convert a Word document to PDF"""
    word = win32.gencache.EnsureDispatch('Word.Application')
    print(f"converting {file} to pdf")
    doc = word.Documents.Open(file)
    doc.SaveAs(os.path.splitext(file)[0] + ".pdf", FileFormat=win32.constants.wdFormatPDF)
    print(f"converted {file} to pdf")
    doc.Close(False)
    os.remove(file)
    word.Quit()

def rename_files(folder, collection_id):
    """Rename files in the folder in chronological order starting with 2022_{collection_id}_001"""
    extensions = ["tiff","tif","jpg", "jpeg", "png", "bmp", "gif", "pdf", "mp3", "wav", "wma","m4a"]
    counter = 1
    for ext in extensions:
        files = glob.glob(os.path.join(folder, f"*.{ext}"))
        for file in files:
            if os.path.basename(file) == os.path.basename(__file__):
                continue
            old_name = os.path.basename(file)
            new_name = f"{collection_id}_{counter:03}.{ext}"
            os.rename(file, os.path.join(folder, new_name))
            print(f"{old_name} renamed to {new_name}")
            counter += 1

def arrange_files(folder):
    """Arrange files in the folder in the order of Photos>pdf>audio files"""
    extensions = ["tiff","tif","jpg", "jpeg", "png", "bmp", "gif", "pdf", "mp3", "wav", "wma","m4a"]
    order = ["tiff","tif","jpg", "jpeg", "png", "bmp", "gif", "pdf", "mp3", "wav", "wma","m4a"]
    for ext in order:
        files = glob.glob(os.path.join(folder, f"*.{ext}"))
        for file in files:
            old_name = os.path.basename(file)
            new_name = f"{order.index(ext)+1:03}_{os.path.basename(file)}"
            os.rename(file, os.path.join(folder, new_name))
            print(f"{old_name} renamed to {new_name}")


def save_file_names(folder, collection_id):
    """Save original and new file names to an Excel file"""
    extensions = ["tiff","tif","jpg", "jpeg", "png", "bmp", "gif", "pdf", "mp3", "wav", "wma","m4a"]
    data = {"Old Name": [], "New Name": []}
    counter = 1

    for ext in extensions:
        files = glob.glob(os.path.join(folder, f"*.{ext}"))
        for file in files:
            old_name = os.path.basename(file)
            old_name = old_name[4:]
            new_name = f"{collection_id}_{counter:03}.{ext}"
            data["Old Name"].append(old_name)
            data["New Name"].append(new_name)
            counter += 1
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(folder, f"file_names_{collection_id}.xlsx"), index=False)

def create_master(masterspath, collection_id):
    
    for file in os.listdir(masterspath):
        if os.path.splitext(file)[1] == ".docx" or os.path.splitext(file)[1] == ".doc":
            doc = os.path.join(masterspath, file).replace("/","\\")
            #doc = r'{}'.format(doc)
            print("hrllo")
            print( doc)
            convert_word_to_pdf(doc)

    arrange_files(masterspath)
    save_file_names(masterspath, collection_id)
    rename_files(masterspath, collection_id)
    