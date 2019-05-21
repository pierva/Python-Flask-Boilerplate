# application/main/views.py

from flask import render_template, Blueprint, flash

from application import app, db
from application.models import User

from sqlalchemy import exc
from sqlalchemy.sql import text

# Configuration
main_blueprint = Blueprint('main', __name__,)


# routes
@main_blueprint.route('/')
@main_blueprint.route('/index')
def showHome():
    return render_template('main/home.html')
