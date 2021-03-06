import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_LOG_FILENAME = os.path.join(rootdir, 'log/error.log')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/databaseName'
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
        'test.sqlite')


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:user@localhost/database'
    DEBUG_TB_ENABLED = False

    # production config takes precedence over env variables
    # production config file at ./application/instance/production.cfg
    config_path = os.path.join(basedir, 'instance', 'production.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.readfp(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECURITY_PASSWORD_SALT')
        SQLALCHEMY_DATABASE_URI = config.get('keys', 'SQLALCHEMY_DATABASE_URI')
