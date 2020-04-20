""" Primary router for the application
This will handle the majority of the functions for the application
- Authenticate user
- Get Credential
- Get Configuration
- Authenticate Credential?
"""
from definitions import get_current_env
from utils.file_utils import get_default_app_config
from utils.logger import logger

from flask import Flask, request, abort, jsonify

from application.func.cred_manager.credential import ApplicationCredentials
from application.func.cred_manager.flask_handlers import AuthToken

# Constants
CONF = get_default_app_config()
ENV = get_current_env()
EXP_TIME = 600  # 10 Minutes per Token

# Flask Setup
app = Flask(__name__)
app.secret_key = CONF['configs']['env'][ENV]['configman_key']

# Import Shortcuts
app_creds = ApplicationCredentials()
auth_token = AuthToken(app, EXP_TIME)


# Response Handlers
def success(endpoint, resp_dict):
    """ Success message handling with additional logging
    :return: Success response
    """
    logger.info('Endpoint: %s | HTTP Status: %s' % (endpoint, str(resp_dict['code'])))
    payload = {
        'response': resp_dict['message']
    }
    return handle_response(payload, resp_dict['code'])


def err(resp_dict):
    """ Error message handling with additional logging
    :return: Error response
    """
    logger.error('API related error being sent to client')
    logger.error('HTTP Status: %s' % str(resp_dict['code']))
    logger.error('Message Returned: %s' % resp_dict['message'])
    payload = {
        'error': {
            'code': resp_dict['code'],
            'message': resp_dict['message']
        }
    }
    return handle_response(payload, resp_dict['code'])


def warn(warning_type, resp_dict):
    """ Warning message handling with additional logging
    :return: Warning response
    """
    logger.error('HTTP Status: %s' % str(resp_dict['code']))
    logger.error('Message Returned: %s' % resp_dict['message'])
    payload = {
        warning_type: {
            'code': resp_dict['code'],
            'message': resp_dict['message']
        }
    }
    return handle_response(payload, resp_dict['code'])


def handle_response(payload, code):
    """ Generate and return appropriate response
    :param payload:
    :param code: HTTPStatusCode
    :return: Fully formatted response
    """
    response = jsonify(payload)
    response.status_code = code
    return response


# Test Endpoint
@app.route('/test')
def testing_route():
    return 'Hello'


@app.route('/auth/token/generate', methods=['POST'])
def get_auth_token():
    # Validate payload
    if not (request.json or 'user' in request.json or 'password' in request.json or 'app' in request.json):
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(request.json))
        abort(400)

    # Validate credentials
    user_dict = {
        'user': request.json['user'],
        'password': request.json['password']
    }
    response = app_creds.validate_application_credentials(request.json['app'], user_dict)
    status_code = response['code']

    # Generate Token
    if response['success']:
        logger.info('User %s authenticated, generating token' % request.json['user'])
        token = auth_token.generate_auth_token(request.json['user'])
        response = {
            'code': status_code,
            'success': True,
            'message': {
                'token': token.decode('ascii')
            }
        }
        return success('/auth/token/generate', response)
    else:
        logger.warning('User %s not authenticated, reporting error...' % request.json['user'])
        return warn('authGen', response)


@app.route('/auth/token/validate', methods=['POST'])
def verify_token():
    # Validate payload
    if not (request.json or 'user' in request.json or 'token' in request.json):
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(request.json))
        abort(400)
    response = auth_token.validate_auth_token(request.json['token'], request.json['user'])
    if response['exception']:
        return warn('authVal', response)
    else:
        return success('/auth/token/validate', response)


if __name__ == '__main__':
    app.run(debug=True)
