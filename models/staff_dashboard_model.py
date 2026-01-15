"""
Staff Dashboard Model
Handles data operations for staff dashboard
"""
import datetime
from db.activity_db import activity_db
from db.menu_db import menu_db
from db.orders_db import orders_db_instance as orders_db


class StaffDashboardModel:
    """Model for staff dashboard operations"""

    def __init__(self, staff_info):
        self.staff_info = staff_info
        self.staff_name = staff_info.get("staff_name", "Staff")
        self.staff_email = staff_info.get("staff_email", "")
        self.staff_id = staff_info.get("staff_id", "")

        if not self.staff_id:
            self.staff_id = staff_info.get("id", "")

        # Create activity logs table if it doesn't exist
        activity_db.create_table()

        # Add initial activity log for staff login
        self.log_activity("Staff logged in")

    def log_activity(self, action, details=""):
        """Log staff activities"""
        return activity_db.add_activity(
            staff_name=self.staff_name,
            staff_id=self.staff_id,
            action=action,
            details=details
        )

    def load_menu_items(self):
        """Load menu items from database"""
        try:
            menu_items_data = menu_db.get_all_menu_items()

            # Convert database format to app format
            menu_items = []
            for item in menu_items_data:
                menu_items.append({
                    "id": item['id'],
                    "title": item['name'],
                    "description": item['description'],
                    "category": item['category'],
                    "price": str(item['price']),
                    "image": item['image_url']
                })

            return menu_items

        except Exception as e:
            print(f"Error loading menu items from database: {e}")
            # Return sample data if database fails
            return self._get_sample_menu_items()

    def _get_sample_menu_items(self):
        """Return sample menu items for fallback"""
        return [
            {
                "id": 1,
                "title": "Classic Burger",
                "description": "Juicy beef patty with fresh veggies and homemade sauce that's perfect for any craving.",
                "category": "Burgers",
                "price": "159",
                "image": "picture/burger.png"
            },
            {
                "id": 2,
                "title": "Crispy Fries",
                "description": "Golden crispy potato fries cooked to perfection and best served hot.",
                "category": "Sides",
                "price": "79",
                "image": "picture/fries.png"
            },
            {
                "id": 3,
                "title": "Fried Chicken",
                "description": "Crispy fried chicken with tender and juicy meat inside.",
                "category": "Chicken",
                "price": "189",
                "image": "picture/chicken.png"
            },
            {
                "id": 4,
                "title": "Milk Tea",
                "description": "Classic milk tea with brown sugar pearls and creamy flavor.",
                "category": "Drinks",
                "price": "99",
                "image": "picture/milktea.png"
            },
            {
                "id": 5,
                "title": "Pepperoni Pizza",
                "description": "Loaded with pepperoni slices and special cheese blend.",
                "category": "Pizza",
                "price": "349",
                "image": "picture/pizza.png"
            },
        ]

    def add_menu_item(self, title, description, category, price, image):
        """Add new menu item to database"""
        try:
            success, message = menu_db.create_menu_item(
                name=title,
                description=description,
                category=category,
                price=float(price) if '.' in price else int(price),
                image_url=image
            )
            return success, message
        except ValueError:
            return False, "Price must be a number!"
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def update_menu_item(self, item_id, title, description, category, price, image):
        """Update menu item in database"""
        try:
            success, message = menu_db.update_menu_item(
                item_id=item_id,
                name=title,
                description=description,
                category=category,
                price=float(price) if '.' in price else int(price),
                image_url=image
            )
            return success, message
        except ValueError:
            return False, "Price must be a number!"
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def delete_menu_item(self, item_id, item_name):
        """Delete menu item from database"""
        success, message = menu_db.delete_menu_item(item_id)
        return success, message

    def load_todays_orders(self):
        """Load today's orders from database"""
        try:
            # Get today's date
            today = datetime.date.today()

            # Get orders from database
            success, orders = orders_db.get_all_orders()

            if not success or not orders:
                return []

            # Filter orders to show only today's orders
            today_orders = []
            for order in orders:
                order_date = order.get('created_at', '')

                # Handle different date formats
                if isinstance(order_date, str):
                    if ' ' in order_date:
                        date_part = order_date.split(' ')[0]
                    else:
                        date_part = order_date

                    try:
                        order_date_obj = datetime.datetime.strptime(date_part, '%Y-%m-%d').date()
                        if order_date_obj == today:
                            today_orders.append(order)
                    except ValueError:
                        pass

                elif hasattr(order_date, 'date'):
                    if order_date.date() == today:
                        today_orders.append(order)

                elif isinstance(order_date, datetime.date):
                    if order_date == today:
                        today_orders.append(order)

            return today_orders

        except Exception as e:
            print(f"Error loading orders: {e}")
            return []

    def update_order_status(self, order_id, new_status):
        """Update order status in database"""
        return orders_db.update_order_status(order_id, new_status)

    def get_order_by_id(self, order_id):
        """Get order by ID"""
        success, orders = orders_db.get_all_orders()
        if success:
            for order in orders:
                if order.get('id') == order_id:
                    return order
        return None