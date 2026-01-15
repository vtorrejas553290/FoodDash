# admin_dashboard_model.py
import sys
import numpy as np
from datetime import datetime, timedelta, date
import calendar

# Database imports
from db.activity_db import activity_db
from db.orders_db import orders_db_instance as orders_db
from db.menu_db import menu_db
from db.staff_db import staff_db
from db.customer_db import customer_db


class AdminDashboardModel:
    """Model for Admin Dashboard - Handles all data operations"""

    def __init__(self, admin_info=None):
        # Handle both old and new parameter formats
        if isinstance(admin_info, dict):
            # New format: admin_info dictionary
            self.admin_name = admin_info.get('admin_name', 'Admin User')
            self.admin_id = admin_info.get('admin_id', 'ADM00000')
        elif isinstance(admin_info, str):
            # Old format: just admin_name string
            self.admin_name = admin_info
            self.admin_id = "ADM00000"
        else:
            # Default if nothing provided
            self.admin_name = "Admin User"
            self.admin_id = "ADM00000"

        # Initialize data containers
        self.menu_items = []
        self.all_users = []
        self.active_user_count = 0
        self.current_revenue = 0
        self.order_stats = {}

        # Load initial data
        self.load_menu_items_from_db()
        self.load_users_from_db()
        self.load_analytics_data()

    def load_menu_items_from_db(self):
        """Load menu items from database"""
        try:
            menu_items_data = menu_db.get_all_menu_items()

            # Convert database format to our app format
            self.menu_items = []
            for item in menu_items_data:
                self.menu_items.append({
                    "id": item['id'],  # Store database ID
                    "title": item['name'],
                    "description": item['description'],
                    "category": item['category'],
                    "price": str(item['price']),  # Convert to string
                    "image": item['image_url']
                })

            return self.menu_items

        except Exception as e:
            print(f"Error loading menu items from database: {e}")
            # Return sample data if database fails
            self.menu_items = [
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
            return self.menu_items

    def load_analytics_data(self):
        """Load analytics data from database"""
        try:
            # Use the get_order_stats method from orders_db
            success, stats = orders_db.get_order_stats()
            if success:
                self.order_stats = stats
            else:
                self.order_stats = {}
                print(f"Error loading analytics: {stats}")
        except Exception as e:
            print(f"Error loading analytics data: {e}")
            self.order_stats = {}

    def get_total_revenue_from_db(self):
        """Calculate total revenue from all completed orders"""
        try:
            # Use the stats if available
            if hasattr(self, 'order_stats') and self.order_stats:
                revenue = float(self.order_stats.get('total_revenue', 0))
                return revenue

            # Fallback to manual calculation
            total_revenue = 0
            success, orders = orders_db.get_all_orders()
            if success:
                for order in orders:
                    if order.get('status', '').lower() == 'completed':
                        total_revenue += float(order.get('total_amount', 0))
            return total_revenue
        except Exception as e:
            print(f"Error getting total revenue: {e}")
            return 0

    def get_todays_orders_count(self):
        """Get count of today's orders from database"""
        try:
            # Use the stats if available
            if hasattr(self, 'order_stats') and self.order_stats:
                return int(self.order_stats.get('today_orders', 0))

            # Fallback
            return 0
        except Exception as e:
            print(f"Error counting today's orders: {e}")
            return 0

    def get_pending_orders_count(self):
        """Get count of pending orders from database"""
        try:
            # Use the stats if available
            if hasattr(self, 'order_stats') and self.order_stats:
                return int(self.order_stats.get('pending_orders', 0))

            # Fallback
            return 0
        except Exception as e:
            print(f"Error counting pending orders: {e}")
            return 0

    def load_users_from_db(self):
        """Load all users from database (customers and staff) - EXCLUDING ADMINS"""
        try:
            # Get all customers
            customers = customer_db.get_all_customers()
            # Get all staff
            staff_list = staff_db.get_all_staff()

            # Combine and format users (excluding admins)
            self.all_users = []

            # Add customers (excluding admins)
            for customer in customers:
                # Check if user is admin (adjust based on your database schema)
                is_admin = False
                # Check various ways admin might be identified
                if customer.get('role', '').lower() == 'admin':
                    is_admin = True
                elif customer.get('user_type', '').lower() == 'admin':
                    is_admin = True
                elif customer.get('email', '').lower().endswith('@admin.com'):
                    is_admin = True

                if not is_admin:
                    self.all_users.append({
                        "id": customer['id'],
                        "user_id": f"CUST{customer['id']:05d}",
                        "name": customer['full_name'],
                        "email": customer['email'],
                        "phone": customer.get('phone', ''),
                        "address": customer.get('address', ''),
                        "role": "Customer",  # First letter capitalized
                        "created_at": customer.get('created_at', ''),
                        "type": "customer"
                    })

            # Add staff (excluding admins)
            for staff in staff_list:
                # Check if staff is admin
                is_admin = False
                if staff.get('role', '').lower() == 'admin':
                    is_admin = True
                elif staff.get('staff_role', '').lower() == 'admin':
                    is_admin = True
                elif staff.get('staff_email', '').lower().endswith('@admin.com'):
                    is_admin = True

                if not is_admin:
                    # Get role from database, default to "Staff" with capital S
                    role_from_db = staff.get('role', 'Staff')
                    # Ensure first letter is capitalized
                    if role_from_db:
                        role = role_from_db[0].upper() + role_from_db[1:].lower() if role_from_db else "Staff"
                    else:
                        role = "Staff"

                    self.all_users.append({
                        "id": staff['id'],
                        "user_id": staff.get('staff_id', f"EMP{staff['id']:05d}"),
                        "name": staff['staff_name'],
                        "email": staff['staff_email'],
                        "phone": staff.get('staff_phone', ''),
                        "address": staff.get('staff_address', ''),
                        "role": role,  # First letter capitalized
                        "created_at": staff.get('created_at', ''),
                        "type": "staff"
                    })

            # Sort by ID
            self.all_users.sort(key=lambda x: x['id'])

            # Update active user count (excluding admins)
            self.active_user_count = len(self.all_users)

            return True

        except Exception as e:
            print(f"Error loading users from database: {e}")
            # If database fails, use sample data with proper capitalization
            self.all_users = [
                {
                    "id": 1,
                    "user_id": "CUST00001",
                    "name": "Juan Dela Cruz",
                    "email": "juan@email.com",
                    "role": "Customer"  # Capital C
                },
                {
                    "id": 2,
                    "user_id": "EMP00001",
                    "name": "Maria Santos",
                    "email": "maria@fooddash.com",
                    "role": "Staff"  # Capital S
                },
                {
                    "id": 3,
                    "user_id": "CUST00002",
                    "name": "Pedro Reyes",
                    "email": "pedro@email.com",
                    "role": "Customer"  # Capital C
                },
                {
                    "id": 4,
                    "user_id": "CUST00003",
                    "name": "Anna Lopez",
                    "email": "anna@email.com",
                    "role": "Customer"  # Capital C
                },
                {
                    "id": 5,
                    "user_id": "EMP00002",
                    "name": "Carlos Garcia",
                    "email": "carlos@fooddash.com",
                    "role": "Staff"  # Capital S
                },
                {
                    "id": 6,
                    "user_id": "CUST00004",
                    "name": "Sophia Martinez",
                    "email": "sophia@email.com",
                    "role": "Customer"  # Capital C
                },
            ]
            self.active_user_count = len(self.all_users)
            return False

    def get_all_orders(self):
        """Get all orders from database"""
        try:
            success, orders = orders_db.get_all_orders()
            if success:
                return orders
            return []
        except Exception as e:
            print(f"Error getting orders: {e}")
            return []

    def search_orders(self, search_term):
        """Search orders in database"""
        try:
            success, orders = orders_db.search_orders(search_term)
            if success:
                return orders
            return []
        except Exception as e:
            print(f"Error searching orders: {e}")
            return []

    def update_order_status(self, order_id, new_status):
        """Update order status in database"""
        try:
            return orders_db.update_order_status(order_id, new_status)
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False, str(e)

    def get_all_activities(self, limit=100):
        """Get all activity logs from database"""
        try:
            return activity_db.get_all_activities(limit=limit)
        except Exception as e:
            print(f"Error getting activities: {e}")
            return False, str(e)

    def search_activities(self, search_term):
        """Search activities in database"""
        try:
            return activity_db.search_activities(search_term)
        except Exception as e:
            print(f"Error searching activities: {e}")
            return False, str(e)

    def clear_all_activities(self):
        """Clear all activity logs"""
        try:
            return activity_db.clear_all_activities()
        except Exception as e:
            print(f"Error clearing activities: {e}")
            return False, str(e)

    def create_menu_item(self, name, description, category, price, image_url):
        """Create a new menu item"""
        try:
            return menu_db.create_menu_item(
                name=name,
                description=description,
                category=category,
                price=float(price) if '.' in price else int(price),
                image_url=image_url
            )
        except Exception as e:
            print(f"Error creating menu item: {e}")
            return False, str(e)

    def update_menu_item(self, item_id, name, description, category, price, image_url):
        """Update a menu item"""
        try:
            return menu_db.update_menu_item(
                item_id=item_id,
                name=name,
                description=description,
                category=category,
                price=float(price) if '.' in price else int(price),
                image_url=image_url
            )
        except Exception as e:
            print(f"Error updating menu item: {e}")
            return False, str(e)

    def delete_menu_item(self, item_id):
        """Delete a menu item"""
        try:
            return menu_db.delete_menu_item(item_id)
        except Exception as e:
            print(f"Error deleting menu item: {e}")
            return False, str(e)

    def create_customer(self, full_name, email, phone, address, password):
        """Create a new customer"""
        try:
            return customer_db.create_customer(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                password=password
            )
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False, str(e)

    def create_staff(self, staff_name, staff_email, staff_phone, staff_address, staff_password):
        """Create a new staff member"""
        try:
            return staff_db.create_staff(
                staff_name=staff_name,
                staff_email=staff_email,
                staff_phone=staff_phone,
                staff_address=staff_address,
                staff_password=staff_password
            )
        except Exception as e:
            print(f"Error creating staff: {e}")
            return False, str(e)

    def update_customer(self, customer_id, full_name, email, phone, address, password):
        """Update a customer"""
        try:
            return customer_db.update_customer(
                customer_id=customer_id,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                password=password
            )
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False, str(e)

    def update_staff(self, staff_id, staff_name, staff_email, staff_phone, staff_address, staff_password):
        """Update a staff member"""
        try:
            return staff_db.update_staff(
                staff_id=staff_id,
                staff_name=staff_name,
                staff_email=staff_email,
                staff_phone=staff_phone,
                staff_address=staff_address,
                staff_password=staff_password
            )
        except Exception as e:
            print(f"Error updating staff: {e}")
            return False, str(e)

    def delete_customer(self, customer_id):
        """Delete a customer"""
        try:
            return customer_db.delete_customer(customer_id)
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False, str(e)

    def delete_staff(self, staff_id):
        """Delete a staff member"""
        try:
            return staff_db.delete_staff(staff_id)
        except Exception as e:
            print(f"Error deleting staff: {e}")
            return False, str(e)

    def log_activity(self, action, details=""):
        """Log an activity"""
        try:
            activity_db.add_activity(
                staff_name=self.admin_name,
                staff_id=self.admin_id,
                action=action,
                details=details
            )
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False

    def parse_date_string(self, date_str):
        """Helper method to parse date strings in various formats"""
        try:
            if isinstance(date_str, datetime):
                return date_str
            elif isinstance(date_str, date):
                return datetime.combine(date_str, datetime.min.time())
            elif isinstance(date_str, str):
                # Clean the string
                cleaned_str = str(date_str).strip()

                # Try to split by space or T
                if ' ' in cleaned_str:
                    cleaned_str = cleaned_str.split(' ')[0]
                elif 'T' in cleaned_str:
                    cleaned_str = cleaned_str.split('T')[0]

                # Try different date formats - most common ones first
                date_formats = [
                    "%Y-%m-%d",  # 2023-12-31 (most common in databases)
                    "%d/%m/%Y",  # 31/12/2023
                    "%m/%d/%Y",  # 12/31/2023
                    "%d-%m-%Y",  # 31-12-2023
                    "%m-%d-%Y",  # 12-31-2023
                    "%Y.%m.%d",  # 2023.12.31
                    "%d.%m.%Y",  # 31.12.2023
                ]

                for date_format in date_formats:
                    try:
                        result = datetime.strptime(cleaned_str, date_format)
                        return result
                    except ValueError:
                        continue

                # If none of the standard formats work, try to extract date parts manually
                import re

                # Pattern for YYYY-MM-DD
                ymd_pattern = r'(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})'
                ymd_match = re.search(ymd_pattern, cleaned_str)
                if ymd_match:
                    year, month, day = ymd_match.groups()
                    try:
                        result = datetime(int(year), int(month), int(day))
                        return result
                    except ValueError:
                        pass

                # Pattern for DD-MM-YYYY or MM-DD-YYYY
                dmy_pattern = r'(\d{1,2})[-/\.](\d{1,2})[-/\.](\d{4})'
                dmy_match = re.search(dmy_pattern, cleaned_str)
                if dmy_match:
                    part1, part2, year = dmy_match.groups()
                    # Try both possibilities
                    try:
                        # Try DD-MM-YYYY first
                        result = datetime(int(year), int(part2), int(part1))
                        return result
                    except ValueError:
                        try:
                            # Try MM-DD-YYYY
                            result = datetime(int(year), int(part1), int(part2))
                            return result
                        except ValueError:
                            pass

                return None

            return None
        except Exception as e:
            print(f"Error parsing date string '{date_str}': {e}")
            return None