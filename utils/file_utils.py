""" Handle all functions needed for file reading
YAML - Handles all YAML functions
"""
import yaml
from definitions import APP_DIR, get_current_env


def get_default_app_config():
    """ Get the app_config.yaml for default application needs
    1. Set function variables
    2. Read the YAML file
    3. Return a dictionary of the contents
    :return: Dictionary of app_config.yaml contents
    """
    # 1. Set function variables
    file_location = str(APP_DIR) + '/application/static/app_config.yaml'

    # 2. Read the YAML file
    yaml_dict = read_yaml(file_location)

    # 3. Return a dictionary of the contents
    return yaml_dict


def read_yaml(file_location):
    """ Read and return the YAML dict in the file location
    :param file_location: Absolute file path for YAML file
    :return: Dictionary of YAML file contents
    """
    with open(file_location, 'r') as stream:
        try:
            yaml_dict = yaml.load(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as e:
            print(e)  # TODO configure logger
    return yaml_dict


def write_yaml(file_location, file_contents):
    """ Write dict to YAML file in the file location
    :param file_location: Absolute file path for YAML file
    :param file_contents: Dictionary of the YAML file
    :return: TODO some type of confirmation of update success
    """
    with open(file_location, 'w') as stream:
        try:
            document = yaml.dump(file_contents, stream)
        except yaml.YAMLError as e:
            print(e)  # TODO configure logged
    return document


class YAML(object):
    """ Handling YAML functions """

    def __init__(self):
        """ Initialize class variables """
        self.env = get_current_env()
        self.sys_conf = get_default_app_config()

    def get_application_configurations(self, application):
        """ Get the configurations for the application passed
        1. Get the path of the app_config directory
        2. Get the path for the given application configuration file
        3. Read the YAML file
        4. Return the YAML file
        :param application: Required, should be a string of the name of the application to be pulled
        :return: Dictionary of the application configurations
        """
        # 1. Get the path of the app_config directory
        app_conf_dir = self.sys_conf['configs']['env'][self.env]['app_config_url']

        # 2. Get the path for the given application configuration file
        app_conf_dir += '/{file}.yaml'.format(file=application)

        # 3. Read the YAML file
        yaml_dict = read_yaml(app_conf_dir)

        # 4. Return the YAML file
        return yaml_dict
