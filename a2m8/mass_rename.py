import os
import re
def mass_rename(folder_path,old_substring,new_substring):
    for filename in os.listdir(folder_path):
        if old_substring in filename:
            new_filename = re.sub(old_substring, new_substring, filename)
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
    print ("done")
