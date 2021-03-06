""" Unit tests for file utils """
from unittest import TestCase
from utils import file_utils


class TestFileUtils(TestCase):

    def setUp(self):
        """ Set up class variables """
        self.yaml_util = file_utils.YAML()
        self.env = self.yaml_util.env
        self.sys_conf = self.yaml_util.sys_conf

    def test_get_default_app_config(self):
        """ Test to get the default application configuration
        1. Get default config
        2. Confirm not empty
        """
        # 1. Get default config
        configs = file_utils.get_default_app_config()

        # 2. Confirm not empty
        self.assertIsNotNone(configs)

    def test_get_app_configs(self):
        """ Test to get application configs
        1. Get the config file
        2. Confirm the expected length
        3. Confirm the content
        """
        # 1. Get the config file
        configs = self.yaml_util.get_application_configurations('test')

        # 2. Confirm the expected length
        self.assertEqual(3, len(configs))

        # 3. Confirm the content
        self.assertEqual(configs['Item3'], 'final thing')
        print(configs)

    def test_write_yaml(self):
        """ Test to write a simple file
        1. Set up the test variables
        2. Write the file
        3. Read the file
        4. Confirm the contents
        """
        # 1. Set up the test variables
        content = {
            'Item1': 'this is one thing',
            'Item2': {
                'ItemA': 765,
                'ItemB': 99
            },
            'Item3': 'final thing'
        }
        file_location = self.sys_conf['configs']['env'][self.env]['app_config_url'] + '/test.yaml'

        # 2. Write the file
        chk = file_utils.write_yaml(file_location, content)
        self.assertTrue(chk)

        # 3. Read the file
        configs = self.yaml_util.get_application_configurations('test')

        # 4. Confirm the contents
        self.assertEqual(content, configs)

    def test_write_test_app_config(self):
        """ Test to write the test application configuration to file
        1. Set up test variables
        2. Write the file
        3. Read the file confirm written as expected
        """
        # 1. Set up test variables
        content = {
            'Item1': 'this is one thing',
            'Item2': {
                'ItemA': 765,
                'ItemB': 99
            },
            'Item3': 'final thing'
        }

        # 2. Write the file
        self.assertTrue(self.yaml_util.write_application_configuration('test', content))

        # 3. Read the file confirm written as expected
        document = self.yaml_util.get_application_configurations('test')
        self.assertEqual(content, document)

    def test_check_file_existence(self):
        """ Test to validate a file can be found appropriately
        1. Set up test variables
        2. Check file existence
        3. Validate the appropriate response
        """
        # 1. Set up test variables
        file_location = self.sys_conf['configs']['env'][self.env]['app_config_url'] + '/test.yaml'

        # 2. Check file existence
        response = file_utils.file_check(file_location)

        # 3. Validate the appropriate response
        self.assertTrue(response)

    def test_check_if_app_conf_exists(self):
        """ Test to validate an app config exits
        1. Set up test variables
        2. Check if app config exists
        3. Validate the appropriate response
        4. Check if app config exists for one that doesn't
        5. Validate the appropriate response
        """
        # 1. Set up test variables
        good_app = 'test'
        bad_app = 'batman'

        # 2. Check if app config exists
        response = self.yaml_util.check_for_application_file(good_app)

        # 3. Validate the appropriate response
        self.assertTrue(response)

        # 4. Check if app config exists for one that doesn't
        response = self.yaml_util.check_for_application_file(bad_app)

        # 5. Validate the appropriate response
        self.assertFalse(response)
