""" Handling the credentials for system requirements
- Create the credentials
    - Encrypt password (encryption key should be configurable value)
- Validate the successful creation of the record
    - After creation, select the successful record
- Get the credentials for a given user
    - Validate password is correct
"""
from utils.file_utils import YAML
from utils.encryption_utils import generate_user_dict_for_app_config, validate_pass_hash
from utils.logger import logger


class ApplicationCredentials(object):
    """ Generate the credentials for a user """

    def __init__(self):
        """ Initialize class variables """
        self.yaml = YAML()

    def create_update_application_credentials(self, application, user_dict, overwrite=False):
        """ Generate new credentials for an application
        1. Encrypt user password
        2. Check to see if the application has a file
            a. If file exists, get current file contents
        3. If no file, generate new file with contents
        4. Check if record exists already
            a. If record does not exist, create
            b. If record does exist, validate overwrite
                i. If overwrite set overwrite
                ii. Else expected overwrite failure
        5. Write the file back saving the changes
        :param application: The application that the credentials are being generated for
        :param user_dict: The new dictionary that is going to be added
        :param overwrite: Overwrite the existing credential
        :return: If overwrite scenario, return overwrite validation, else, add the credential
        """
        # 1. Encrypt user password
        user_dict = generate_user_dict_for_app_config(**user_dict)

        # 2. Check to see if the application has a file
        if self.yaml.check_for_application_file(application):
            if 'profiles' in self.yaml.get_application_configurations(application):
                logger.info('Getting existing configs for %s' % application)
                contents = self.yaml.get_application_configurations(application)
            else:
                contents = {
                    'profiles': {
                        user_dict['user']: {
                            'user': user_dict['user'],
                            'password': user_dict['password']
                        }
                    }
                }
                chk = self.yaml.write_application_configuration(application, contents)
                logger.info('Profile Created: %s' % user_dict['user'])
                return {'code': 201, 'message': 'User created successfully', 'success': chk}

        # 3. If no file, generate new file with contents
        else:
            contents = {
                'profiles': {
                    user_dict['user']: {
                        'user': user_dict['user'],
                        'password': user_dict['password']
                    }
                }
            }
            chk = self.yaml.write_application_configuration(application, contents)
            logger.info('Profile Created: %s' % user_dict['user'])
            return {'code': 201, 'message': 'User created successfully', 'success': chk}

        # 4. Check if record exists already
        users = []
        for profile in contents['profiles']:
            username = contents['profiles'][profile]['user']
            users.append(username)
        if user_dict['user'] in users:
            if overwrite:
                contents['profiles'][user_dict['user']]['password'] = user_dict['password']
            else:
                return {'code': 403, 'message': 'Overwrite flag needs to be set', 'success': False}
        else:
            contents['profiles'][user_dict['user']] = {
                'user': user_dict['user'],
                'password': user_dict['password']
            }

        # 5. Write the file back saving the changes
        chk = self.yaml.write_application_configuration(application, contents)
        if chk:
            logger.info('Profile Change: %s' % user_dict['user'])
            return {'code': 200, 'message': 'Existing file has been updated', 'success': True}

    def validate_application_credentials(self, application, user_dict):
        """ Validate application credentials to what is saved in the YAML configuration
        1. Verify that the file is available
            a. If no file, return with error
        2. Validate the password against the hashed value for the password
            a. If password correct, return success
            b. If password incorrect, return failure
        :param application:
        :param user_dict:
        :return:
        """
        # 1. Verify that the file is available
        if self.yaml.check_for_application_file(application):
            contents = self.yaml.get_application_configurations(application)
        else:
            logger.error('Application configuration file not found: %s' % application)
            return {'code': 404, 'message': 'Application configuration file not found', 'success': False}

        # 2. Validate the password against the hashed value for the password
        if user_dict['user'] in contents['profiles']:
            pass_hash = contents['profiles'][user_dict['user']]['password']
        else:
            logger.error('User not found: %s' % user_dict['user'])
            return {'code': 404, 'message': 'Application configuration user not found', 'success': False}
        if validate_pass_hash(user_dict['password'].encode('utf8'), pass_hash):
            logger.info('User validated: %s' % user_dict['user'])
            return {'code': 202, 'message': 'Password match', 'success': True}
        else:
            logger.info('User invalid password: %s' % user_dict['user'])
            return {'code': 401, 'message': 'Password does not match', 'success': False}
