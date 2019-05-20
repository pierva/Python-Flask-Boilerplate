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


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="admin@carnival.com",
        username="Test_AdminUser",
        password="Admin1234",
        admin=True,
        first_login=False)
    )
    db.session.commit()


@manager.command
def create_user():
    """Creates a non admin user."""
    db.session.add(User(
        email="nonadmin@carnival.com",
        username="Test_NonAdminUser",
        password="Nonadmin1234",
        admin=False)
    )
    db.session.commit()


@manager.command
def delete_test_users():
    """Delete the Admin and NonAdmin users."""
    try:
        stmt = User.__table__.delete().where(User.username.contains('Test_'))
        db.session.execute(stmt)
        db.session.commit()
        print('Deleted test users')
    except Exception as e:
        print(e)
        print('Unable to delete users')


@manager.command
def reset_user_password(email):
    try:
        user = User.query.filter_by(email=email.lower().strip()).one()
        if user:
            user.password = flask_bcrypt.generate_password_hash('Temp1234')\
                .decode('utf-8')
            user.first_login = True
            db.session.add(user)
            db.session.commit()
            print('temporary password for {} is "Temp1234"'.format(user.email))
    except Exception as e:
        print(e)
        print('Unable to reset password for {}'.format(email))


if __name__ == '__main__':
    manager.run()
