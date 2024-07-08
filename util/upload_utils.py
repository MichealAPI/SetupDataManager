import base64
import os

import util.config_utils as config_utils
import util.time_utils as time_utils


def upload_file(file_path, upload_folder_path, files_collection):
    """
    Uploads a single file to the database.
    :param file_path:  The path of the file to upload.
    :param upload_folder_path:  The path of the upload folder.
    :param files_collection:  The collection to insert the file into.
    :return:
    """
    # Convert file_path and upload_folder_path to absolute paths
    abs_file_path = os.path.abspath(file_path)
    abs_upload_folder_path = os.path.abspath(upload_folder_path)

    # Calculate the relative path of the file with respect to the upload folder
    relative_path = os.path.relpath(abs_file_path, start=abs_upload_folder_path)

    if not relative_path.endswith(".yml") and not relative_path.endswith(".yaml"):
        print(f"Skipping {file_path} as it is not a YAML file.")
        return False

    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    parsed_path = relative_path.replace("\\", "/")

    files_collection.insert_one({
        "millis": time_utils.current_milli_time(),
        "path": parsed_path,
        "content": base64.b64encode(bytes(data, 'utf-8')).decode('utf-8')
    })

    return True


def list_files_recursively_and_upload(folder_path, files_collection, config):
    """
    Recursively lists all files in a given folder and its subfolders and uploads them to the database.
    :param folder_path:  The folder path to list files from.
    :param files_collection:  The collection to insert the files into.
    :param config:  The configuration dictionary.
    :return:
    """
    # Ensure folder_path is a string
    folder_path_str = str(folder_path)
    upload_folder = config.get('upload-folder', '')
    # Ensure upload_folder is a string and construct the upload_folder_path
    upload_folder_path = os.path.join(folder_path_str, str(upload_folder))

    if not os.path.exists(upload_folder_path):
        print("Upload folder does not exist.")
        return 0

    file_count = 0
    for root, dirs, files in os.walk(upload_folder_path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if upload_file(file_path, upload_folder_path, files_collection):
                    file_count += 1
            except Exception as e:
                print(f"Failed to upload {file}: {e}")
    return file_count


def handle_files_upload(files_collection):
    """
    Function to handle the upload of files.
    :param files_collection:  The collection to insert the files into.
    :return:  None
    """
    default_path = os.path.abspath('data')
    folder_path_input = input("Enter the folder path or press Enter to use the default: ").strip()
    folder_path = os.path.abspath(folder_path_input) if folder_path_input else default_path

    try:
        print(os.listdir(folder_path))
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied to access the folder '{folder_path}'.")

    config = config_utils.load_config(folder_path)
    if config is None:
        print("config.yml not found in the specified folder.")
        return

    uploaded_files_count = list_files_recursively_and_upload(folder_path, files_collection, config)
    print(f"Uploaded {uploaded_files_count} files.")
