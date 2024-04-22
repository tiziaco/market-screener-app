import os
import json

# Set the project base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Load API keys from JSON file
with open(f'{basedir}/../keys.json', 'r') as keys_file:
	keys_data = json.load(keys_file)

ENVIRONMENT = "dev" #Supported environments: 'dev', 'test', 'backtest', 'live'


class Config:
	"""
	iTrader general configuration variables.
	"""
	TIMEZONE = 'Europe/Paris'
	SECRET_KEYS = keys_data.get('SECRET_KEYS', {})

	LOGGING_FORMAT = str('%(levelname)s | %(message)s') # %(asctime)s 
	PRINT_LOG = bool(True)
	SAVE_LOG = bool(False)

	SUPPORTED_CURRENCIES = {'USDT', 'BUSD'}
	SUPPORTED_EXCHANGES = {'BINANCE', 'KUCOIN'}

class DevelopmentConfig(Config):
	PRICE_DB_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/trading_system_prices'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_test.db')
	DEBUG = bool(True)
	TESTING = bool(False)
	SQLALCHEMY_TRACK_MODIFICATIONS = bool(False)


class TestingConfig(Config):
	PRICE_DB_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/trading_system_prices'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_test.db')
	DEBUG = bool(False)
	TESTING = bool(True)
	PRESERVE_CONTEXT_ON_EXCEPTION = bool(False)
	SQLALCHEMY_TRACK_MODIFICATIONS = bool(False)

class LiveConfig(Config):
	DEBUG = bool(False)
	DATA_DB_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/trading_system_prices'
	SYSTEM_DB_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/.......'
	DEBUG = bool(False)
	TESTING = bool(False)
	PRESERVE_CONTEXT_ON_EXCEPTION = bool(True)
	SQLALCHEMY_TRACK_MODIFICATIONS = bool(True)


def set_config(env) -> Config:
    """
    Sets the configuration based on the environment.

    Parameters
    ----------
    env : `str`
		Environment identifier ('dev', 'test', 'backtest', 'live').

    Returns
    ----------
	Config : `Config`
		Configuration object corresponding to the specified environment.

    Raises
    ----------
        ValueError : If the specified environment is not recognized.
    """
    configs = {
        'dev': DevelopmentConfig,
        'test': TestingConfig,
        'live': LiveConfig
    }
    config = configs.get(env)
    if config is None:
        raise ValueError(f"Unknown environment: {env}. Supported environments are: 'dev', 'test', 'backtest', 'live'.")
    return config
