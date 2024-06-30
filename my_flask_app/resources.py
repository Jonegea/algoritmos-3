from flask_restful import Resource, reqparse
from models import db, Customer, Order

customer_parser = reqparse.RequestParser()
customer_parser.add_argument('name', type=str, required=True, help="Name is required")
customer_parser.add_argument('status', type=str, required=True, help="Status is required")

order_parser = reqparse.RequestParser()
order_parser.add_argument('customer_id', type=int, required=True, help="Customer ID is required")
order_parser.add_argument('order_date', type=str, required=True, help="Order Date is required")

class CustomerResource(Resource):
    def get(self, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        return {'id': customer.id, 'name': customer.name, 'status': customer.status}

    def put(self, customer_id):
        args = customer_parser.parse_args()
        customer = Customer.query.get_or_404(customer_id)
        customer.name = args['name']
        customer.status = args['status']
        db.session.commit()
        return {'message': 'Customer updated'}

    def delete(self, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted'}

class CustomerListResource(Resource):
    def get(self):
        customers = Customer.query.all()
        return [{'id': customer.id, 'name': customer.name, 'status': customer.status} for customer in customers]

    def post(self):
        args = customer_parser.parse_args()
        customer = Customer(name=args['name'], status=args['status'])
        db.session.add(customer)
        db.session.commit()
        return {'message': 'Customer created'}, 201

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return {'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date}

    def put(self, order_id):
        args = order_parser.parse_args()
        order = Order.query.get_or_404(order_id)
        order.customer_id = args['customer_id']
        order.order_date = args['order_date']
        db.session.commit()
        return {'message': 'Order updated'}

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted'}

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [{'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date} for order in orders]

    def post(self):
        args = order_parser.parse_args()
        order = Order(customer_id=args['customer_id'], order_date=args['order_date'])
        db.session.add(order)
        db.session.commit()
        return {'message': 'Order created'}, 201
