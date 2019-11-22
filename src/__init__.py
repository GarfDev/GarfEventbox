# IMPORT_LIBRARYS
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, UserMixin, login_user, logout_user
import time, os
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from dotenv import load_dotenv

# DEFAULT_ENVIROMENT_SETUP

load_dotenv()
app = Flask(__name__, static_folder='../static')
app.config.from_object("config.Config")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
moment = Moment(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# FLASK-LOGIN FUNCTION
from src.models import *


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect('/login')


# ROUTING_FUNCTIONS

from src.components.root import root_blueprint
app.register_blueprint(root_blueprint, url_prefix="/")