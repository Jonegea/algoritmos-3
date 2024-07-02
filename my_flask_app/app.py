from flask import Flask, g
from flask_restful import Api
from models import db
from resources import CustomerResource, CustomerListResource, OrderResource, OrderListResource, DeleteAllCustomersResource
from database import init_db, create_tables, populate_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
api = Api(app)

db_initialized = False  # Variable global para rastrear la inicialización de la base de datos

@app.before_request
def setup_database():
    global db_initialized
    if not db_initialized:
        create_tables(app)
        populate_db(app)
        db_initialized = True

api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:customer_id>')
api.add_resource(OrderListResource, '/orders')
api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(DeleteAllCustomersResource, '/customers/delete_all')

if __name__ == '__main__':
    app.run(debug=True)
