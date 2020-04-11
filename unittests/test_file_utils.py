""" Unit tests for file utils """
from unittest import TestCase
from utils import file_utils


class TestFileUtils(TestCase):

    def setUp(self):
        """ Set up class variables """
        self.yaml_util = file_utils.YAML()

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