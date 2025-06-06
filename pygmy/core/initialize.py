import sys
import os

from pygmy.config import config
from pygmy.database.factory import DatabaseFactory

_CONFIG_ENV_VAR = 'PYGMY_CONFIG_FILE'
_CFG_PATHS = ['pygmy/config/pygmy.cfg', 'pygmy.cfg',
              '$HOME/.pygmy.cfg', '/etc/pygmy.cfg'
              'tests/pygmy_test.cfg', 'pygmy/config/pygmy_test.cfg']


def load_config_path(config_path=None):
    if config_path and os.path.exists(config_path):
        os.environ[_CONFIG_ENV_VAR] = config_path
        return
    for cfg_path in _CFG_PATHS:
        if os.path.exists(cfg_path):
            os.environ[_CONFIG_ENV_VAR] = cfg_path
            break


def initialize_config(config_path=None):
    os.environ['TZ'] = 'UTC'
    if config_path and os.path.exists(config_path):
        os.environ[_CONFIG_ENV_VAR] = config_path
    else:
        load_config_path(config_path)
    # If config not found, exit the program. Else call config initialize.
    if os.environ.get(_CONFIG_ENV_VAR) is None:
        print('\nNo _CONFIG_ENV_VAR variable set. Exiting...')
        sys.exit(1)
    config.initialize()


def initialize_db():
    database = DatabaseFactory()
    config.db = database.create()


def initialize(config_path=None):
    initialize_config(config_path)
    initialize_db()


def initialize_test(config_path=None, db_url=None):
    """For handeling initialization while running tests"""
    initialize_config(config_path)
    # Handle sqlite file path
    if config.database['engine'] == 'sqlite3':
        config.database['url'] = db_url
    initialize_db()
