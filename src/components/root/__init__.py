from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from src.models import Users, Events, Order_History
from src import db, mailjet, app, encoder
import time, re
from itsdangerous import SignatureExpired

root_blueprint = Blueprint('root', __name__
                           , template_folder="../../templates")


@root_blueprint.route('/', methods=["GET"])
def home():
    events = Events.query.all()
    return render_template("/root/index.html", events=events, time=time)


@root_blueprint.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("/")
        return render_template("/root/login.html")
    if request.method == "POST":
        try:
            if re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['username']):
                user = Users.query.filter_by(email=request.form['username']).first()
            else:
                user = Users.query.filter_by(username=request.form['username']).first()
            if not user:
                flash("Your username of password is wrong, please try again!")
                return render_template("root/login.html")
            if not user.email_verified:
                flash("Please verify your acccount before try to loggin")
                return render_template("root/login.html")
            if not user.check_password(request.form['password']):
                flash("Your username of password is wrong, please try again!")
                return render_template("root/login.html")
            if user.check_password(request.form['password']):
                login_user(user)
                flash("Login successful!")
                return redirect("/")
        except Exception as Error:
            print(Error)
            flash("Error while log you in our server, please try again later.")
            return render_template("root/login.html")


@root_blueprint.route('/register', methods=["POST", "GET"])
def register():
    global verify_token
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect("/")
        return render_template("/root/register.html")
    if request.method == "POST":
        try:
            new_user = Users(
                username=request.form['username'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                created_at=int(time.time()),
                updated_at=int(time.time())
            )
            new_user.set_password(request.form['password'])
            db.session.add(new_user)
            print(str(encoder.dumps(new_user.email, salt="email-verify")))
            verify_token = str(encoder.dumps(new_user.email, salt="email-verify"))

            html = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta name="viewport" content="width=device-width, initial-scale=1.0" />
              <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
              <title>Verify your email address</title>
              <style type="text/css" rel="stylesheet" media="all">
                /* Base ------------------------------ */
                *:not(br):not(tr):not(html) {
                  font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
                  -webkit-box-sizing: border-box;
                  box-sizing: border-box;
                }
                body {
                  width: 100% !important;
                  height: 100%;
                  margin: 0;
                  line-height: 1.4;
                  background-color: #F5F7F9;
                  color: #839197;
                  -webkit-text-size-adjust: none;
                }
                a {
                  color: #414EF9;
                }
                /* Layout ------------------------------ */
                .email-wrapper {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  background-color: #F5F7F9;
                }
                .email-content {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                }
                /* Masthead ----------------------- */
                .email-masthead {
                  padding: 25px 0;
                  text-align: center;
                }
                .email-masthead_logo {
                  max-width: 400px;
                  border: 0;
                }
                .email-masthead_name {
                  font-size: 16px;
                  font-weight: bold;
                  color: #839197;
                  text-decoration: none;
                  text-shadow: 0 1px 0 white;
                }
                /* Body ------------------------------ */
                .email-body {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  border-top: 1px solid #E7EAEC;
                  border-bottom: 1px solid #E7EAEC;
                  background-color: #FFFFFF;
                }
                .email-body_inner {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                }
                .email-footer {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                  text-align: center;
                }
                .email-footer p {
                  color: #839197;
                }
                .body-action {
                  width: 100%;
                  margin: 30px auto;
                  padding: 0;
                  text-align: center;
                }
                .body-sub {
                  margin-top: 25px;
                  padding-top: 25px;
                  border-top: 1px solid #E7EAEC;
                }
                .content-cell {
                  padding: 35px;
                }
                .align-right {
                  text-align: right;
                }
                /* Type ------------------------------ */
                h1 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 19px;
                  font-weight: bold;
                  text-align: left;
                }
                h2 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 16px;
                  font-weight: bold;
                  text-align: left;
                }
                h3 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 14px;
                  font-weight: bold;
                  text-align: left;
                }
                p {
                  margin-top: 0;
                  color: #839197;
                  font-size: 16px;
                  line-height: 1.5em;
                  text-align: left;
                }
                p.sub {
                  font-size: 12px;
                }
                p.center {
                  text-align: center;
                }
                /* Buttons ------------------------------ */
                .button {
                  display: inline-block;
                  width: 200px;
                  background-color: #414EF9;
                  border-radius: 3px;
                  color: #ffffff;
                  font-size: 15px;
                  line-height: 45px;
                  text-align: center;
                  text-decoration: none;
                  -webkit-text-size-adjust: none;
                  mso-hide: all;
                }
                .button--green {
                  background-color: #28DB67;
                }
                .button--red {
                  background-color: #FF3665;
                }
                .button--blue {
                  background-color: #414EF9;
                }
                /*Media Queries ------------------------------ */
                @media only screen and (max-width: 600px) {
                  .email-body_inner,
                  .email-footer {
                    width: 100% !important;
                  }
                }
                @media only screen and (max-width: 500px) {
                  .button {
                    width: 100% !important;
                  }
                }
              </style>
            </head>
            <body>
              <table class="email-wrapper" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <table class="email-content" width="100%" cellpadding="0" cellspacing="0">
                      <!-- Logo -->
                      <tr>
                        <td class="email-masthead">
                          <a class="email-masthead_name">Garfield Events Corporations</a>
                        </td>
                      </tr>
                      <!-- Email Body -->
                      <tr>
                        <td class="email-body" width="100%">
                          <table class="email-body_inner" align="center" width="570" cellpadding="0" cellspacing="0">
                            <!-- Body content -->
                            <tr>
                              <td class="content-cell">
                                <h1>Verify your email address</h1>
                                <p>Thanks for signing up for Garfield Events! We're excited to have you as an early user.</p>
                                <!-- Action -->
                                <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0">
                                  <tr>
                                    <td align="center">
                                      <div>
                                        <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://garfticketbox.herokuapp.com/verify/""" + verify_token + """" style="height:45px;v-text-anchor:middle;width:200px;" arcsize="7%" stroke="f" fill="t">
                                        <v:fill type="tile" color="#414EF9" />
                                        <w:anchorlock/>
                                        <center style="color:#ffffff;font-family:sans-serif;font-size:15px;">Verify Email</center>
                                      </v:roundrect><![endif]-->
                                        <a href="https://garfticketbox.herokuapp.com/verify/""" + verify_token + """" style="color:white;" class="button button--blue">Verify Email</a>
                                      </div>
                                    </td>
                                  </tr>
                                </table>
                                <p>Thanks,<br>The Garfield Events Team</p>
                                <!-- Sub copy -->
                                <table class="body-sub">
                                  <tr>
                                    <td>
                                      <p class="sub">If you’re having trouble clicking the button, copy and paste the URL below into your web browser.
                                      </p>
                                      <p class="sub"><a href="https://garfticketbox.herokuapp.com/verify/""" + verify_token + """"</a></p>
                                    </td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <table class="email-footer" align="center" width="570" cellpadding="0" cellspacing="0">
                            <tr>
                              <td class="content-cell">
                                <p class="sub center">
                                  Garfield Events, Inc.
                                  <br>325 9th St, San Francisco, CA 94103
                                </p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </body>
            </html>
            """

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "nguyengiatuan3110@gmail.com",
                            "Name": "Garfield Event"
                        },
                        "To": [
                            {
                                "Email": new_user.email,
                                "Name": new_user.first_name
                            }
                        ],
                        "Subject": "Verify your Garfield Event Account!",
                        "HTMLPart": html,
                    }
                ]
            }

            respone = mailjet.send.create(data=data)
            print(respone)
            print("email sent to ", new_user.email)
            db.session.commit()
            new_user.id
        except Exception as Error:
            print(Error)
            flash("Error on creating your email, please check your information again.")
            return render_template("/root/register.html")
        else:
            flash("Successful created your account, please verify your account \
                   with the key we sent to you though email.")
            return redirect("/login")


