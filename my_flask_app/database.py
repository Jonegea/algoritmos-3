import os
from models import db, Customer, Order

def init_db(app):
    db.init_app(app)

def create_tables(app):
    with app.app_context():
        # Eliminar la base de datos si ya existe
        if os.path.exists('database.db'):
            os.remove('database.db')
        db.create_all()

def populate_db(app):
    with app.app_context():
        customers = [
            Customer(id=1, name='John Doe', status='active'),
            Customer(id=2, name='Robert Roe', status='inactive'),
            Customer(id=3, name='Sammy Soe', status='active')
        ]
        
        orders = [
            Order(id=1, customer_id=3, order_date='2020-12-06'),
            Order(id=2, customer_id=2, order_date='2020-12-06')
        ]
        
        db.session.bulk_save_objects(customers)
        db.session.bulk_save_objects(orders)
        db.session.commit()
