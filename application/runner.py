""" Primary router for the application
This will handle the majority of the functions for the application
- Authenticate user
- Get Credential
- Get Configuration
- Authenticate Credential?
"""
import json
from definitions import get_current_env
from utils.file_utils import get_default_app_config
from utils.logger import logger

from flask import Flask, request, abort, jsonify

from application.func.cred_manager.credential import ApplicationCredentials
from application.func.cred_manager.configs import ApplicationConfigs
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
app_confs = ApplicationConfigs()
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


# Tools
def handle_auth_in_req(token, user):
    """ Validates the request header proper formatting """
    response = auth_token.validate_auth_token(token, user)
    if response['exception']:
        return warn('authVal', response)
    else:
        return response


# Test Endpoint
@app.route('/test')
def testing_route():
    return 'Hello'


############################
# AUTHENTICATION ENDPOINTS #
############################
@app.route('/auth/token/generate', methods=['POST'])
def get_auth_token():
    # Validate payload
    if not (request.json or 'user' in request.json or 'password' in request.json or 'app' in request.json):
        content = json.loads(request.json)
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(content))
        abort(400)

    # Validate credentials
    content = request.json
    user_dict = {
        'user': content['user'],
        'password': content['password']
    }
    response = app_creds.validate_application_credentials(content['app'], user_dict)
    status_code = response['code']

    # Generate Token
    if response['success']:
        logger.info('User %s authenticated, generating token' % content['user'])
        token = auth_token.generate_auth_token(content['user'])
        response = {
            'code': status_code,
            'success': True,
            'message': {
                'token': token.decode('ascii')
            }
        }
        return success('/auth/token/generate', response)
    else:
        logger.warning('User %s not authenticated, reporting error...' % content['user'])
        return warn('authGen', response)


@app.route('/auth/token/validate', methods=['POST'])
def verify_token():
    # Validate payload
    if not (request.json or 'user' in request.json or 'token' in request.json):
        content = json.loads(request.json)
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(content))
        abort(400)
    content = json.loads(request.json)
    response = auth_token.validate_auth_token(content['token'], content['user'])
    if response['exception']:
        return warn('authVal', response)
    else:
        return success('/auth/token/validate', response)


###########################
# CONFIGURATION ENDPOINTS #
###########################
@app.route('/app/configs', methods=['POST'])
def handle_app_configs():
    # Get headers
    if not (request.json or 'Authorization' in request.headers or 'user' in request.headers):
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(request.json))
        abort(400)
    response = handle_auth_in_req(request.headers['Authorization'], request.headers['User'])
    if type(response) != dict:
        return response
    if not ('app' in request.json or 'configType' in request.json):
        logger.debug('Something is missing from your payload.  Double check everything is there')
        logger.debug(str(request.json))
        abort(400)
    else:
        content = json.loads(request.json)
        response = app_confs.read_application_configs(content['app'], content['configType'],
                                                      response['message']['user'])
        if response['success']:
            return success('/app/configs', response)
        else:
            return err(response)
    return


# Runner
if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0')  # For production deploy
    app.run(debug=True)                     # For local testing
