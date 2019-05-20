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


def days_until_today(value, format = 'days'):
    """ Return the difference between now and the passed date.
        Value must be a datetime object.
    """
    now = datetime.datetime.now()
    try:
        start = datetime.datetime(value.year, value.month, value.day)
        if format == 'days':
            diff = abs(start - now).days
        elif format == 'hours':
            diff = abs(start - now).hours
    except Exception as e:
        app.logger.error(e)
        return 'n/a'
    return diff

def format_iso_date(isodate):
    """Formats a iso date and returns a formatted date as
       'Sun Apr 07, 2019 @ 18:20'. In case of errros it returns 'N/A'"""
    try:
        dateobj = datetime.datetime.strptime(isodate, '%Y-%m-%dT%H:%M:%S.%f')
        return dateobj.strftime('%a %b %d, %Y @ %H:%M')
    except Exception as e:
        app.logger.error('Error trying formatting the isodate. {} - {}'\
                         .format(isodate, e))
        return 'N/A'

def round_to_two_decimals(value):
    """It takes a float and returns a 2 decimal places string"""
    try:
        return "{0:.2f}".format(value)
    except Exception as e:
        return '--'

app.jinja_env.filters['days_until_today'] = days_until_today
app.jinja_env.filters['format_iso_date'] = format_iso_date
app.jinja_env.filters['round_to_two_decimals'] = round_to_two_decimals


@app.context_processor
def date_diff():
    def _date_diff(start, end=datetime.datetime.now().strftime("%m/%d/%Y"),
                   format='days'):
        """ Return the difference between two dates. Default output is in
            days. Start and end date are date strings (mm/dd/yyyy).
            The difference is the absolute value.
            If no end date is provided, the difference will be between now
            and start date.
        """
        try:
            s_m, s_d, s_y = start.split('/')
            e_m, e_d, e_y = end.split('/')
            start = datetime.datetime(int(s_y), int(s_m), int(s_d))
            end = datetime.datetime(int(e_y), int(e_m), int(e_d))
            if format == 'days':
                diff = abs(end - start).days
            elif format == 'hours':
                diff = abs(end - start).hours
        except Exception as e:
            app.logger.error(e)
            return 'n/a'
        return diff
    return dict(date_diff=_date_diff)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter(User.id == int(user_id)).first()
    except exc.SQLAlchemyError as e:
        return None


# error handlers setup (use with abort(errCode))
@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
