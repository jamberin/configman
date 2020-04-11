""" Application definitions that are used throughout the system """
import os
import pathlib
APP_DIR = pathlib.Path(__file__).parent.absolute()


# TODO Configure better
def get_current_env():
    """
    Returns the string of the current environment
    :return: String of current environment
    """
    if os.environ.get('ENVIRONMENT'):
        environment = os.environ.get('ENVIRONMENT')
    else:
        environment = 'LOCAL'
    return environment

