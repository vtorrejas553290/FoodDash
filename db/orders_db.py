# orders_db.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
import random
import string


class orders_db:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(orders_db, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'food_dash_db'
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def test_connection(self):
        """Test database connection"""
        try:
            if self.connect():
                self.disconnect()
                return True, "Connected successfully"
            return False, "Failed to connect"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def generate_order_number(self):
        """Generate unique order number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.digits, k=4))
        return f"ORD-{timestamp}-{random_str}"

    def create_order(self, customer_id, customer_info, cart_items, subtotal, delivery_fee=50.00, notes=""):
        """Create a new order in database"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            order_number = self.generate_order_number()
            total_amount = subtotal + delivery_fee

            # Serialize cart items as JSON
            items_json = json.dumps(cart_items, default=str)

            # Insert order
            query = """
            INSERT INTO orders (
                order_number, customer_id, customer_name, customer_email, 
                customer_phone, customer_address, items, subtotal, 
                delivery_fee, total_amount, notes, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                order_number, customer_id, customer_info['full_name'],
                customer_info['email'], customer_info['phone'],
                customer_info['address'], items_json, subtotal,
                delivery_fee, total_amount, notes, 'pending'
            )

            self.cursor.execute(query, values)
            order_id = self.cursor.lastrowid

            # Insert order items
            for item in cart_items:
                # Find menu item ID
                menu_query = "SELECT id, price FROM menu_items WHERE name = %s"
                self.cursor.execute(menu_query, (item['title'],))
                menu_item = self.cursor.fetchone()

                if menu_item:
                    item_query = """
                    INSERT INTO order_items (
                        order_id, order_number, menu_item_id, menu_item_name,
                        quantity, price, total_price
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    item_values = (
                        order_id, order_number, menu_item['id'], item['title'],
                        item['qty'], float(item['price'].replace('₱', '')),
                        float(item['price'].replace('₱', '')) * item['qty']
                    )
                    self.cursor.execute(item_query, item_values)

            self.connection.commit()
            self.disconnect()

            return True, {
                'order_id': order_id,
                'order_number': order_number,
                'total_amount': total_amount
            }

        except Error as e:
            print(f"Error creating order: {e}")
            if self.connection:
                self.connection.rollback()
            self.disconnect()
            return False, f"Failed to create order: {str(e)}"
        except Exception as e:
            print(f"Unexpected error creating order: {e}")
            self.disconnect()
            return False, f"Unexpected error: {str(e)}"

    def get_customer_orders(self, customer_id):
        """Get all orders for a specific customer"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            query = """
            SELECT o.*, 
                   GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.customer_id = %s
            GROUP BY o.id
            ORDER BY o.created_at DESC
            """
            self.cursor.execute(query, (customer_id,))
            orders = self.cursor.fetchall()

            # Parse items JSON
            for order in orders:
                if 'items' in order and order['items']:
                    try:
                        order['items'] = json.loads(order['items'])
                    except:
                        order['items'] = []

            self.disconnect()
            return True, orders

        except Error as e:
            print(f"Error fetching customer orders: {e}")
            self.disconnect()
            return False, f"Failed to fetch orders: {str(e)}"

    def get_all_orders(self, status=None):
        """Get all orders (for admin) with optional status filter"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            if status:
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.status = %s
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query, (status,))
            else:
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query)

            orders = self.cursor.fetchall()

            # Parse items JSON
            for order in orders:
                if 'items' in order and order['items']:
                    try:
                        order['items'] = json.loads(order['items'])
                    except:
                        order['items'] = []

            self.disconnect()
            return True, orders

        except Error as e:
            print(f"Error fetching all orders: {e}")
            self.disconnect()
            return False, f"Failed to fetch orders: {str(e)}"

    def get_order_details(self, order_id):
        """Get detailed information for a specific order"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            # Get order info
            order_query = "SELECT * FROM orders WHERE id = %s"
            self.cursor.execute(order_query, (order_id,))
            order = self.cursor.fetchone()

            if not order:
                self.disconnect()
                return False, "Order not found"

            # Get order items
            items_query = "SELECT * FROM order_items WHERE order_id = %s"
            self.cursor.execute(items_query, (order_id,))
            items = self.cursor.fetchall()

            # Parse items JSON if exists
            if 'items' in order and order['items']:
                try:
                    order['items'] = json.loads(order['items'])
                except:
                    order['items'] = []

            order['order_items'] = items

            self.disconnect()
            return True, order

        except Error as e:
            print(f"Error fetching order details: {e}")
            self.disconnect()
            return False, f"Failed to fetch order details: {str(e)}"

    def update_order_status(self, order_id, status):
        """Update order status"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            query = "UPDATE orders SET status = %s WHERE id = %s"
            self.cursor.execute(query, (status, order_id))
            self.connection.commit()

            # Get updated order
            updated_query = "SELECT * FROM orders WHERE id = %s"
            self.cursor.execute(updated_query, (order_id,))
            updated_order = self.cursor.fetchone()

            if updated_order and 'items' in updated_order and updated_order['items']:
                try:
                    updated_order['items'] = json.loads(updated_order['items'])
                except:
                    updated_order['items'] = []

            self.disconnect()
            return True, updated_order

        except Error as e:
            print(f"Error updating order status: {e}")
            if self.connection:
                self.connection.rollback()
            self.disconnect()
            return False, f"Failed to update order status: {str(e)}"

    def get_order_stats(self):
        """Get order statistics"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            stats = {}

            # Total orders
            self.cursor.execute("SELECT COUNT(*) as count FROM orders")
            stats['total_orders'] = self.cursor.fetchone()['count']

            # Total revenue
            self.cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as revenue FROM orders")
            stats['total_revenue'] = self.cursor.fetchone()['revenue']

            # Today's orders
            self.cursor.execute("""
                SELECT COUNT(*) as count 
                FROM orders 
                WHERE DATE(created_at) = CURDATE()
            """)
            stats['today_orders'] = self.cursor.fetchone()['count']

            # Pending orders
            self.cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'pending'")
            stats['pending_orders'] = self.cursor.fetchone()['count']

            # Orders by status
            self.cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM orders 
                GROUP BY status
            """)
            stats['status_counts'] = self.cursor.fetchall()

            # Recent orders (last 7 days)
            self.cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count, SUM(total_amount) as revenue
                FROM orders 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DATE(created_at)
                ORDER BY date
            """)
            stats['recent_days'] = self.cursor.fetchall()

            self.disconnect()
            return True, stats

        except Error as e:
            print(f"Error fetching order stats: {e}")
            self.disconnect()
            return False, f"Failed to fetch order stats: {str(e)}"

    def search_orders(self, search_term, search_by="order_number"):
        """Search orders by various criteria"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            if search_by == "order_number":
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.order_number LIKE %s
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query, (f"%{search_term}%",))
            elif search_by == "customer_name":
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.customer_name LIKE %s
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query, (f"%{search_term}%",))
            elif search_by == "customer_email":
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.customer_email LIKE %s
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query, (f"%{search_term}%",))
            else:
                query = """
                SELECT o.*, 
                       GROUP_CONCAT(CONCAT(oi.quantity, 'x ', oi.menu_item_name) SEPARATOR ', ') as item_summary
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                WHERE o.order_number LIKE %s OR o.customer_name LIKE %s OR o.customer_email LIKE %s
                GROUP BY o.id
                ORDER BY o.created_at DESC
                """
                self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))

            orders = self.cursor.fetchall()

            # Parse items JSON
            for order in orders:
                if 'items' in order and order['items']:
                    try:
                        order['items'] = json.loads(order['items'])
                    except:
                        order['items'] = []

            self.disconnect()
            return True, orders

        except Error as e:
            print(f"Error searching orders: {e}")
            self.disconnect()
            return False, f"Failed to search orders: {str(e)}"

    def get_todays_revenue(self):
        """Get today's total revenue"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            query = """
            SELECT COALESCE(SUM(total_amount), 0) as revenue 
            FROM orders 
            WHERE DATE(created_at) = CURDATE()
            """
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            self.disconnect()
            return True, result['revenue'] if result else 0

        except Error as e:
            print(f"Error fetching today's revenue: {e}")
            self.disconnect()
            return False, f"Failed to fetch revenue: {str(e)}"

    def delete_order(self, order_id):
        """Delete an order (admin only)"""
        try:
            if not self.connect():
                return False, "Database connection failed"

            # Get order number before deletion for confirmation
            self.cursor.execute("SELECT order_number FROM orders WHERE id = %s", (order_id,))
            order = self.cursor.fetchone()

            if not order:
                self.disconnect()
                return False, "Order not found"

            # Delete order (cascade will delete order_items)
            delete_query = "DELETE FROM orders WHERE id = %s"
            self.cursor.execute(delete_query, (order_id,))
            self.connection.commit()

            self.disconnect()
            return True, f"Order {order['order_number']} deleted successfully"

        except Error as e:
            print(f"Error deleting order: {e}")
            if self.connection:
                self.connection.rollback()
            self.disconnect()
            return False, f"Failed to delete order: {str(e)}"


# Create singleton instance
orders_db_instance = orders_db()