import os


def list_files_recursively(folder_path):
    """
    Recursively lists all files in a given folder and its subfolders.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            yield os.path.join(root, file)
