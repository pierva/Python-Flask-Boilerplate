# manage.py

import os
import unittest
import datetime
import logging

from logging.handlers import RotatingFileHandler
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from application import app, db, flask_bcrypt
from application.models import User

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s: %(levelname)s: %(message)s",
                    filename=app.config['ERROR_LOG_FILENAME'])

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()
