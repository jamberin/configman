""" Handle all functions needed for file reading
YAML - Handles all YAML functions
"""

import yaml
from definitions import APP_DIR


class YAML(object):
    """ Handling YAML functions """

    def __init__(self):
        """ Initialize class variables """



    def get_default_app_config(self):
        """ Get the app_config.yaml for default application needs
        1. Set function variables
        2. Read the YAML file
        3. Return a dictionary of the contents
        :return: Dictionary of app_config.yaml contents
        """
        # 1. Set function variables
        file_location = str(APP_DIR) + '/application/static/app_config.yaml'

        # 2. Read the YAML file
        with open(file_location, 'r') as stream:
            try:
                yaml_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # 3. Return a dictionary of the contents
        return yaml_dict