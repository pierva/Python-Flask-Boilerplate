import os
import datetime
from flask import (Flask, render_template, abort)

from flask_login import LoginManager

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# For production
# app.config.from_object("application.config.ProductionConfig")

db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# routes setup
from application.main.views import main_blueprint


app.register_blueprint(main_blueprint)

from application.models import User


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter(User.id == int(user_id)).first()
    except exc.SQLAlchemyError as e:
        return None