@root_blueprint.route('/forgot', methods=["GET", "POST"])
def forgot():
    if request.method == "GET":
        return render_template("/root/forgot.html")
    if request.method == "POST":
        pass


@root_blueprint.route('/verify/<string:token>', methods=["GET", "POST"])
def verify(token=None):
    if request.method == "GET":
        if not token:
            flash("Access denied!")
            return redirect("/")
        try:
            encoder.loads(token, salt='email-verify', max_age=60 * 60 * 24)
        except SignatureExpired:
            decoded_email = encoder.loads(token, salt='email-verify')
            verify_token = str(encoder.dumps(decoded_email, salt="email-verify"))
            user = Users.query.filter_by(email=decoded_email).first()
            html = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
              <meta name="viewport" content="width=device-width, initial-scale=1.0" />
              <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
              <title>Verify your email address</title>
              <style type="text/css" rel="stylesheet" media="all">
                /* Base ------------------------------ */
                *:not(br):not(tr):not(html) {
                  font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
                  -webkit-box-sizing: border-box;
                  box-sizing: border-box;
                }
                body {
                  width: 100% !important;
                  height: 100%;
                  margin: 0;
                  line-height: 1.4;
                  background-color: #F5F7F9;
                  color: #839197;
                  -webkit-text-size-adjust: none;
                }
                a {
                  color: #414EF9;
                }
                /* Layout ------------------------------ */
                .email-wrapper {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  background-color: #F5F7F9;
                }
                .email-content {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                }
                /* Masthead ----------------------- */
                .email-masthead {
                  padding: 25px 0;
                  text-align: center;
                }
                .email-masthead_logo {
                  max-width: 400px;
                  border: 0;
                }
                .email-masthead_name {
                  font-size: 16px;
                  font-weight: bold;
                  color: #839197;
                  text-decoration: none;
                  text-shadow: 0 1px 0 white;
                }
                /* Body ------------------------------ */
                .email-body {
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  border-top: 1px solid #E7EAEC;
                  border-bottom: 1px solid #E7EAEC;
                  background-color: #FFFFFF;
                }
                .email-body_inner {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                }
                .email-footer {
                  width: 570px;
                  margin: 0 auto;
                  padding: 0;
                  text-align: center;
                }
                .email-footer p {
                  color: #839197;
                }
                .body-action {
                  width: 100%;
                  margin: 30px auto;
                  padding: 0;
                  text-align: center;
                }
                .body-sub {
                  margin-top: 25px;
                  padding-top: 25px;
                  border-top: 1px solid #E7EAEC;
                }
                .content-cell {
                  padding: 35px;
                }
                .align-right {
                  text-align: right;
                }
                /* Type ------------------------------ */
                h1 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 19px;
                  font-weight: bold;
                  text-align: left;
                }
                h2 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 16px;
                  font-weight: bold;
                  text-align: left;
                }
                h3 {
                  margin-top: 0;
                  color: #292E31;
                  font-size: 14px;
                  font-weight: bold;
                  text-align: left;
                }
                p {
                  margin-top: 0;
                  color: #839197;
                  font-size: 16px;
                  line-height: 1.5em;
                  text-align: left;
                }
                p.sub {
                  font-size: 12px;
                }
                p.center {
                  text-align: center;
                }
                /* Buttons ------------------------------ */
                .button {
                  display: inline-block;
                  width: 200px;
                  background-color: #414EF9;
                  border-radius: 3px;
                  color: #ffffff;
                  font-size: 15px;
                  line-height: 45px;
                  text-align: center;
                  text-decoration: none;
                  -webkit-text-size-adjust: none;
                  mso-hide: all;
                }
                .button--green {
                  background-color: #28DB67;
                }
                .button--red {
                  background-color: #FF3665;
                }
                .button--blue {
                  background-color: #414EF9;
                }
                /*Media Queries ------------------------------ */
                @media only screen and (max-width: 600px) {
                  .email-body_inner,
                  .email-footer {
                    width: 100% !important;
                  }
                }
                @media only screen and (max-width: 500px) {
                  .button {
                    width: 100% !important;
                  }
                }
              </style>
            </head>
            <body>
              <table class="email-wrapper" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <table class="email-content" width="100%" cellpadding="0" cellspacing="0">
                      <!-- Logo -->
                      <tr>
                        <td class="email-masthead">
                          <a class="email-masthead_name">Garfield Events Corporations</a>
                        </td>
                      </tr>
                      <!-- Email Body -->
                      <tr>
                        <td class="email-body" width="100%">
                          <table class="email-body_inner" align="center" width="570" cellpadding="0" cellspacing="0">
                            <!-- Body content -->
                            <tr>
                              <td class="content-cell">
                                <h1>Verify your email address</h1>
                                <p>Thanks for signing up for Garfield Events! We're excited to have you as an early user.</p>
                                <!-- Action -->
                                <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0">
                                  <tr>
                                    <td align="center">
                                      <div>
                                        <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://127.0.0.1:5000/verify/""" + verify_token + """" style="height:45px;v-text-anchor:middle;width:200px;" arcsize="7%" stroke="f" fill="t">
                                        <v:fill type="tile" color="#414EF9" />
                                        <w:anchorlock/>
                                        <center style="color:#ffffff;font-family:sans-serif;font-size:15px;">Verify Email</center>
                                      </v:roundrect><![endif]-->
                                        <a href="http://127.0.0.1:5000/verify/""" + verify_token + """" style="color:white;" class="button button--blue">Verify Email</a>
                                      </div>
                                    </td>
                                  </tr>
                                </table>
                                <p>Thanks,<br>The Garfield Events Team</p>
                                <!-- Sub copy -->
                                <table class="body-sub">
                                  <tr>
                                    <td>
                                      <p class="sub">If you’re having trouble clicking the button, copy and paste the URL below into your web browser.
                                      </p>
                                      <p class="sub"><a href="http://127.0.0.1:5000/verify/""" + verify_token + """"</a></p>
                                    </td>
                                  </tr>
                                </table>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <table class="email-footer" align="center" width="570" cellpadding="0" cellspacing="0">
                            <tr>
                              <td class="content-cell">
                                <p class="sub center">
                                  Garfield Events, Inc.
                                  <br>325 9th St, San Francisco, CA 94103
                                </p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </body>
            </html>
            """

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "noreply@garfdev.space",
                            "Name": "Garfield Event"
                        },
                        "To": [
                            {
                                "Email": decoded_email,
                                "Name": user.first_name
                            }
                        ],
                        "Subject": "Verify your Garfield Event Account!",
                        "HTMLPart": html,
                    }
                ]
            }

            respone = mailjet.send.create(data=data)
            flash("Your token is expired, don't worry, we just sent a new token to you!")
            return redirect("/")
        except:
            flash("Error while progressing your token, please check your email and correct it!")
            return render_template("/root/verifyfailed.html")
        else:
            decoded_email = encoder.loads(token, salt='email-verify')
            print("decoded_email", decoded_email)
            user = Users.query.filter_by(email=decoded_email).first()
            user.email_verified = True
            new_order = Order_History(status="NOT COMPLETE",
                                      created_at=int(time.time()),
                                      updated_at=int(time.time()),
                                      buyer_id=user.id)
            db.session.add(new_order)
            db.session.commit()
            return render_template("/root/verify.html")
