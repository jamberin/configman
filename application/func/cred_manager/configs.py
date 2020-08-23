""" Handles reading and writing configurations to the application file
- Reading configurations from the file
    - Can only read from a file where the user is present
- Writing configurations to the file
    - Overwrite flag option to overwrite existing content
"""
from utils.file_utils import YAML
from utils.logger import logger


class ApplicationConfigs(object):
    """ Generate the configurations for an application """

    def __init__(self):
        """ Initialize class variables """
        self.yaml = YAML()

    """ METHOD DEPRECATED DUE TO DEFECT WITHIN METHOD, APPLICATION CONFIGS ARE BEING SET MANUALLY NOW """
    # def create_update_application_configuration(self, application, user, config_type, config_dict, overwrite=False):
    #     """ Generate configuration for an application
    #     1. Get the application file (if no file, return error)
    #     2. Validate the user is in the file
    #     3. Check if record currently exists in file
    #         a. If record exists, check for overwrite flag
    #     4. Write the file back saving the changes
    #     :param application: The application that the configuration is being written
    #     :param user: User who is making the request
    #     :param config_type:
    #     :param config_dict: Dictionary of the configurations to be written (key in dict will be key in file)
    #     :param overwrite: Overwrite the existing credential
    #     :return: If overwrite condition, return overwrite validation, else add the credential
    #     """
    #     # 1. Get the application file (if no file, return error)
    #     if self.yaml.check_for_application_file(application):
    #         contents = self.yaml.get_application_configurations(application)
    #         logger.info('Application contents being loaded: %s' % application)
    #     else:
    #         return {'code': 404, 'message': 'No file for application', 'success': False}
    #
    #     # 2. Validate the user is in the file
    #     if 'profiles' in contents:
    #         if user in contents['profiles']:
    #             logger.info('User profile found in application configs: %s' % user)
    #         else:
    #             return {'code': 404, 'message': 'User not found in file', 'success': False}
    #     else:
    #         return {'code': 404, 'message': 'No profiles in file', 'success': False}
    #
    #     # 3. Check if record currently exists in file
    #     valid_types = {'dirs', 'vars'}
    #     if config_type not in valid_types:
    #         logger.error('Not a valid config type: %s' % config_type)
    #         return {'code': 403, 'message': 'Not a valid config type', 'success': False}
    #     if 'configs' in contents:
    #         if contents['configs'][config_type]:
    #             contents_keys = contents['configs'][config_type].keys()
    #             dict_keys = config_dict.keys()
    #             for key in dict_keys:
    #                 if key in contents_keys and overwrite:
    #                     logger.info('Overwriting existing configuration: %s' % key)
    #                     contents['configs'][config_type][key] = config_dict[key]
    #                 elif key in contents_keys and overwrite is False:
    #                     return {'code': 403, 'message': 'Overwrite flag needs to be set', 'success': False}
    #                 else:
    #                     logger.info('New config written to file: %s' % key)
    #                     contents['configs'][config_type][key] = config_dict[key]
    #         else:
    #             contents['configs'] = {config_type: config_dict}
    #     else:
    #         contents['configs'] = {config_type: config_dict}
    #
    #     # 4. Write the file back saving the changes
    #     chk = self.yaml.write_application_configuration(application, contents)
    #     if chk:
    #         logger.info('Configuration written')
    #         return {'code': 200, 'message': 'Existing file has been updated', 'success': True}
    #     else:
    #         logger.error('Error writing application configuration')
    #         return {'code': 500, 'message': 'Error writing to file', 'success': True}

    def read_application_configs(self, application, config_type, user):
        """ Read application configurations
        1. Get the application file (if no file, return error)
        2. Validate the user is in the file
        3. Check the config type exists
        4. Return the configuration
        :param application: Application to be read
        :param config_type: Configuration type to be returned
        :param user: User making the request
        :return:
        """
        # 1. Get the application file (if no file, return error)
        if self.yaml.check_for_application_file(application):
            contents = self.yaml.get_application_configurations(application)
            logger.info('Application contents being loaded: %s' % application)
        else:
            return {'code': 404, 'message': 'No file for application', 'success': False}

        # 2. Validate the user is in the file
        if 'profiles' in contents:
            if user in contents['profiles']:
                logger.info('User profile found in application configs: %s' % user)
            else:
                return {'code': 404, 'message': 'User not found in file', 'success': False}
        else:
            return {'code': 404, 'message': 'No profiles in file', 'success': False}

        # 3. Check the config type exists
        if 'configs' in contents:
            if config_type in contents['configs']:
                response = contents['configs'][config_type]
            else:
                return {'code': 404, 'message': 'Config type not found', 'success': False}
        else:
            return {'code': 404, 'message': 'Configs not found', 'success': False}

        # 4. Return the configuration
        return {'code': 200, 'message': response, 'success': True}
