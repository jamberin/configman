""" Handling the credentials for system requirements
- Create the credentials
    - Encrypt password (encryption key should be configurable value)
- Validate the successful creation of the record
    - After creation, select the successful record
- Get the credentials for a given user
    - Validate password is correct
"""


class GenerateCredentials(object):
    """ Generate the credentials for a user """
