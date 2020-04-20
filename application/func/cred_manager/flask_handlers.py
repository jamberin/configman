""" Handlers for Flask Application
- CredResp: Handles the API responses
- AuthToken: Handles all token related activities
"""
from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class AuthToken(object):
    """ Handler for token authentication """

    def __init__(self, application, exp_time=600):
        """ Initialize Class Variables """
        self.app = application
        self.expiration = exp_time

    def generate_auth_token(self, username):
        """ Generates a valid authentication token for the application
        :param username: Hashed password for the given user to generate the token against
        :return: Proper token for usage
        """
        serial = Serializer(self.app.secret_key)
        exp_epoch = datetime.timestamp(datetime.now() + timedelta(seconds=self.expiration))
        response = {
            'user': username,
            'exp_time': str(exp_epoch)
        }
        return serial.dumps(response)

    def validate_auth_token(self, token, username):
        """ Validates the token for the given username
        :param token:
        :param username:
        :return: Boolean flag for success
        """
        response = {
            'code': None,
            'message': None,
            'success': None
        }
        serial = Serializer(self.app.secret_key)
        try:
            token = serial.loads(token)
        except SignatureExpired:
            response['code'] = 401
            response['message'] = 'Unauthorized: Expired Token'
            response['success'] = False
            response['exception'] = 'SignatureExpired'
            return response
        except BadSignature:
            response['code'] = 401
            response['message'] = 'Unauthorized: Token not recognized'
            response['success'] = False
            response['exception'] = 'BadSignature'
            return response
        if token['user'] == username:
            if float(token['exp_time']) > datetime.timestamp(datetime.now()):
                response['code'] = 200
                response['message'] = {
                    'user': username,
                    'timestamp': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                }
                response['success'] = True
                response['exception'] = None
            else:
                response['code'] = 401
                response['message'] = 'Unauthorized: Expired Token'
                response['success'] = False
                response['exception'] = 'SignatureExpired'
            return response
        else:
            response['code'] = 403
            response['message'] = 'Forbidden: Token not for user'
            response['success'] = True
            response['exception'] = 'Forbidden'
            return response
