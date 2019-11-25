from flask import Blueprint, request, url_for, render_template, redirect, flash
from flask_login import current_user, login_required, login_user, logout_user
from src.models import *
from src import db, mailjet, app, encoder
import time, re
from itsdangerous import SignatureExpired

order_blueprint = Blueprint('order', __name__
                            , template_folder="../../templates")


@order_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == "GET":
        return render_template("order/cart.html", items=current_user.order_history[-1].get_bill())
    if request.method == "POST":
        try:
            for item in current_user.order_history[-1].order_items:
                db.session.delete(item)
                db.session.commit()
            dict_to_buy = request.form.to_dict()
            for key in dict_to_buy:
                ticket = Tickets.query.get(key)
                if int(dict_to_buy[key]) > ticket.number:
                    flash("This ticket sold out:", ticket.title)
                    return redirect("/order")
                for ticket in range(int(dict_to_buy[key])):
                    new_item = Order_Item(ticket_id=key,
                                          order_id=current_user.order_history[-1].id)
                    db.session.add(new_item)
        except:
            flash("Some Error Happened, please try again.")
            return redirect("/order")
        else:
            db.session.commit()
            return redirect(f"/event/{id}")
