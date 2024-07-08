import os


def list_files_recursively(folder_path):
    """
    Recursively lists all files in a given folder and its subfolders.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            yield os.path.join(root, file)


def upload_file(file_path, files_collection, config):
    """
    Uploads a single file to the database.
    """
    with open(file_path, 'r') as file:
        data = file.read()

    # Normalize the path to use forward slashes
    parsed_path = os.path.dirname(file_path).replace("\\", "/")

    files_collection.insert_one({
        "locale": config['locale'].lower(),
        "content": data,
        "path": parsed_path,
        "file_name": os.path.basename(file_path)
    })
