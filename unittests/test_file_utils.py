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
        configs = self.yaml_util.get_default_app_config()

        # 2. Confirm not empty
        self.assertIsNotNone(configs)
