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
        3. Confirm the file length
        4. Read the file
        5. Confirm the contents
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
        document = file_utils.write_yaml(file_location, content)

        # 4. Read the file
        configs = self.yaml_util.get_application_configurations('test')

        # 5. Confirm the contents
        self.assertEqual(content, configs)
