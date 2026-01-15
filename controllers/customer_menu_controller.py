"""
Customer Menu Controller
Coordinates between Model and View for customer dashboard
"""
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from typing import Dict, List, Optional
from models.customer_menu_model import CustomerMenuModel
from views.customer_menu_view import CustomerMenuView
from db.orders_db import orders_db_instance as orders_db
import os
from datetime import datetime


class CustomerMenuController(QObject):
    """Controller for customer menu dashboard"""

    # Signals
    logout_requested = pyqtSignal()
    profile_updated = pyqtSignal(dict)  # Signal when profile is updated

    def __init__(self, customer_info: Dict):
        super().__init__()
        self.customer_info = customer_info
        self.cart_items = []  # Store cart items in controller

        # Initialize view first (as in original code)
        self.view = CustomerMenuView(customer_info)

        # Initialize model
        self.model = CustomerMenuModel()
        self.model.set_customer_info(customer_info)

        # Connect signals
        self._connect_signals()

        # Load menu items (matching original flow)
        self._load_menu_items()

        # Update customer info in view
        self.view.update_customer_info(customer_info)

    def _connect_signals(self):
        """Connect view signals to controller methods"""
        # Logout signals
        self.view.logout_requested.connect(self.logout_requested.emit)

        # Add to cart signal
        self.view.add_to_cart_requested.connect(self._handle_add_to_cart)

        # Category filter signal
        self.view.filter_category_signal.connect(self._handle_filter_category)

        # Cart operations - CONNECT THESE SIGNALS
        self.view.cart_page.quantity_changed.connect(self._handle_quantity_change)
        self.view.cart_page.item_deleted.connect(self._handle_item_delete)
        self.view.cart_page.checkout_btn.clicked.connect(self._handle_checkout)

        # Profile edit signals
        self.view.profile_edit_requested.connect(self._handle_profile_edit)

        # Page navigation
        self.view.bottomnav.page_changed.connect(self._handle_page_change)

    def _load_menu_items(self):
        """Load menu items from database - matching original code"""
        menu_items = self.model.load_menu_items_from_db()
        self.view.menu_items = menu_items

        # Get unique categories for filter
        categories = ["All", "Burger", "Sides", "Chicken", "Pizza", "Drinks"]

        # Display in view
        self.view.display_menu_items(menu_items, categories)

    def _handle_page_change(self, page_name: str):
        """Handle page navigation - matching original"""
        print(f"DEBUG: Page changed to: {page_name}")

        if page_name == "Orders":
            print(f"DEBUG: Loading orders for customer ID: {self.customer_info.get('id')}")
            self._load_orders()
        elif page_name == "Cart":
            # Update cart display with controller's cart items
            self.view.cart_page.cart_items = self.cart_items
            self.view.cart_page.update_cart()
        elif page_name == "Profile":
            # Load profile (already loaded in init)
            pass

        self.view.switch_page(page_name)

    def _handle_add_to_cart(self, title: str, price: str, img: str):
        """Handle add to cart request - matching original"""
        success, updated_cart = self.model.add_to_cart(title, price, img, self.cart_items)
        if success:
            self.cart_items = updated_cart
            self.view.cart_page.cart_items = self.cart_items
            self.view.cart_page.update_cart()

            # Show message (matching original style)
            msg = QMessageBox()
            msg.setWindowTitle("Added to Cart")
            msg.setText(f"{title} added to cart!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    color: white;
                    background-color: #2ea1ff;
                    border: 1px solid #2ea1ff;
                    padding: 5px 15px;
                    border-radius: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1e90ff;
                }
            """)
            msg.exec()

    def _handle_quantity_change(self, index: int, delta: int):
        """Handle cart quantity change"""
        print(f"DEBUG: Changing quantity for index {index} by {delta}")
        success, updated_cart = self.model.change_cart_quantity(index, delta, self.cart_items)
        if success:
            self.cart_items = updated_cart
            self.view.cart_page.cart_items = self.cart_items
            self.view.cart_page.update_cart()

    def _handle_item_delete(self, index: int):
        """Handle item deletion from cart"""
        print(f"DEBUG: Deleting item at index {index}")
        success, updated_cart = self.model.delete_cart_item(index, self.cart_items)
        if success:
            self.cart_items = updated_cart
            self.view.cart_page.cart_items = self.cart_items
            self.view.cart_page.update_cart()

    def _handle_checkout(self):
        """Handle checkout process - FIXED to show placed order"""
        print(f"DEBUG: Checkout initiated")
        print(f"DEBUG: Cart items: {len(self.cart_items)}")

        if not self.cart_items:
            # Create styled message box for cart empty (matching original)
            msg = QMessageBox()
            msg.setWindowTitle("Cart Empty")
            msg.setText("Your cart is empty!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
                QPushButton {
                    color: white;
                    background-color: #2ea1ff;
                    border: 1px solid #2ea1ff;
                    padding: 5px 15px;
                    border-radius: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1e90ff;
                }
            """)
            msg.exec()
            return

        # Calculate total amount
        total_amount = self.model.calculate_cart_total(self.cart_items)
        print(f"DEBUG: Total amount: ₱{total_amount}")

        # Create styled confirmation dialog with black text (matching original)
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Order")
        msg.setText(f"Do you want to place this order totaling ₱{total_amount}?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Style the OK button specifically
        ok_button = msg.button(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #2ea1ff;
                border: 1px solid #2ea1ff;
            }
            QPushButton:hover {
                background-color: #1e90ff;
            }
        """)

        # Style the Cancel button
        cancel_button = msg.button(QMessageBox.StandardButton.Cancel)
        cancel_button.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        if msg.exec() == QMessageBox.StandardButton.Ok:
            try:
                print(f"DEBUG: Placing order for customer: {self.customer_info.get('id')}")

                # DIRECT DATABASE CALL like original code
                if self.customer_info and 'id' in self.customer_info:
                    success, result = orders_db.create_order(
                        customer_id=self.customer_info['id'],
                        customer_info=self.customer_info,
                        cart_items=self.cart_items.copy(),
                        subtotal=total_amount
                    )

                    if success:
                        print(f"DEBUG: Order placed successfully: {result}")

                        # Create order data exactly like original
                        order_data = {
                            'order_id': result['order_id'],
                            'order_number': result['order_number'],
                            'items': self.cart_items.copy(),
                            'date': datetime.now().strftime("%m/%d/%Y • %I:%M %p"),
                            'total': total_amount,
                            'db_id': result['order_id'],
                            'subtotal': total_amount,
                            'delivery_fee': 50.0,
                            'total_amount': total_amount + 50.0,
                            'status': 'pending',
                            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        # Add to orders items
                        self.view.orders_items.append(order_data)

                        # Clear cart
                        self.cart_items.clear()
                        self.view.cart_page.cart_items = self.cart_items
                        self.view.cart_page.update_cart()

                        # Navigate to orders page
                        self.view.switch_page("Orders")

                        # MANUALLY ADD THE NEW ORDER TO THE ORDERS PAGE
                        # Clear the orders list first
                        self.view.orders_page.orders_list.clear()

                        # Add the new order first
                        self.view.orders_page.add_order_card(order_data)

                        # Then load all other orders from database
                        self._load_all_orders_with_new_one(order_data)

                        # Create styled success message box with receipt info
                        success_msg = QMessageBox()
                        success_msg.setWindowTitle("Order Placed")

                        # Save receipt to file
                        receipt_file = self.model.save_receipt_to_file(order_data, self.cart_items, self.customer_info)

                        if receipt_file:
                            success_msg.setText(
                                f"Order #{result['order_number']} placed successfully!\n"
                                f"Total: ₱{total_amount}\n"
                                f"Receipt saved to: {receipt_file}"
                            )
                        else:
                            success_msg.setText(
                                f"Order #{result['order_number']} placed successfully!\n"
                                f"Total: ₱{total_amount}"
                            )

                        success_msg.setIcon(QMessageBox.Icon.Information)
                        success_msg.setStyleSheet("""
                            QMessageBox {
                                background-color: white;
                            }
                            QLabel {
                                color: black;
                                font-size: 14px;
                            }
                            QPushButton {
                                color: white;
                                background-color: #2ea1ff;
                                border: 1px solid #2ea1ff;
                                padding: 5px 15px;
                                border-radius: 5px;
                                min-width: 80px;
                            }
                            QPushButton:hover {
                                background-color: #1e90ff;
                            }
                        """)

                        success_msg.exec()
                    else:
                        # Create styled warning message box
                        warning_msg = QMessageBox()
                        warning_msg.setWindowTitle("Order Failed")
                        warning_msg.setText(f"Failed to save order: {result}")
                        warning_msg.setIcon(QMessageBox.Icon.Warning)
                        warning_msg.setStyleSheet("""
                            QMessageBox {
                                background-color: white;
                            }
                            QLabel {
                                color: black;
                                font-size: 14px;
                            }
                            QPushButton {
                                color: white;
                                background-color: #2ea1ff;
                                border: 1px solid #2ea1ff;
                                padding: 5px 15px;
                                border-radius: 5px;
                                min-width: 80px;
                            }
                            QPushButton:hover {
                                background-color: #1e90ff;
                            }
                        """)
                        warning_msg.exec()
                else:
                    # Create styled warning message box
                    warning_msg = QMessageBox()
                    warning_msg.setWindowTitle("Error")
                    warning_msg.setText("Customer information not available.")
                    warning_msg.setIcon(QMessageBox.Icon.Warning)
                    warning_msg.setStyleSheet("""
                        QMessageBox {
                            background-color: white;
                        }
                        QLabel {
                            color: black;
                            font-size: 14px;
                        }
                        QPushButton {
                            color: white;
                            background-color: #2ea1ff;
                            border: 1px solid #2ea1ff;
                            padding: 5px 15px;
                            border-radius: 5px;
                            min-width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #1e90ff;
                        }
                    """)
                    warning_msg.exec()

            except Exception as e:
                # Create styled error message box
                error_msg = QMessageBox()
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Failed to place order: {str(e)}")
                error_msg.setIcon(QMessageBox.Icon.Critical)
                error_msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QLabel {
                        color: black;
                        font-size: 14px;
                    }
                    QPushButton {
                        color: white;
                        background-color: #2ea1ff;
                        border: 1px solid #2ea1ff;
                        padding: 5px 15px;
                        border-radius: 5px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #1e90ff;
                    }
                """)
                error_msg.exec()

    def _load_all_orders_with_new_one(self, new_order):
        """Load all orders from database including the new one"""
        print(f"DEBUG: Loading all orders with new one")

        # Clear existing orders
        self.view.orders_page.orders_list.clear()

        # First add the new order (most recent)
        self.view.orders_page.add_order_card(new_order)

        # Then load and add other orders from database
        success, orders = self.model.load_orders_from_db(self.customer_info)

        if success and orders:
            print(f"DEBUG: Loaded {len(orders)} orders from database")

            # Add each order except the one we just added
            for order in orders:
                # Skip if this is the same order we just added
                if 'order_number' in order and order.get('order_number') == new_order.get('order_number'):
                    continue

                # Format date before displaying
                if 'created_at' in order:
                    order['formatted_date'] = self.model.format_database_date(order.get('created_at', ''))
                else:
                    order['formatted_date'] = new_order.get('date', 'Date not available')

                # Make sure order has required fields
                if 'items' not in order:
                    order['items'] = []

                self.view.orders_page.add_order_card(order)
        else:
            print(f"DEBUG: No other orders found or error loading: {orders}")

    def _load_orders(self):
        """Load customer orders - FIXED to work properly"""
        print(f"DEBUG: Loading orders for customer ID: {self.customer_info.get('id')}")

        # Clear existing orders first
        self.view.orders_page.orders_list.clear()

        success, orders = self.model.load_orders_from_db(self.customer_info)
        print(f"DEBUG: Load orders success: {success}")
        print(f"DEBUG: Orders returned: {len(orders) if orders else 0}")

        if success and orders:
            for order in orders:
                print(f"DEBUG: Processing order: {order.get('order_number', 'No order number')}")

                # Format date before displaying
                order['formatted_date'] = self.model.format_database_date(order.get('created_at', ''))

                # Make sure order has required fields
                if 'items' not in order:
                    order['items'] = []

                self.view.orders_page.add_order_card(order)
        else:
            print(f"DEBUG: Showing no orders message")
            self.view.orders_page.show_no_orders("No orders yet" if success else "Error loading orders")

    def _handle_filter_category(self, category: str):
        """Handle category filter"""
        filtered_items = self.model.filter_items_by_category(category)
        self.view.display_menu_items(filtered_items)
        self.view.update_category_buttons(category)

    def _handle_profile_edit(self, field: str, new_value: str, current_password: str = ""):
        """Handle profile edit requests - identical to your working version"""
        success, message = self.model.update_customer_profile(
            self.customer_info,
            field,
            new_value,
            current_password
        )

        if success:
            # Update local customer info (except password)
            if field != 'password':
                if field == 'name':
                    self.customer_info['full_name'] = new_value
                elif field == 'email':
                    self.customer_info['email'] = new_value
                elif field == 'phone':
                    self.customer_info['phone'] = new_value
                elif field == 'address':
                    self.customer_info['address'] = new_value

            # Update UI in the view
            self.view.update_customer_info(self.customer_info)
            self.view.profile_page.show_message("Success", message)
            self.profile_updated.emit(self.customer_info)
        else:
            self.view.profile_page.show_message("Update Failed", message, QMessageBox.Icon.Warning)

    def get_view(self) -> CustomerMenuView:
        """Get the view component"""
        return self.view

    def update_customer_info(self, customer_info: Dict):
        """Update customer information"""
        self.customer_info = customer_info
        self.model.set_customer_info(customer_info)
        self.view.update_customer_info(customer_info)

    def show(self):
        """Show the view"""
        self.view.show()