import os

from pymongo import MongoClient

from util.menu_utils import handle_menu
from util.config_utils import load_config


def main():

    print("\033[93mLoading... Please wait until the menu is displayed.")

    files_collection, licenses_collection = init_database()

    print("\033[92mLoaded successfully!\033[0m")

    return handle_menu(files_collection, licenses_collection)


def init_database():
    base_config = load_config(os.getcwd())

    if base_config is None:
        print("No config file found")
        return

    client = MongoClient(base_config['mongo-uri'])
    db = client[base_config['database']]
    licenses_collection = db['licenses-collection']
    files_collection = db['files-collection']

    return files_collection, licenses_collection


if __name__ == '__main__':
    main()
