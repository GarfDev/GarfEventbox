from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from src.models import *
from src import db

root_blueprint = Blueprint('root', __name__
                           , template_folder="../../templates")


@root_blueprint.route('/', methods=["POST", "GET"])
def home():
    return render_template("/root/index.html")