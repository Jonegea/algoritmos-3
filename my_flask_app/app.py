from flask import Flask, g
from flask_restful import Api
from models import db
from resources import CustomerResource, CustomerListResource, OrderResource, OrderListResource
from database import init_db, create_tables, populate_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
api = Api(app)

@app.before_request
def setup_database():
    if not hasattr(g, 'db_initialized'):
        create_tables(app)
        populate_db(app)
        g.db_initialized = True

api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:customer_id>')
api.add_resource(OrderListResource, '/orders')
api.add_resource(OrderResource, '/orders/<int:order_id>')

if __name__ == '__main__':
    app.run(debug=True)
