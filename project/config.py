from boiler.config import default_config as config
import os
"""
Local config
This file configures installation of this specific environment.
It extends global application config and should not be committed to repository
"""


class DefaultConfig(config.DefaultConfig):
    """ Local development config """

    # set this for offline mode
    SERVER_NAME = None
    SECRET_KEY = '282d2acc-1f96-11e8-ab74-406c8f413974'

    ASSETS_VERSION = 1
    ASSETS_PATH = '/'
    FLASK_STATIC_PATH = os.path.realpath(os.getcwd() + '/web')

    # users
    USER_JWT_SECRET = '28312d28-1f96-11e8-810c-406c8f413974'


class DevConfig(DefaultConfig, config.DevConfig):
    """ Local development config """
    pass


class TestingConfig(DefaultConfig, config.TestingConfig):
    """ Local testing config """
    pass






