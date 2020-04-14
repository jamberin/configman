""" Utilities for Encryption Services
- Using bcrypt for handling credential encryption and decryption
"""

import bcrypt


def generate_pass_hash(value):
    """ Create password hash for the given value
    :param value: String of the value to be encrypted
    :return: Hash value of string
    """
    value = value.encode('UTF-8')
    salt = bcrypt.gensalt()
    hash_val = bcrypt.hashpw(value, salt)
    return hash_val


def validate_pass_hash(value, hash_val):
    """ Validate the value given matches the hashed value
    :param value:
    :param hash_val:
    :return:
    """
    return bcrypt.checkpw(value, hash_val)


def generate_user_dict_for_app_config(user, password):
    """ Generate a dictionary that can be used to update or create a new user profile
    :param user: Username to be included in the application configuration
    :param password: Password to be encrypted
    :return: User profile dictionary
    """
    pass_hash = generate_pass_hash(value=password)
    user_dictionary = {
        'user': user,
        'password': pass_hash
    }
    return user_dictionary

