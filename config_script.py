#!/usr/bin/python
""" Script to create application credentials
USAGE:
- python ./config_script.py
- python ./config_script.py [-h] [-a APPLICATION] [-u USERNAME] [-o [OVERWRITE]]
"""
from application.func.cred_manager.configs import ApplicationConfigs
from argparse import ArgumentParser
from utils.logger import logger

# GLOBAL VARS
APP_CONF = ApplicationConfigs()
PARSER = ArgumentParser()


# FUNCTIONS
def handle_response(response):
    """ Handles the default response from the create application creds function """
    if response['success']:
        logger.info('Code: %s' % str(response['code']))
        logger.info(response['message'])
        logger.info('Exit Code: 0')
        exit(0)
    else:
        logger.error('Code: %s' % str(response['code']))
        logger.error(response['message'])
        logger.info('Exit Code: 1')
        exit(1)


# ARGUMENT PARSER
PARSER.add_argument('-a', '--application', help='The app that the configuration is to be created for', required=False)
PARSER.add_argument('-u', '--username', help='The username of the user to be generated', required=False)
PARSER.add_argument('-t', '--config_type', help='The type of configuration to be created', required=False)
PARSER.add_argument('-k', '--config_key', help='The key for the configuration to be generated', required=False)
PARSER.add_argument('-o', '--overwrite', help='Overwrite the current password that is set', default=False, type=bool,
                    nargs='?')
ARGS = PARSER.parse_args()
APP = ARGS.application
USER = ARGS.username
TYPE = ARGS.config_type
CONF = ARGS.config_key
SUPER = ARGS.overwrite

# SCRIPT
# App splash
logger.info('\n')
logger.info(" dP''b8  dP'Yb  88b 88 888888 88  dP''b8 8b    d8    db    88b 88 ")
logger.info("dP   `' dP   Yb 88Yb88 88__   88 dP   `' 88b  d88   dPYb   88Yb88 ")
logger.info("Yb      Yb   dP 88 Y88 88''   88 Yb  '88 88YbdP88  dP__Yb  88 Y88 ")
logger.info(" YboodP  YbodP  88  Y8 88     88  YboodP 88 YY 88 dP''''Yb 88  Y8 ")
logger.info('\n')

# Validate arguments
if APP is None:
    APP = input('Please enter the name of the application: ')
if USER is None:
    USER = input('Please enter the username consuming the configuration: ')
if TYPE is None:
    TYPE = input('Please enter the type of configuration to be created: ')
if CONF is None:
    CONF = input('Please enter the configuration key to be generated: ')
VALUE = input('Enter the value of the new configuration: ')
CONF_DICT = {
    CONF: VALUE
}
RESPONSE = APP_CONF.create_update_application_configuration(application=APP, user=USER, config_type=TYPE,
                                                            config_dict=CONF_DICT, overwrite=SUPER)
handle_response(RESPONSE)