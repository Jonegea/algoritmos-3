from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#Representa a un cliente con atributos como id, name y status.
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    status = db.Column(db.String(10))
#Representa un pedido con atributos como id, customer_id y order_date.
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.String(10))
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
