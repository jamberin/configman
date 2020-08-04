#!/usr/bin/python
""" Script to create application credentials
USAGE:
- python ./cred_script.py
- python ./cred_script.py [-h] [-a APPLICATION] [-u USERNAME] [-o [OVERWRITE]]
"""
from application.func.cred_manager.credential import ApplicationCredentials
from argparse import ArgumentParser
from getpass import getpass
from utils.logger import logger

# GLOBAL VARS
APP_CREDS = ApplicationCredentials()
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
PARSER.add_argument('-a', '--application', help='The app that the credential is to be created for', required=False)
PARSER.add_argument('-u', '--username', help='The username of the user to be generated', required=False)
PARSER.add_argument('-o', '--overwrite', help='Overwrite the current password that is set', default=False, type=bool,
                    nargs='?')
ARGS = PARSER.parse_args()
APP = ARGS.application
USER = ARGS.username
SUPER = ARGS.overwrite

# SCRIPT
# App splash
logger.info('\n')
logger.info("                               d8b")
logger.info("                               88P")
logger.info("                              d88")
logger.info("   d8888b  88bd88b d8888b d888888    88bd8b,d88b  d888b8b    88bd88b")
logger.info("  d8P' `P  88P'  `d8b_,dPd8P' ?88    88P'`?8P'?8bd8P' ?88    88P' ?8b")
logger.info("  88b     d88     88b    88b  ,88b  d88  d88  88P88b  ,88b  d88   88P")
logger.info("  `?888P'd88'     `?888P'`?88P'`88bd88' d88'  88b`?88P'`88bd88'   88b")
logger.info('\n')

# Validate arguments
if APP is None:
    APP = input('Please enter the name of the application: ')
if USER is None:
    USER = input('Please enter the username for the new user: ')
PASS = getpass(prompt='Please enter the password for the new user: ')
USER_DICT = {
    'user': USER,
    'password': PASS
}
RESPONSE = APP_CREDS.create_update_application_credentials(application=APP, user_dict=USER_DICT, overwrite=SUPER)
handle_response(RESPONSE)
