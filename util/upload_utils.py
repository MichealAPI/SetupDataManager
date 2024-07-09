import base64
import os

import util.config_utils as config_utils
import util.time_utils as time_utils


def insert_embedded_document(file_paths, upload_folder_path, config, files_collection):
    """
    Uploads a single file to the database.
    :param file_paths: The path of the file to upload.
    :param config:  The configuration dictionary.
    :param upload_folder_path:  The path of the upload folder.
    :param files_collection:  The collection to insert the file into.
    :return:
    """

    document_array = []

    for file_path in file_paths:
        # Convert file_path and upload_folder_path to absolute paths
        abs_file_path = os.path.abspath(file_path)
        abs_upload_folder_path = os.path.abspath(upload_folder_path)

        # Calculate the relative path of the file with respect to the upload folder
        relative_path = os.path.relpath(abs_file_path, start=abs_upload_folder_path)

        parsed_path = relative_path.replace("\\", "/")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

        document_array.append({
            "path": parsed_path,
            "content": base64.b64encode(bytes(data, 'utf-8')).decode('utf-8')
        })

    locale = config['locale']
    product = config['product']

    files_collection.insert_one({
        "locale": locale,
        "product": product,
        "millis": time_utils.current_milli_time(),
        "files": document_array
    })


def list_files_recursively_and_upload(folder_path, files_collection, config):
    """
    Recursively lists all files in a given folder and its subfolders and uploads them to the database.
    :param folder_path:  The folder path to list files from.
    :param files_collection:  The collection to insert the files into.
    :param config:  The configuration dictionary.
    :return:
    """

    embedded_documents_array = []

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
            file_path = os.path.join(root, file)
            if is_valid_file(file_path):
                file_count += 1
                embedded_documents_array.append(file_path)
            else:
                print(f"Skipping {file_path} as it is not a YAML file.")

    insert_embedded_document(
        embedded_documents_array,
        upload_folder_path,
        config,
        files_collection
    )
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
    print(f"Uploading {uploaded_files_count} files.")


def is_valid_file(path):
    valid_extensions = ['.yml', '.yaml']

    return any(path.endswith(ext) for ext in valid_extensions)
