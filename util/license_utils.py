import random
import string
import util.time_utils as time_utils


def delete_license(license_key, licenses_collection):
    """
    Function to delete a license by its key.
    :param license_key: The key of the license to delete.
    :param licenses_collection: The collection to delete the license from.
    :return: A boolean indicating the success of the operation.
    """
    count = licenses_collection.count_documents(
        {"licenseKey": license_key}
    )

    if count == 0:
        print("No license found")
        return False
    elif count == 1:
        licenses_collection.delete_one({"licenseKey": license_key})
        return True
    elif count > 1:
        print("More than one license found, aborting dangerous operation...")
        return False


def input_license():
    """
    Function to input a license.
    :return: The target name, the current millis and the license key.
    """
    target = input("Enter target name: ")
    millis = time_utils.current_milli_time()
    license_key = generate_random_license()

    return target, millis, license_key


def create_license(licenses_collection):
    """
    Insert a license into the database.
    :param licenses_collection: The collection to insert the license into.
    :return: A message indicating the success of the operation.
    """
    target, millis, license_key = input_license()

    licenses_collection.insert_one(
        {"target": target,
         "millis": millis,
         "licenseKey": license_key}
    )

    print("Creating license...")
    return "Created license for target " + target + " with license key " + license_key


def find_license(license_key, licenses_collection):
    """
    Function to find a license by its key.
    """
    return licenses_collection.find(
        {"licenseKey": license_key}
    )


def generate_random_license():
    """
    Generates a random license key
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


# Menu operations

def handle_license_creation(licenses_collection):
    print(create_license(licenses_collection))


def handle_license_deletion(licenses_collection):
    license_key = str(input("Enter a license key: "))
    success = delete_license(license_key, licenses_collection)

    if success:
        print("Your license key has been successfully deleted")
    else:
        print("An error has occurred while deleting license key '", license_key, "'")


def handle_license_research(licenses_collection):
    license_key = str(input("Enter a license key: "))
    print(find_license(license_key, licenses_collection))
