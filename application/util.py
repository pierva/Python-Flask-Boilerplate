# application/util.py

from flask_testing import TestCase

from application import app, db
from application.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('application.config.TestingConfig')
        return app

    @classmethod
    def setUpClass(self):
        db.create_all()
        user = User(
            email="test@domain.com",
            password="just_a_test_user",
            admin=False
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()
