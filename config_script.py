#!/usr/bin/python
""" Script to create application credentials
USAGE:
- python ./config_script.py
- python ./config_script.py [-h] [-a APPLICATION] [-u USERNAME] [-o [OVERWRITE]]
"""
from application.func.cred_manager.credential import ApplicationCredentials
from argparse import ArgumentParser
from getpass import getpass
from utils.logger import logger

# GLOBAL VARS
APP_CREDS = ApplicationCredentials()
PARSER = ArgumentParser()