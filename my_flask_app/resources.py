from flask_restful import Resource, reqparse
from models import db, Customer, Order

# Recurso para manejar clientes individuales
class CustomerResource(Resource):
    def get(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'message': 'No hay Clientes'}, 404
        return {'id': customer.id, 'name': customer.name, 'status': customer.status}, 200


    def delete(self, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Cliente eliminado satisfactoriamente.'}, 200

    def put(self, customer_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
        parser.add_argument('status', type=str, required=True, help='Status cannot be blank!')
        data = parser.parse_args()
        
        customer = Customer.query.get_or_404(customer_id)
        customer.name = data['name']
        customer.status = data['status']
        
        db.session.commit()
        return {'message': 'Cliente cargado correctamente.'}, 200

# Recurso para manejar lista de clientes
class CustomerListResource(Resource):
    def get(self):
        customers = Customer.query.all()
        return [{'id': customer.id, 'name': customer.name, 'status': customer.status} for customer in customers], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
        parser.add_argument('status', type=str, required=True, help='Status cannot be blank!')
        data = parser.parse_args()
        
        new_customer = Customer(name=data['name'], status=data['status'])
        db.session.add(new_customer)
        db.session.commit()
        
        return {'message': 'Customer created successfully.'}, 201

# Recurso para manejar pedidos individuales
class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return {'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date}, 200

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully.'}, 200

    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('customer_id', type=int, required=True, help='Customer ID cannot be blank!')
        parser.add_argument('order_date', type=str, required=True, help='Order Date cannot be blank!')
        data = parser.parse_args()
        
        order = Order.query.get_or_404(order_id)
        order.customer_id = data['customer_id']
        order.order_date = data['order_date']
        
        db.session.commit()
        return {'message': 'Order updated successfully.'}, 200

# Recurso para manejar lista de pedidos
class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [{'id': order.id, 'customer_id': order.customer_id, 'order_date': order.order_date} for order in orders], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('customer_id', type=int, required=True, help='Customer ID cannot be blank!')
        parser.add_argument('order_date', type=str, required=True, help='Order Date cannot be blank!')
        data = parser.parse_args()
        
        new_order = Order(customer_id=data['customer_id'], order_date=data['order_date'])
        db.session.add(new_order)
        db.session.commit()
        
        return {'message': 'Order created successfully.'}, 201

# Recurso para eliminar todos los clientes
class DeleteAllCustomersResource(Resource):
    def delete(self):
        try:
            num_rows_deleted = db.session.query(Customer).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} customers deleted successfully.'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred while deleting customers.', 'error': str(e)}, 500
