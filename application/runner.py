""" Primary router for the application
This will handle the majority of the functions for the application
- Authenticate user
- Get Credential
- Get Configuration
- Authenticate Credential?
"""
from flask import Flask
from utils.file_utils import get_default_app_config
from definitions import get_current_env

# Constants
CONF = get_default_app_config()
ENV = get_current_env()

# Flask Setup
app = Flask(__name__)
app.secret_key = CONF['configs']['env'][ENV]['configman_key']


# Test Endpoint
@app.route('/test')
def testing_route():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)
