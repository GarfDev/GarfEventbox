from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user

root_blueprint = Blueprint('root', __name__
                           , template_folder="../../templates")


@root_blueprint.route('/', methods=["GET"])
def home():
    return render_template("/root/index.html")


@root_blueprint.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("/")
        return render_template("/root/login.html")
    if request.method == "POST":
        pass


@root_blueprint.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("/")
        return render_template("/root/register.html")
    if request.method == "POST":
        pass


@root_blueprint.route('/forgot', methods=["GET", "POST"])
def forgot():
    if request.method == "GET":
        return render_template("/root/forgot.html")
    if request.method == "POST":
        pass


@root_blueprint.route('/verify/<string:TOKEN>', methods=["GET", "POST"])
def verify(TOKEN):
    if request.method == "GET":
        return render_template("/root/verify.html")
    if request.method == "POST":
        pass
