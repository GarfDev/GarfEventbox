from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from src.models import *
from src import db, mailjet, app, encoder
import time, re
from itsdangerous import SignatureExpired

event_blueprint = Blueprint('event', __name__
                            , template_folder="../../templates")


@event_blueprint.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "GET":
        return render_template("event/create.html")
    if request.method == "POST":
        print(request.form)
        try:
            new_event = Events(title=request.form['title'],
                               start_time=time.mktime(
                                   datetime.strptime(request.form['start_time'], "%m/%d/%Y").timetuple()),
                               end_time=time.mktime(
                                   datetime.strptime(request.form['end_time'], "%m/%d/%Y").timetuple()),
                               address=request.form['address'],
                               short_desc=request.form['short_desc'],
                               feature_pic=request.form['feature_pic'],
                               created_at=int(time.time()),
                               updated_at=int(time.time()),
                               host_id=current_user.id)
            db.session.add(new_event)
            db.session.commit()
            new_category = EventCategory(event_id=new_event.id,
                                         category_id=request.form['event_type'])
            db.session.add(new_category)
            db.session.commit()
            flash("Successful created your event, let's update more information for it!")
            return redirect(f"/event/{new_event.id}/editor")
        except Exception as Error:
            print("Error from event editor", Error)
            return render_template("event/create.html")


@event_blueprint.route("/<int:id>", methods=['GET', 'POST'])
def event(id):
    if request.method == "GET":
        event = Events.query.get(id)
        if not event:
            flash("Sorry but this event not exist, please try again.")
            return redirect("/event")
        return render_template("event/event.html", event=event, time=time)
    if request.method == "POST":
        print(request.form)
        for key, value in request.form:
            print(f"{key} | {value}")
        return redirect(f"/event/{id}")


@event_blueprint.route("/<int:id>/editor", methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == "GET":
        event = Events.query.get(id)
        if not event:
            flash(
                "Cannot find this event in our database, please contact administrator if you believe this is an error")
            return redirect("/event")
        return render_template("event/edit.html", desc=event.desc)
    if request.method == "POST":
        try:
            event = Events.query.get(id)
            event.desc = request.form['markdown-desc']
            db.session.commit()
            return redirect(f"/event/{id}/editor")
        except Exception as Error:
            print("Error from editor", Error)
            return redirect(f"/event/{id}/editor")
        return render_template("event/edit.html")


@event_blueprint.route("/<int:id>/ticket-editor", methods=['GET', 'POST'])
@login_required
def edit_ticket(id):
    if request.method == "GET":
        event = Events.query.get(id)
        if not event:
            flash("Sorry but we cannot found this event.")
            return redirect("/")
        return render_template("event/ticket-editor.html", event=event)
    if request.method == "POST":
        try:
            new_ticket = Tickets(tier=request.form['tier'],
                                 title=request.form['title'],
                                 price=request.form['price'],
                                 desc=request.form['desc'],
                                 event_id=id)
            db.session.add(new_ticket)
            db.session.commit()
        except:
            flash("Error while add your ticket")
            return redirect(f"/event/{id}/ticket-editor")
        else:
            return redirect(f"/event/{id}/ticket-editor")
