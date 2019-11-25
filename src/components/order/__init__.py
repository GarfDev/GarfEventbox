from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from src.models import *
from src import db, mailjet, app, encoder
import time, re
from itsdangerous import SignatureExpired

order_blueprint = Blueprint('order', __name__
                           , template_folder="../../templates")
