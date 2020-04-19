""" Unit tests for cred manager """
from unittest import TestCase
from application.func.cred_manager.credential_manager import ApplicationCredentials
from utils import file_utils
from random import randint


class TestCredManager(TestCase):

    def setUp(self):
        """ Set up class variables """
        self.app_creds = ApplicationCredentials()

    def test_create_and_validate_new_application_credentials(self):
        """ Test to generate application credentials for a test app
        1. Set up test variables
        2. Generate the credentials
        3. Validate response
        4. Raw read the file
        5. Validate the password is encrypted
        6. Run the validate application credentials
        7. Validate response
        """
        # 1. Set up test variables
        application = 'test_app' + str(randint(0, 99))
        user_dict = {
            'user': 'test_user',
            'password': 'test_pass'
        }

        # 2. Generate the credentials
        response = self.app_creds.create_update_application_credentials(application, user_dict)

        # 3. Validate response
        self.assertEqual(response['code'], 201)
        self.assertTrue(response['success'])

        # 4. Raw read the file
        file = file_utils.read_yaml('/usr/local/beringersolutions/app_configs/LOCAL/{application}.yaml'.format(
            application=application))

        # 5. Validate the password is encrypted
        self.assertNotEqual(user_dict['password'], file['profiles'][user_dict['user']]['password'])
        self.assertEqual(user_dict['user'], file['profiles'][user_dict['user']]['user'])

        # 6. Run the validate application credentials
        response = self.app_creds.validate_application_credentials(application, user_dict)

        # 7. Validate response
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

    def test_create_and_validate_new_application_credentials_for_new_app(self):
        """ Test to generate applications
        1. Set up test variables
        2. Generate the credentials
        3. Validate the response
        4. Run validate application credentials
        5. Validate the response
        6. Update the password without the overwrite flag
        7. Validate the response
        8. Update the password with the overwrite flag
        9. Validate the response
        10. Run validate application credentials
        11. Validate the response
        """
        # 1. Set up test variables
        application = 'test_app' + str(randint(0, 99))
        user_dict = {
            'user': 'test_user',
            'password': 'test_pass'
        }
        new_password = 'test_pass_new'

        # 2. Generate the credentials
        response = self.app_creds.create_update_application_credentials(application, user_dict)

        # 3. Validate the response
        self.assertEqual(response['code'], 201)
        self.assertTrue(response['success'])

        # 4. Run validate application credentials
        response = self.app_creds.validate_application_credentials(application, user_dict)

        # 5. Validate the response
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

        # 6. Update the password without the overwrite flag
        user_dict['password'] = new_password
        response = self.app_creds.create_update_application_credentials(application, user_dict)

        # 7. Validate the response
        self.assertEqual(response['code'], 403)
        self.assertFalse(response['success'])

        # 8. Update the password with the overwrite flag
        response = self.app_creds.create_update_application_credentials(application, user_dict, True)

        # 9. Validate the response
        self.assertEqual(response['code'], 200)
        self.assertTrue(response['success'])

        # 10. Run validate application credentials
        response = self.app_creds.validate_application_credentials(application, user_dict)

        # 11. Validate the response
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

    def test_creation_for_existing_app(self):
        """ Test to validate the flow of an existing app getting a new credential or updating a credential
        1. Set up test variables
        2. Generate the new test application
        3. Validate credentials accurate
        4. Update credentials for same user
        5. Validate credentials accurate
        6. Add new credential to existing file
        7. Validate credentials accurate
        8. Update new credential
        9. Validate credentials accurate
        """
        # 1. Set up test variables
        application = 'test_app' + str(randint(0, 99))
        user_dict = {
            'user': 'test_user',
            'password': 'test_pass'
        }
        second_user_dict = {
            'user': 'test_user_second',
            'password': 'test_pass_different'
        }
        new_password = 'test_pass_new'

        # 2. Generate the new test application
        response = self.app_creds.create_update_application_credentials(application, user_dict)
        self.assertEqual(response['code'], 201)
        self.assertTrue(response['success'])

        # 3. Validate credentials accurate
        response = self.app_creds.validate_application_credentials(application, user_dict)
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

        # 4. Update credentials for same user
        user_dict['password'] = new_password
        response = self.app_creds.create_update_application_credentials(application, user_dict, overwrite=True)
        self.assertEqual(response['code'], 200)
        self.assertTrue(response['success'])

        # 5. Validate credentials accurate
        response = self.app_creds.validate_application_credentials(application, user_dict)
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

        # 6. Add new credential to existing file
        response = self.app_creds.create_update_application_credentials(application, second_user_dict)
        self.assertEqual(response['code'], 200)
        self.assertTrue(response['success'])

        # 7. Validate credentials accurate
        response = self.app_creds.validate_application_credentials(application, second_user_dict)
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

        # 8. Update new credential
        second_user_dict['password'] = new_password
        response = self.app_creds.create_update_application_credentials(application, second_user_dict, overwrite=True)
        self.assertEqual(response['code'], 200)
        self.assertTrue(response['success'])

        # 9. Validate credentials accurate
        response = self.app_creds.validate_application_credentials(application, second_user_dict)
        self.assertEqual(response['code'], 202)
        self.assertTrue(response['success'])

    def test_error_scenarios(self):
        """ Test to validate the various error scenarios and the responses
        1. Set up test variables
        2. Application config not found
        3. User not found
        4. User password invalid
        """
        # 1. Set up test variables
        application = 'test_app' + str(randint(0, 99))
        user_dict = {
            'user': 'test_user',
            'password': 'test_pass'
        }
        bad_user_dict = {
            'user': 'test_user_bad',
            'password': 'test_pass'
        }
        invalid_password = 'invalid'

        # 2. Application config not found
        response = self.app_creds.validate_application_credentials('batman', user_dict)
        self.assertFalse(response['success'])
        self.assertEqual(response['code'], 404)

        # 3. User not found
        response = self.app_creds.create_update_application_credentials(application, user_dict)
        self.assertEqual(response['code'], 201)
        self.assertTrue(response['success'])
        response = self.app_creds.validate_application_credentials(application, bad_user_dict)
        self.assertEqual(response['code'], 404)
        self.assertFalse(response['success'])

        # 4. User password invalid
        user_dict['password'] = invalid_password
        response = self.app_creds.validate_application_credentials(application, user_dict)
        self.assertEqual(response['code'], 401)
        self.assertFalse(response['success'])
