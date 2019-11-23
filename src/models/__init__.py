from src import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer, nullable=False)
    # RELATIONSHIP_COLUMNS
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tickets = db.relationship('Tickets', backref='event', lazy=True)
    rating = db.relationship('Rating_Hitory', backref='event', lazy=True)
    type = db.relationship("EventCategory", backref='event', lazy=True)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    events = db.relationship("EventCategory", backref='category', lazy=True)


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


class Order_Item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    # RELATIONSHIP_COLUMNS
    order_id = db.Column(db.Integer, db.ForeignKey('order_history.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    status = db.Column(db.String(15), default="NOT-USED")


class Rating_Hitory(db.Model):
    __tablename__ = 'rating_history'
    id = db.Column(db.Integer, primary_key=True)
    # RELATIONSHIP_COLUMN
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String, nullable=False)

db.create_all()