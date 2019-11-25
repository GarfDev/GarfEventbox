from src import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from src import qrgen
from datetime import datetime
import time


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Integer, nullable=True)
    address = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.Integer, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(60), default="USER")
    organize = db.Column(db.String(100), nullable=True)
    organize_desc = db.Column(db.String, nullable=True)
    organize_email = db.Column(db.String, nullable=True)
    organize_phone = db.Column(db.String, nullable=True)
    organize_avatar = db.Column(db.String, nullable=True)
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    # RELATIONSHIP_COLUMNS
    order_history = db.relationship("Order_History", backref='owner', lazy=True)
    rating_history = db.relationship("Rating_Hitory", backref='owner', lazy=True)
    event_history = db.relationship("Events", backref='owner', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    short_desc = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String, default="# Welcome to Garfield Event Markdown Editor!\r\nHi! I'm your first Markdown "
                                        "file in **Garfield Event**. If you want to learn about markdown, "
                                        "you can [read here]("
                                        "https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet). That "
                                        "important cause we using markdown to layout your excellent event content!")
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    feature_pic = db.Column(db.String, nullable=True)
    status = db.Column(db.String(50), default="CREATING")
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer, nullable=False)
    # RELATIONSHIP_COLUMNS
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tickets = db.relationship('Tickets', backref='event', lazy=True)
    rating = db.relationship('Rating_Hitory', backref='event', lazy=True)
    type = db.relationship("Category", secondary="eventcategory", backref=db.backref('event'))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)


class EventCategory(db.Model):
    __tablename__ = 'eventcategory'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, default=0)
    # RELATIONSHIP_COLUMNS
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    order_items_id = db.relationship("Order_Item", backref='ticket', lazy=True)


class Order_History(db.Model):
    __tablename__ = 'order_history'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer, nullable=False)
    # RELATIONSHIP_COLUMNS
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_items = db.relationship("Order_Item", backref='order', lazy=True)

    def get_bill(self):
        return Order_Item.query.join(Tickets).with_entities(
            Tickets.id.label("id"), Tickets.title.label("name"),
            Tickets.tier.label("tier"), Tickets.price.label("quality"),
            Tickets.desc.label("desc"),
            func.count(Tickets.id).label("quality"),
            func.sum(Tickets.price).label("amount")
            ).filter(Order_Item.order_id == self.id).group_by(
            Tickets.id).all()


class Order_Item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String, nullable=True)
    # RELATIONSHIP_COLUMNS
    order_id = db.Column(db.Integer, db.ForeignKey('order_history.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    status = db.Column(db.String(15), default="NOT-USED")

    def changestatus(self, content):
        self.status = content


class Rating_Hitory(db.Model):
    __tablename__ = 'rating_history'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String, nullable=False)
    # RELATIONSHIP_COLUMN
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)


db.create_all()
