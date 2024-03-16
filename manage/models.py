from manage import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime 
from sqlalchemy import LargeBinary
import uuid

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(500))

    orders = db.relationship('Order', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    admin_name = db.Column(db.String(150))
    phone_number = db.Column(db.Integer)
    admin_password = db.Column(db.String(500))

    def __repr__(self):
        return f"Admin('{self.admin_name}', '{self.email}')"

class WarehouseAccount(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(500))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'))
    warehouse = db.relationship('Warehouse', backref=db.backref('accounts', lazy=True))

class Warehouse(db.Model):
    warehouse_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    hotline = db.Column(db.String(150))

    def __repr__(self):
        return f"Warehouse('{self.name}', '{self.address}')"

class Transport(db.Model):
    transport_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    cost = db.Column(db.Float)

    orders = db.relationship('Order', backref=db.backref('transport', lazy=True))

class Shift(db.Model):
    shift_id = db.Column(db.Integer, primary_key=True)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)
    employee_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))
    day = db.Column(db.Date)

    employee = db.relationship('Admin', backref=db.backref('shifts', lazy=True))

class Sender(db.Model):
    sender_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    address = db.Column(db.String(150))

    orders = db.relationship('Order', backref=db.backref('sender', lazy=True))

class Receiver(db.Model):
    receiver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    address = db.Column(db.String(150))

    orders = db.relationship('Order', backref=db.backref('receiver', lazy=True))

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(150))
    number_of_product = db.Column(db.Integer)
    transport_id = db.Column(db.Integer, db.ForeignKey('transport.transport_id'))
    cod = db.Column(db.Float)
    transport_fee = db.Column(db.Float)
    note = db.Column(db.String(500))
    record_at = db.Column(db.DateTime)
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.receiver_id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('sender.sender_id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'))
    status = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    cancel_at = db.Column(db.DateTime)
    complete_at = db.Column(db.DateTime)
    confirm_at = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class CusAccount(db.Model):
    cus_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(500))

    def __repr__(self):
        return f"CusAccount('{self.name}', '{self.username}')"