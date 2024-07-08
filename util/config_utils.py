import yaml
import os


def load_config(folder_path):
    config_path = os.path.join(folder_path, "config.yml")
    if os.path.exists(config_path):

        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        return None
