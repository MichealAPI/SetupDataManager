import util.license_utils as license_utils
import util.upload_utils as upload_utils


def handle_menu(files_collection, licenses_collection):
    choice = print_menu()

    while choice > 6 | choice < 1:
        choice = print_menu()

    while choice != 6:

        match choice:

            # Licenses
            case 1:
                license_utils.handle_license_creation(licenses_collection)
            case 2:
                license_utils.handle_license_research(licenses_collection)
            case 3:
                license_utils.handle_license_deletion(licenses_collection)

            # Files
            case 4:
                upload_utils.handle_files_upload(files_collection)

        choice = print_menu()


def print_menu():
    print("1. New License")
    print("2. Print License")
    print("3. Delete License")
    print("4. Upload new data from a folder")
    print("5. Filtered deletion")
    print("6. Exit")
    return int(input("Enter your choice: "))


def yes_or_no():
    result = input("Would you like to proceed? [Y/N]")
    return result == "Y" or result == "y"
