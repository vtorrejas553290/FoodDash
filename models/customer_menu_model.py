"""
Customer Menu Model
"""

from datetime import datetime
import os
import re
from db.menu_db import menu_db
from db.orders_db import orders_db_instance as orders_db
from db.customer_db import customer_db


class CustomerMenuModel:
    def __init__(self):
        self.cart_items = []
        self.orders_items = []
        self.menu_items = []
        self.current_category = "All"

    def set_customer_info(self, customer_info):
        self.customer_info = customer_info

    def load_menu_items_from_db(self):
        try:
            menu_items_data = menu_db.get_all_menu_items()
            self.menu_items = []
            for item in menu_items_data:
                self.menu_items.append({
                    "img": item['image_url'],
                    "title": item['name'],
                    "subtitle": item['description'],
                    "price": f"₱{item['price']}",
                    "category": self.standardize_category(item['category'])
                })

            if not self.menu_items:
                self.menu_items = self.get_fallback_menu_items()
            return self.menu_items
        except Exception as e:
            print(f"Error loading menu items: {e}")
            self.menu_items = self.get_fallback_menu_items()
            return self.menu_items

    def standardize_category(self, db_category):
        """Standardize category names - identical to original"""
        if not db_category:
            return "Other"

        category_lower = db_category.lower()
        if "burger" in category_lower:
            return "Burger"
        elif "side" in category_lower:
            return "Sides"
        elif "chicken" in category_lower:
            return "Chicken"
        elif "pizza" in category_lower:
            return "Pizza"
        elif "drink" in category_lower:
            return "Drinks"
        else:
            return db_category.capitalize()

    def get_fallback_menu_items(self):
        """Get fallback menu items if database fails - identical to original"""
        return [
            {
                "img": "picture/burger.png",
                "title": "Classic Burger",
                "subtitle": "Juicy beef patty with fresh veggies",
                "price": "₱159",
                "category": "Burger"
            },
            {
                "img": "picture/fries.png",
                "title": "Crispy Fries",
                "subtitle": "Golden crispy potato fries",
                "price": "₱79",
                "category": "Sides"
            },
            {
                "img": "picture/chicken.png",
                "title": "Fried Chicken",
                "subtitle": "Crispy fried chicken pieces",
                "price": "₱189",
                "category": "Chicken"
            },
            {
                "img": "picture/milktea.png",
                "title": "Milk Tea",
                "subtitle": "Classic milk tea with pearls",
                "price": "₱99",
                "category": "Drinks"
            },
            {
                "img": "picture/pizza.png",
                "title": "Pepperoni Pizza",
                "subtitle": "Loaded with pepperoni slices",
                "price": "₱349",
                "category": "Pizza"
            },
        ]

    def filter_items_by_category(self, category):
        self.current_category = category
        if category == "All":
            return self.menu_items
        else:
            return [item for item in self.menu_items if item["category"] == category]

    def add_to_cart(self, title, price, img, cart_items):
        """Add item to cart - matching original logic"""
        for item in cart_items:
            if item['title'] == title:
                item['qty'] += 1
                return True, cart_items

        cart_items.append({'title': title, 'price': price, 'img': img, 'qty': 1})
        return True, cart_items

    def change_cart_quantity(self, index, delta, cart_items):
        """Change cart item quantity"""
        if 0 <= index < len(cart_items):
            cart_items[index]['qty'] += delta
            if cart_items[index]['qty'] <= 0:
                del cart_items[index]
            return True, cart_items
        return False, cart_items

    def delete_cart_item(self, index, cart_items):
        """Delete item from cart"""
        if 0 <= index < len(cart_items):
            del cart_items[index]
            return True, cart_items
        return False, cart_items

    def calculate_cart_total(self, cart_items):
        """Calculate cart total"""
        total = 0
        for item in cart_items:
            price_val = self.extract_price(item['price']) * item.get('qty', 1)
            total += price_val
        return total

    def extract_price(self, price_str):
        """Extract numeric price from string - FIXED to match original"""
        try:
            # Debug print
            print(f"DEBUG extract_price: Input: '{price_str}'")

            # Remove any currency symbols and whitespace
            clean_str = str(price_str).replace("₱", "").replace("P", "").strip()

            # Remove any non-digit characters except decimal point
            clean_str = re.sub(r'[^\d.]', '', clean_str)

            # If empty after cleaning, return 0
            if not clean_str:
                return 0.0

            result = float(clean_str)
            print(f"DEBUG extract_price: Result: {result}")
            return result
        except Exception as e:
            print(f"DEBUG extract_price: Error parsing '{price_str}': {e}")
            return 0.0

    def place_order(self, cart_items, customer_info):
        """Place order in database - FIXED to match original"""
        if not cart_items or not customer_info or 'id' not in customer_info:
            return False, "Cart is empty or customer info missing"

        # Calculate total amount from cart items - IMPORTANT: Calculate here first
        total_amount = 0
        for item in cart_items:
            price_val = self.extract_price(item['price']) * item.get('qty', 1)
            total_amount += price_val
            print(f"DEBUG place_order: {item['title']} - {item['price']} x {item.get('qty', 1)} = {price_val}")

        print(f"DEBUG place_order: Total amount calculated: {total_amount}")

        success, result = orders_db.create_order(
            customer_id=customer_info['id'],
            customer_info=customer_info,
            cart_items=cart_items.copy(),
            subtotal=total_amount
        )

        if success:
            order_data = {
                'order_id': result['order_id'],
                'order_number': result['order_number'],
                'items': cart_items.copy(),
                'date': datetime.now().strftime("%m/%d/%Y • %I:%M %p"),
                'total': total_amount,
                'db_id': result['order_id']
            }

            # Save receipt to file
            receipt_file = self.save_receipt_to_file(order_data, cart_items, customer_info)

            return True, {
                "order_data": order_data,
                "receipt_file": receipt_file,
                "total": total_amount,
                "order_number": result['order_number']
            }
        else:
            return False, result

    def save_receipt_to_file(self, order_data, cart_items, customer_info):
        """Save receipt to file"""
        try:
            receipts_dir = "receipts"
            if not os.path.exists(receipts_dir):
                os.makedirs(receipts_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipts/order_{order_data['order_number']}_{timestamp}.txt"

            receipt_content = self.generate_receipt_content(order_data, cart_items, customer_info)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(receipt_content)

            return filename
        except Exception as e:
            print(f"ERROR: Failed to save receipt: {str(e)}")
            return None

    def generate_receipt_content(self, order_data, cart_items, customer_info):
        """Generate receipt content"""
        receipt_content = f"""
            =================================
                    FOOD DASH RECEIPT
            =================================

            Order Number: #{order_data['order_number']}
            Order ID: {order_data['order_id']}
            Date: {datetime.now().strftime("%m/%d/%Y • %I:%M %p")}

            ---------------------------------
            CUSTOMER INFORMATION
            ---------------------------------
            Name: {customer_info.get('full_name', 'N/A')}
            Email: {customer_info.get('email', 'N/A')}
            Address: {customer_info.get('address', 'N/A')}

            ---------------------------------
            ORDER DETAILS
            ---------------------------------
            """

        for item in cart_items:
            price_val = self.extract_price(item['price'])
            total_item_price = price_val * item.get('qty', 1)
            receipt_content += f"{item['title']} x{item.get('qty', 1)}"
            receipt_content += f"\n   {item['price']} each = ₱{total_item_price:.2f}\n"

        receipt_content += f"""
            ---------------------------------
            ORDER SUMMARY
            ---------------------------------
            Subtotal:      ₱{order_data['total']:.2f}
            Delivery Fee:  ₱50.00
            Total:         ₱{order_data['total'] + 50:.2f}

            ---------------------------------
            ORDER STATUS
            ---------------------------------
            Status: Pending
            Estimated Delivery: 30-45 minutes

            =================================
            Thank you for ordering with Food Dash!
            =================================
            """

        return receipt_content

    def load_orders_from_db(self, customer_info):
        """Load customer orders from database"""
        if not customer_info or 'id' not in customer_info:
            return False, "Customer info missing"

        try:
            success, orders = orders_db.get_customer_orders(customer_info['id'])
            return success, orders
        except Exception as e:
            print(f"Error loading orders: {e}")
            return False, str(e)

    def update_customer_profile(self, customer_info, field, value, current_password=""):
        """Update customer profile"""
        if not customer_info or 'id' not in customer_info:
            return False, "Customer info missing"

        try:
            if field == 'password':
                # Verify current password first
                success, auth_customer = customer_db.authenticate_customer(
                    customer_info['email'],
                    current_password
                )

                if not success:
                    return False, "Current password is incorrect"

                # Update password
                success, message = customer_db.update_customer(
                    customer_info['id'],
                    customer_info.get('full_name', ''),
                    customer_info.get('email', ''),
                    customer_info.get('phone', ''),
                    customer_info.get('address', ''),
                    value  # New password
                )
            else:
                # Update other fields
                update_data = {
                    'full_name': customer_info.get('full_name', ''),
                    'email': customer_info.get('email', ''),
                    'phone': customer_info.get('phone', ''),
                    'address': customer_info.get('address', '')
                }

                if field == 'name':
                    update_data['full_name'] = value
                elif field == 'email':
                    update_data['email'] = value
                elif field == 'phone':
                    update_data['phone'] = value
                elif field == 'address':
                    update_data['address'] = value

                success, message = customer_db.update_customer(
                    customer_info['id'],
                    update_data['full_name'],
                    update_data['email'],
                    update_data['phone'],
                    update_data['address']
                )

            if success and field != 'password':
                # Update the specific field in customer info
                if field == 'name':
                    customer_info['full_name'] = value
                elif field == 'email':
                    customer_info['email'] = value
                elif field == 'phone':
                    customer_info['phone'] = value
                elif field == 'address':
                    customer_info['address'] = value

            return success, message
        except Exception as e:
            return False, str(e)

    def format_database_date(self, date_str):
        """Format database date string"""
        if not date_str:
            return "Date not available"

        try:
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{2}/\d{2}/\d{4})',
            ]

            for pattern in date_patterns:
                match = re.search(pattern, str(date_str))
                if match:
                    date_part = match.group(1)
                    time_formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-dT%H:%M:%S',
                        '%Y-%m-%d',
                        '%m/%d/%Y'
                    ]

                    for time_format in time_formats:
                        try:
                            date_obj = datetime.strptime(date_part, time_format)
                            formatted_date = date_obj.strftime("%m/%d/%Y • %I:%M %p")
                            return formatted_date
                        except ValueError:
                            continue

            if isinstance(date_str, str):
                clean_str = date_str.split('.')[0]
                clean_str = clean_str.replace('T', ' ')
                return clean_str[:19]

            return "Date not available"
        except Exception as e:
            print(f"Error formatting date '{date_str}': {e}")
            return "Date not available"