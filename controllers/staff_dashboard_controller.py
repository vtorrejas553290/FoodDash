"""
Staff Dashboard Controller
Coordinates between Model and View, handles business logic
"""
from PyQt6.QtCore import QObject, pyqtSignal
from models.staff_dashboard_model import StaffDashboardModel
from views.staff_dashboard_view import StaffDashboardView


class StaffDashboardController(QObject):
    """Controller for staff dashboard functionality"""

    # Signal emitted when logout is requested
    logout_requested = pyqtSignal()

    def __init__(self, staff_info):
        super().__init__()
        self.model = StaffDashboardModel(staff_info)
        self.view = StaffDashboardView()

        # Store data
        self.menu_items = []
        self.all_today_orders = []
        self.today_orders = []

        # Setup UI
        self._setup_ui()
        self._setup_connections()

        # Load initial data
        self.load_menu_items()

    def _setup_ui(self):
        """Setup the user interface"""
        # Set staff info in view
        self.view.set_staff_info(self.model.staff_name, self.model.staff_id)

        # Build and add pages
        menu_page = self.view.build_menu_page(self.menu_items)
        orders_page = self.view.build_orders_page()

        self.view.pages.addWidget(menu_page)
        self.view.pages.addWidget(orders_page)

        # Populate menu table
        self.view.populate_menu_table(self.menu_items)

    def _setup_connections(self):
        """Setup signal connections"""
        # View signals
        self.view.logout_requested.connect(self.handle_logout)
        self.view.page_switched.connect(self.handle_page_switch)
        self.view.add_item_clicked.connect(self.handle_add_item)
        self.view.edit_item_clicked.connect(self.handle_edit_item)
        self.view.delete_item_clicked.connect(self.handle_delete_item)
        self.view.search_orders_clicked.connect(self.handle_search_orders)
        self.view.filter_orders_changed.connect(self.handle_filter_orders)
        self.view.refresh_orders_clicked.connect(self.handle_refresh_orders)
        self.view.order_status_changed.connect(self.handle_order_status_change)

    def load_menu_items(self):
        """Load menu items from model"""
        self.menu_items = self.model.load_menu_items()
        self.view.populate_menu_table(self.menu_items)

    def handle_page_switch(self, index):
        """Handle page switching"""
        self.view.switch_page(index)
        if index == 1:  # Orders page
            self.load_orders()

    def handle_add_item(self):
        """Handle add item request"""
        item_data = self.view.show_add_item_dialog()
        if item_data:
            title = item_data['title']
            description = item_data['description']
            category = item_data['category']
            price = item_data['price']
            image = item_data['image']

            if title and price:
                success, message = self.model.add_menu_item(title, description, category, price, image)

                if success:
                    # Log the activity
                    self.model.log_activity(
                        "Added menu item",
                        f"{title} (₱{price}) - {category}"
                    )

                    # Reload menu items
                    self.load_menu_items()
                    self.view.show_message("Success", "Menu item added to database successfully!")
                else:
                    self.view.show_message("Error", f"Failed to add menu item: {message}")
            else:
                self.view.show_message("Error", "Title and price are required fields!")

    def handle_edit_item(self, row):
        """Handle edit item request"""
        if row < 0 or row >= len(self.menu_items):
            return

        item_data = self.menu_items[row]
        item_id = item_data.get('id')
        original_title = item_data["title"]
        original_price = item_data["price"].replace("₱", "") if "₱" in item_data["price"] else item_data["price"]

        updated_data = self.view.show_edit_item_dialog(item_data)
        if updated_data:
            title = updated_data['title']
            description = updated_data['description']
            category = updated_data['category']
            price = updated_data['price']
            image = updated_data['image']

            if title and price:
                success, message = self.model.update_menu_item(item_id, title, description, category, price, image)

                if success:
                    # Log the activity
                    log_details = []
                    if original_title != title:
                        log_details.append(f"Name: {original_title} → {title}")
                    if original_price != price:
                        log_details.append(f"Price: ₱{original_price} → ₱{price}")
                    if item_data["category"] != category:
                        log_details.append(f"Category: {item_data['category']} → {category}")

                    if log_details:
                        self.model.log_activity(
                            "Updated menu item",
                            f"{title}: " + ", ".join(log_details)
                        )

                    # Reload menu items
                    self.load_menu_items()
                    self.view.show_message("Success", "Menu item updated in database successfully!")
                else:
                    self.view.show_message("Error", f"Failed to update menu item: {message}")
            else:
                self.view.show_message("Error", "Title and price are required fields!")

    def handle_delete_item(self, row):
        """Handle delete item request"""
        if row < 0 or row >= len(self.menu_items):
            return

        item_data = self.menu_items[row]
        item_id = item_data.get('id')
        item_name = item_data["title"]

        confirmed = self.view.show_delete_confirmation(item_name)
        if confirmed:
            success, message = self.model.delete_menu_item(item_id, item_name)

            if success:
                # Log the activity
                self.model.log_activity(
                    "Deleted menu item",
                    f"{item_name}"
                )

                # Reload menu items
                self.load_menu_items()
                self.view.show_message("Success", f"'{item_name}' has been deleted from database.")
            else:
                self.view.show_message("Error", f"Failed to delete item: {message}")

    def load_orders(self):
        """Load orders from model"""
        self.all_today_orders = self.model.load_todays_orders()
        self.today_orders = self.all_today_orders.copy()
        self.view.display_orders(self.today_orders)

    def handle_search_orders(self):
        """Handle search orders request"""
        search_term = self.view.get_search_term()

        if not search_term:
            # If search is cleared, show current filtered orders
            self.view.display_orders(self.today_orders)
            return

        # Search within current filtered orders
        if self.today_orders:
            search_term_lower = search_term.lower()
            searched_orders = []

            for order in self.today_orders:
                order_number = str(order.get('order_number', '')).lower()
                customer_name = str(order.get('customer_name', '')).lower()
                customer_email = str(order.get('customer_email', '')).lower()

                if (search_term_lower in order_number or
                        search_term_lower in customer_name or
                        search_term_lower in customer_email):
                    searched_orders.append(order)

            self.view.display_orders(searched_orders)

    def handle_filter_orders(self, status):
        """Handle filter orders request"""
        # Always use the complete list of today's orders as the source
        if not self.all_today_orders:
            self.load_orders()
            return

        if status == "All Status":
            # Show all today's orders
            self.today_orders = self.all_today_orders.copy()
        else:
            # Filter today's orders by status
            filtered_orders = []
            for order in self.all_today_orders:
                order_status = order.get('status', '')
                if isinstance(order_status, str):
                    if order_status.lower() == status.lower():
                        filtered_orders.append(order)

            self.today_orders = filtered_orders

        # Display the filtered results
        self.view.display_orders(self.today_orders)

    def handle_refresh_orders(self):
        """Handle refresh orders request"""
        self.load_orders()

    def handle_order_status_change(self, order_id, new_status):
        """Handle order status change"""
        success, result = self.model.update_order_status(order_id, new_status)

        if success:
            # Log the activity
            order = self.model.get_order_by_id(order_id)
            order_number = order.get('order_number', 'Unknown') if order else "Unknown"

            self.model.log_activity(
                f"Updated order status",
                f"Order #{order_number}: {new_status}"
            )

            # Reload orders to reflect changes
            self.load_orders()

            # Show success message
            self.view.show_message("Success", f"Order status updated to {new_status}")
        else:
            # Show error message
            self.view.show_message("Error", f"Failed to update status: {result}")

    def handle_logout(self):
        """Handle logout request"""
        confirmed = self.view.show_logout_confirmation()
        if confirmed:
            # Log logout activity
            self.model.log_activity("Staff logged out")
            self.logout_requested.emit()

    def get_view(self):
        """Get the view component"""
        return self.view