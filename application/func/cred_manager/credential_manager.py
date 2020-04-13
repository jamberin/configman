""" Handling the credentials for system requirements
- Create the credentials
    - Encrypt password (encryption key should be configurable value)
- Validate the successful creation of the record
    - After creation, select the successful record
- Get the credentials for a given user
    - Validate password is correct
"""
from utils.file_utils import YAML


class GenerateCredentials(object):
    """ Generate the credentials for a user """

    def __init__(self):
        """ Initialize class variables """
        self.yaml = YAML()

    def create_update_application_credentials(self, application, user_dict, overwrite=False):
        """ Generate new credentials for an application
        1. Check to see if the application has a file
            a. If no file, generate new file with contents
        2. If file exists, get current file contents
        3. Check if record exists already
            a. If record does not exist, create
            b. If record does exist, validate overwrite
                i. If overwrite set overwrite
                ii. Else expected overwrite failure
        4. Write the file back saving the changes
        :param application: The application that the credentials are being generated for
        :param user_dict: The new dictionary that is going to be added
        :param overwrite: Overwrite the existing credential
        :return: If overwrite scenario, return overwrite validation, else, add the credential
        """
        # 1. Check to see if the application has a file
        if self.yaml.get_application_configurations(application) is not None:
            contents = self.yaml.get_application_configurations(application)

        # 2. If file exists, get current file contents
        else:
            contents = {}
            contents['profiles'][user_dict['user']] = user_dict['password']
            chk = self.yaml.write_application_configuration(application, content=user_dict)
            return {'code': 201, 'message': 'User created successfully', 'success': chk}

        # 3. Check if record exists already
        users = []
        for profile in contents['profiles']:
            users.append(profile['user'])
        if user_dict['user'] in users:
            if overwrite:
                contents['profiles'][user_dict['user']] = user_dict['password']
            else:
                return {'code': 403, 'message': 'Overwrite flag needs to be set', 'success': False}

        # 4. Write the file back saving the changes
        chk = self.yaml.write_application_configuration(application, contents)
        if chk:
            return {'code': 200, 'message': 'Existing password value has been updated', 'success': True}
