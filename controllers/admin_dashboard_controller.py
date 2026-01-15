# admin_dashboard_controller.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView,
    QScrollArea, QStackedWidget, QMessageBox, QInputDialog, QFileDialog,
    QDialog, QLineEdit, QTextEdit, QComboBox, QDialogButtonBox
)
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QDialog
import sys
from datetime import date, datetime, timedelta
import os

from models.admin_dashboard_model import AdminDashboardModel
from views.admin_dashboard_view import AdminDashboardView
from .widgets import AddUserDialog, EditUserDialog

# Import ReportLab for PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import tempfile


class AdminDashboardController(QObject):
    """Controller for Admin Dashboard - Handles all business logic"""

    logout_requested = pyqtSignal()

    def __init__(self, admin_info=None):
        super().__init__()

        # Initialize model and view
        self.model = AdminDashboardModel(admin_info)
        self.view = AdminDashboardView()

        # Set admin info in view
        self.view.set_admin_info(self.model.admin_name, self.model.admin_id)

        # Build pages
        self.build_pages()

        # Connect signals
        self.setup_connections()

        # Create activity logs table if it doesn't exist
        from db.activity_db import activity_db
        activity_db.create_table()

        # Add initial activity log for admin login
        self.model.log_activity("Admin logged in")

    def get_view(self):
        """Return the view widget"""
        return self.view

    def build_pages(self):
        """Build all pages for the dashboard"""
        # Build overview page
        total_revenue = self.model.get_total_revenue_from_db()
        today_orders = self.model.get_todays_orders_count()
        pending_orders = self.model.get_pending_orders_count()
        user_count = len([u for u in self.model.all_users if u['role'].lower() != 'admin'])

        overview_page = self.view.build_overview_page(
            user_count, total_revenue, today_orders, pending_orders
        )
        self.view.pages.addWidget(overview_page)

        # Build other pages
        self.view.pages.addWidget(self.view.build_orders_page())
        self.view.pages.addWidget(self.view.build_menu_page())
        self.view.pages.addWidget(self.view.build_user_management_page())
        self.view.pages.addWidget(self.view.build_activity_logs_page())

        # Populate initial data
        self.populate_menu_table()
        self.populate_user_table()
        self.refresh_activity_logs()

    def setup_connections(self):
        """Setup all signal-slot connections"""
        # Tab buttons
        self.view.overview_btn.clicked.connect(lambda: self.switch_page(0))
        self.view.order_btn.clicked.connect(lambda: self.switch_page(1))
        self.view.menu_btn.clicked.connect(lambda: self.switch_page(2))
        self.view.user_btn.clicked.connect(lambda: self.switch_page(3))
        self.view.activity_btn.clicked.connect(lambda: self.switch_page(4))

        # Overview page - Connect refresh button directly
        if hasattr(self.view, 'refresh_btn'):
            self.view.refresh_btn.clicked.connect(self.refresh_dashboard)

        # Add PDF export button connection
        if hasattr(self.view, 'pdf_export_btn'):
            self.view.pdf_export_btn.clicked.connect(self.export_overview_to_pdf)

        # Order tracking page
        # Get buttons from view directly since they're now stored as attributes
        if hasattr(self.view, 'order_search_btn'):
            self.view.order_search_btn.clicked.connect(self.search_orders)
        if hasattr(self.view, 'order_today_btn'):
            self.view.order_today_btn.clicked.connect(self.show_todays_orders)
        if hasattr(self.view, 'order_refresh_btn'):
            self.view.order_refresh_btn.clicked.connect(self.load_orders_from_db)

        self.view.filter_combo.currentTextChanged.connect(self.filter_orders_by_status)
        self.view.month_filter_combo.currentTextChanged.connect(self.filter_orders_by_month)

        # Menu management page
        if hasattr(self.view, 'menu_add_btn'):
            self.view.menu_add_btn.clicked.connect(self.add_new_item)

        # User management page
        if hasattr(self.view, 'user_add_btn'):
            self.view.user_add_btn.clicked.connect(self.add_new_user)
        if hasattr(self.view, 'user_search_btn'):
            self.view.user_search_btn.clicked.connect(self.search_users)
        if hasattr(self.view, 'user_refresh_btn'):
            self.view.user_refresh_btn.clicked.connect(self.refresh_users)

        self.view.user_filter_combo.currentTextChanged.connect(self.filter_users_by_role)

        # Activity logs page
        if hasattr(self.view, 'activity_search_btn'):
            self.view.activity_search_btn.clicked.connect(self.search_activities)
        if hasattr(self.view, 'activity_today_btn'):
            self.view.activity_today_btn.clicked.connect(self.show_todays_activities)
        if hasattr(self.view, 'activity_clear_btn'):
            self.view.activity_clear_btn.clicked.connect(self.clear_activity_logs)
        if hasattr(self.view, 'activity_refresh_btn'):
            self.view.activity_refresh_btn.clicked.connect(self.refresh_activity_logs)

        self.view.period_filter_combo.currentTextChanged.connect(self.filter_activities_by_period)

        # Logout button
        self.view.logout_btn.clicked.connect(self.handle_logout)

        # Connect logout signal
        self.view.logout_requested.connect(self.logout_requested.emit)

    def switch_page(self, index):
        """Switch between different pages"""
        self.view.switch_page(index)

        # Refresh data when switching to specific pages
        if index == 0:  # Overview
            self.model.load_users_from_db()
            if hasattr(self.view, 'refresh_btn'):
                self.view.refresh_btn.setEnabled(True)
        elif index == 1:  # Order Tracking
            self.load_orders_from_db()
        elif index == 2:  # Menu Management
            pass  # Menu data is already loaded
        elif index == 3:  # User Management
            self.refresh_users()
        elif index == 4:  # Activity Logs
            self.refresh_activity_logs()

    def refresh_dashboard(self):
        """Refresh all dashboard data from database"""
        print("=== REFRESHING DASHBOARD ===")

        try:
            # Disable button during refresh
            if hasattr(self.view, 'refresh_btn'):
                self.view.refresh_btn.setEnabled(False)
                self.view.refresh_btn.setText("Refreshing...")

            # Force UI update
            QApplication.processEvents()

            # 1. Load fresh user data
            print("Loading users...")
            self.model.load_users_from_db()

            # 2. Load fresh analytics stats
            print("Loading analytics data...")
            self.model.load_analytics_data()

            # 3. Get updated values
            print("Calculating updated values...")
            total_revenue = self.model.get_total_revenue_from_db()
            today_orders = self.model.get_todays_orders_count()
            pending_orders = self.model.get_pending_orders_count()
            user_count = len([u for u in self.model.all_users if u['role'].lower() != 'admin'])

            print(
                f"Updated Data: Revenue={total_revenue}, Today={today_orders}, Pending={pending_orders}, Users={user_count}")

            # 4. Update stored values
            self.model.current_revenue = total_revenue
            self.model.active_user_count = user_count

            # 5. Update the cards directly
            print("Updating cards...")
            if hasattr(self.view, 'total_revenue_card'):
                self.view.total_revenue_card.update_value(f"₱{total_revenue:,.2f}")

            if hasattr(self.view, 'todays_orders_card'):
                self.view.todays_orders_card.update_value(f"{today_orders}")

            if hasattr(self.view, 'pending_orders_card'):
                self.view.pending_orders_card.update_value(f"{pending_orders}")

            if hasattr(self.view, 'active_users_card'):
                self.view.active_users_card.update_value(f"{user_count}")

            # 6. Update the line graph
            print("Updating line graph...")
            if hasattr(self.view, 'revenue_graph'):
                self.view.revenue_graph.update_monthly_data_from_db()

            # 7. Update the pie chart
            print("Updating pie chart...")
            if hasattr(self.view, 'pie_chart_widget'):
                self.view.pie_chart_widget.refresh()

            # 8. Update button state
            if hasattr(self.view, 'refresh_btn'):
                self.view.refresh_btn.setText("Refresh Dashboard")
                self.view.refresh_btn.setEnabled(True)

            print("=== REFRESH COMPLETE ===")

            # Show success message
            self.view.show_message("Dashboard Refreshed",
                                   f"Dashboard data has been updated:\n"
                                   f"• Total Revenue: ₱{total_revenue:,.2f}\n"
                                   f"• Today's Orders: {today_orders}\n"
                                   f"• Pending Orders: {pending_orders}\n"
                                   f"• Active Users: {user_count}")

        except Exception as e:
            print(f"!!! ERROR REFRESHING DASHBOARD: {e}")
            import traceback
            traceback.print_exc()

            # Reset button on error
            if hasattr(self.view, 'refresh_btn'):
                self.view.refresh_btn.setText("Refresh Dashboard")
                self.view.refresh_btn.setEnabled(True)

            self.view.show_message("Refresh Error",
                                   f"Failed to refresh dashboard:\n{str(e)}",
                                   QMessageBox.Icon.Warning)

    def load_orders_from_db(self):
        """Load orders from database"""
        try:
            orders = self.model.get_all_orders()

            if not orders:
                # Clear current orders
                self.view.clear_orders_layout()

                # Show no orders message
                btn = self.view.show_no_orders_message("No orders found")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
                return

            # Clear current orders
            self.view.clear_orders_layout()

            # Add order cards
            for order in orders:
                card = self.view.build_order_card(order, self.update_order_status)
                card.order_id = str(order.get('id', ''))  # Store order ID for tracking
                self.view.orders_layout.addWidget(card)

            # Add stretch at the end
            self.view.orders_layout.addStretch()

        except Exception as e:
            print(f"Error loading orders: {e}")
            # Clear layout and show error
            self.view.clear_orders_layout()

            error_label = QLabel(f"Error loading orders: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view.orders_layout.addWidget(error_label)

    def update_order_status(self, order_id, new_status):
        """Update order status in database"""
        success, result = self.model.update_order_status(order_id, new_status)

        if success:
            # Log the activity
            order_number = ""
            orders = self.model.get_all_orders()
            for order in orders:
                if order.get('id') == order_id:
                    order_number = order.get('order_number', 'Unknown')
                    break

            self.model.log_activity(
                f"Updated order status",
                f"Order #{order_number}: {new_status}"
            )

            # Reload orders to reflect changes
            self.load_orders_from_db()

            # Show success message
            self.view.show_message("Success", f"Order status updated to {new_status}")
        else:
            # Show error message
            self.view.show_message("Error", f"Failed to update status: {result}", QMessageBox.Icon.Warning)

    def search_orders(self):
        """Search orders based on search term"""
        search_term = self.view.search_input.text().strip()

        if not search_term:
            self.load_orders_from_db()
            return

        orders = self.model.search_orders(search_term)

        if orders:
            self.view.clear_orders_layout()
            for order in orders:
                card = self.view.build_order_card(order, self.update_order_status)
                self.view.orders_layout.addWidget(card)
            self.view.orders_layout.addStretch()
        else:
            btn = self.view.show_no_orders_message(f"No orders found for '{search_term}'")
            if btn:
                btn.clicked.connect(self.clear_filters_and_show_all)

    def filter_orders_by_status(self, status):
        """Filter orders by status"""
        if status == "All Status":
            # Check if month filter is active
            if hasattr(self.view, 'month_filter_combo') and self.view.month_filter_combo.currentText() != "All Months":
                month_name = self.view.month_filter_combo.currentText()
                self.filter_orders_by_month(month_name)
            else:
                self.load_orders_from_db()
        else:
            # Get all orders first
            all_orders = self.model.get_all_orders()

            if not all_orders:
                self.view.clear_orders_layout()
                error_label = QLabel(f"No orders found")
                error_label.setStyleSheet("color: red; padding: 20px;")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.orders_layout.addWidget(error_label)
                return

            # First filter by status
            status_orders = []
            for order in all_orders:
                order_status = order.get('status', '').lower()
                if order_status == status.lower():
                    status_orders.append(order)

            # Then apply month filter if selected
            filtered_orders = status_orders

            if hasattr(self.view, 'month_filter_combo') and self.view.month_filter_combo.currentText() != "All Months":
                month_name = self.view.month_filter_combo.currentText()
                month_map = {
                    "January": 1, "February": 2, "March": 3, "April": 4,
                    "May": 5, "June": 6, "July": 7, "August": 8,
                    "September": 9, "October": 10, "November": 11, "December": 12
                }
                month_number = month_map.get(month_name)

                if month_number:
                    month_filtered_orders = []
                    for order in filtered_orders:
                        order_date_str = order.get('created_at', '')
                        if order_date_str:
                            try:
                                order_date = self.model.parse_date_string(order_date_str)
                                if order_date and order_date.month == month_number:
                                    month_filtered_orders.append(order)
                            except:
                                continue
                    filtered_orders = month_filtered_orders

            # Display the filtered orders
            if filtered_orders:
                filter_name = f"{status.lower()} orders"
                if hasattr(self.view,
                           'month_filter_combo') and self.view.month_filter_combo.currentText() != "All Months":
                    filter_name = f"{status.lower()} orders in {self.view.month_filter_combo.currentText()}"

                btn = self.view.display_filtered_orders(filtered_orders, filter_name, self.update_order_status)
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
            else:
                # Show no orders message
                filter_name = f"{status.lower()} orders"
                if hasattr(self.view,
                           'month_filter_combo') and self.view.month_filter_combo.currentText() != "All Months":
                    filter_name = f"{status.lower()} orders in {self.view.month_filter_combo.currentText()}"

                btn = self.view.show_no_orders_message(f"No {filter_name} found")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)

    def filter_orders_by_month(self, month_name):
        """Filter orders by selected month"""
        if month_name == "All Months":
            # Check if status filter is applied
            if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                status = self.view.filter_combo.currentText()
                self.filter_orders_by_status(status)
            else:
                self.load_orders_from_db()
            return

        try:
            # Map month name to month number
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }

            month_number = month_map.get(month_name)
            if not month_number:
                return

            # Get all orders from database
            all_orders = self.model.get_all_orders()

            if not all_orders:
                btn = self.view.show_no_orders_message(f"No orders found for {month_name}")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
                return

            # Filter orders by month
            month_orders = []

            for order in all_orders:
                order_date_str = order.get('created_at', '')
                if order_date_str:
                    try:
                        order_date = self.model.parse_date_string(order_date_str)
                        if order_date and order_date.month == month_number:
                            month_orders.append(order)
                    except:
                        continue

            # Apply status filter if selected
            if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                status = self.view.filter_combo.currentText().lower()
                status_filtered_orders = []
                for order in month_orders:
                    if order.get('status', '').lower() == status:
                        status_filtered_orders.append(order)
                month_orders = status_filtered_orders

            # Display filtered orders
            if month_orders:
                filter_name = f"{month_name}"
                if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                    filter_name = f"{self.view.filter_combo.currentText().lower()} orders in {month_name}"

                btn = self.view.display_filtered_orders(month_orders, filter_name, self.update_order_status)
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
            else:
                # Show no orders message
                filter_name = f"{month_name}"
                if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                    filter_name = f"{self.view.filter_combo.currentText().lower()} orders in {month_name}"

                btn = self.view.show_no_orders_message(f"No orders found for {filter_name}")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)

        except Exception as e:
            print(f"Error filtering orders by month: {e}")
            self.view.clear_orders_layout()
            error_label = QLabel(f"Error filtering orders: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view.orders_layout.addWidget(error_label)

    def show_todays_orders(self):
        """Filter orders to show only today's orders"""
        try:
            today = date.today()

            # Get all orders from database
            all_orders = self.model.get_all_orders()

            if not all_orders:
                btn = self.view.show_no_orders_message("No orders found for today")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
                return

            # Filter orders for today
            todays_orders = []
            for order in all_orders:
                order_date_str = order.get('created_at', '')
                if order_date_str:
                    try:
                        order_date = self.model.parse_date_string(order_date_str)
                        if order_date and order_date.date() == today:
                            todays_orders.append(order)
                    except:
                        continue

            # Apply status filter if selected
            if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                status = self.view.filter_combo.currentText().lower()
                status_filtered_orders = []
                for order in todays_orders:
                    if order.get('status', '').lower() == status:
                        status_filtered_orders.append(order)
                todays_orders = status_filtered_orders

            # Display filtered orders
            if todays_orders:
                filter_name = "today's orders"
                if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                    filter_name = f"{self.view.filter_combo.currentText().lower()} orders today"

                btn = self.view.display_filtered_orders(todays_orders, filter_name, self.update_order_status)
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)
            else:
                # Show no orders message
                filter_name = "today"
                if hasattr(self.view, 'filter_combo') and self.view.filter_combo.currentText() != "All Status":
                    filter_name = f"{self.view.filter_combo.currentText().lower()} orders today"

                btn = self.view.show_no_orders_message(f"No orders found for {filter_name}")
                if btn:
                    btn.clicked.connect(self.clear_filters_and_show_all)

        except Exception as e:
            print(f"Error filtering today's orders: {e}")
            self.view.clear_orders_layout()
            error_label = QLabel(f"Error loading today's orders: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view.orders_layout.addWidget(error_label)

    def clear_filters_and_show_all(self):
        """Clear all filters and show all orders"""
        # Reset filter combos
        if hasattr(self.view, 'filter_combo'):
            self.view.filter_combo.setCurrentIndex(0)  # Set to "All Status"

        if hasattr(self.view, 'month_filter_combo'):
            self.view.month_filter_combo.setCurrentIndex(0)  # Set to "All Months"

        if hasattr(self.view, 'search_input'):
            self.view.search_input.clear()

        # Reload all orders
        self.load_orders_from_db()

    def populate_menu_table(self):
        """Populate the menu table with data"""
        self.view.populate_table(self.model.menu_items)

        # Connect edit and delete buttons
        for row in range(self.view.table.rowCount()):
            actions_widget = self.view.table.cellWidget(row, 3)
            if actions_widget:
                edit_btn = actions_widget.layout().itemAt(0).widget()
                delete_btn = actions_widget.layout().itemAt(1).widget()

                if edit_btn:
                    edit_btn.clicked.connect(lambda checked, r=row: self.edit_item(r))
                if delete_btn:
                    delete_btn.clicked.connect(lambda checked, r=row: self.delete_item(r))

    def add_new_item(self):
        """Open dialog to add a new menu item to database"""
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Add New Menu Item")
        dialog.setFixedSize(500, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Title:")
        title_input = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Description
        desc_label = QLabel("Description:")
        desc_input = QTextEdit()
        desc_input.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        # Category
        cat_label = QLabel("Category:")
        cat_input = QComboBox()
        cat_input.addItems(["Burgers", "Sides", "Chicken", "Drinks", "Pizza"])
        cat_input.setStyleSheet("""
            QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #f3f0ff;
                selection-color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        layout.addWidget(cat_label)
        layout.addWidget(cat_input)

        # Price
        price_label = QLabel("Price (₱):")
        price_input = QLineEdit()
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Image path
        image_label = QLabel("Image Path:")
        image_input = QLineEdit("picture/default.png")
        layout.addWidget(image_label)
        layout.addWidget(image_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            title = title_input.text().strip()
            description = desc_input.toPlainText().strip()
            category = cat_input.currentText()
            price = price_input.text().strip()
            image = image_input.text().strip()

            if title and price:
                # Save to database
                try:
                    success, message = self.model.create_menu_item(
                        name=title,
                        description=description,
                        category=category,
                        price=price,
                        image_url=image
                    )

                    if success:
                        # Log the activity
                        self.model.log_activity(
                            "Added menu item",
                            f"{title} (₱{price}) - {category}"
                        )

                        # Reload from database and refresh table
                        self.model.load_menu_items_from_db()
                        self.populate_menu_table()
                        self.view.show_message("Success", "Menu item added to database successfully!")
                    else:
                        self.view.show_message("Error", f"Failed to add menu item: {message}", QMessageBox.Icon.Warning)

                except ValueError:
                    self.view.show_message("Error", "Price must be a number!", QMessageBox.Icon.Warning)
                except Exception as e:
                    self.view.show_message("Error", f"An error occurred: {str(e)}", QMessageBox.Icon.Warning)
            else:
                self.view.show_message("Error", "Title and price are required fields!", QMessageBox.Icon.Warning)

    def edit_item(self, row):
        """Edit a menu item"""
        if row < 0 or row >= len(self.model.menu_items):
            return

        item_data = self.model.menu_items[row]
        item_id = item_data.get('id')
        original_title = item_data["title"]
        original_price = item_data["price"].replace("₱", "") if "₱" in item_data["price"] else item_data["price"]

        dialog = QDialog(self.view)
        dialog.setWindowTitle("Edit Menu Item")
        dialog.setFixedSize(500, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;    
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Title:")
        title_input = QLineEdit(item_data["title"])
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Description
        desc_label = QLabel("Description:")
        desc_input = QTextEdit(item_data["description"])
        desc_input.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        # Category
        cat_label = QLabel("Category:")
        cat_input = QComboBox()
        cat_input.addItems(["Burgers", "Sides", "Chicken", "Drinks", "Pizza"])
        cat_input.setCurrentText(item_data["category"])
        cat_input.setStyleSheet("""
            QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #f3f0ff;
                selection-color: black;
            }
        """)
        layout.addWidget(cat_label)
        layout.addWidget(cat_input)

        # Price (remove ₱ symbol for editing)
        price_value = item_data["price"].replace("₱", "") if "₱" in item_data["price"] else item_data["price"]
        price_label = QLabel("Price (₱):")
        price_input = QLineEdit(price_value)
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Image path
        image_label = QLabel("Image Path:")
        image_input = QLineEdit(item_data["image"])
        layout.addWidget(image_label)
        layout.addWidget(image_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_title = title_input.text().strip()
            updated_description = desc_input.toPlainText().strip()
            updated_category = cat_input.currentText()
            updated_price = price_input.text().strip()
            updated_image = image_input.text().strip()

            if updated_title and updated_price:
                # Update in database
                try:
                    success, message = self.model.update_menu_item(
                        item_id=item_id,
                        name=updated_title,
                        description=updated_description,
                        category=updated_category,
                        price=updated_price,
                        image_url=updated_image
                    )

                    if success:
                        # Log the activity
                        log_details = []
                        if original_title != updated_title:
                            log_details.append(f"Name: {original_title} → {updated_title}")
                        if original_price != updated_price:
                            log_details.append(f"Price: ₱{original_price} → ₱{updated_price}")
                        if item_data["category"] != updated_category:
                            log_details.append(f"Category: {item_data['category']} → {updated_category}")

                        if log_details:
                            self.model.log_activity(
                                "Updated menu item",
                                f"{updated_title}: " + ", ".join(log_details)
                            )

                        # Reload from database and refresh table
                        self.model.load_menu_items_from_db()
                        self.populate_menu_table()
                        self.view.show_message("Success", "Menu item updated in database successfully!")
                    else:
                        self.view.show_message("Error", f"Failed to update menu item: {message}",
                                               QMessageBox.Icon.Warning)

                except ValueError:
                    self.view.show_message("Error", "Price must be a number!", QMessageBox.Icon.Warning)
                except Exception as e:
                    self.view.show_message("Error", f"An error occurred: {str(e)}", QMessageBox.Icon.Warning)
            else:
                self.view.show_message("Error", "Title and price are required fields!", QMessageBox.Icon.Warning)

    def delete_item(self, row):
        """Delete a menu item from database with confirmation"""
        if row < 0 or row >= len(self.model.menu_items):
            return

        item_data = self.model.menu_items[row]
        item_id = item_data.get('id')
        item_name = item_data["title"]

        msg = QMessageBox()
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete '{item_name}' from the database?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

        msg.button(QMessageBox.StandardButton.Yes).setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #ff6b6b;
                border: 1px solid #ff5252;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            # Delete from database
            success, message = self.model.delete_menu_item(item_id)

            if success:
                # Log the activity
                self.model.log_activity(
                    "Deleted menu item",
                    f"{item_name}"
                )

                # Reload from database and refresh table
                self.model.load_menu_items_from_db()
                self.populate_menu_table()
                self.view.show_message("Success", f"'{item_name}' has been deleted from database.")
            else:
                self.view.show_message("Error", f"Failed to delete item: {message}", QMessageBox.Icon.Warning)

    def populate_user_table(self):
        """Populate the user table with data"""
        self.view.populate_user_table_with_data(
            self.model.all_users,
            self.edit_user,
            self.delete_user
        )

    def refresh_users(self):
        """Refresh user data"""
        self.model.load_users_from_db()
        self.populate_user_table()

    def search_users(self):
        """Search users based on search term"""
        search_term = self.view.user_search_input.text().strip().lower()
        if not search_term:
            # If search is empty, show all users
            self.view.populate_user_table_with_data(
                self.model.all_users,
                self.edit_user,
                self.delete_user
            )
            return

        # Filter users based on search term
        filtered_users = []
        for user in self.model.all_users:
            if (search_term in user['name'].lower() or
                    search_term in user['email'].lower() or
                    search_term in user['role'].lower()):
                filtered_users.append(user)

        # Populate table with filtered users
        self.view.populate_user_table_with_data(
            filtered_users,
            self.edit_user,
            self.delete_user
        )

    def filter_users_by_role(self, role):
        """Filter users by role"""
        if role == "All Roles":
            # Show all users
            self.view.populate_user_table_with_data(
                self.model.all_users,
                self.edit_user,
                self.delete_user
            )
        else:
            # Filter users by selected role
            filtered_users = [user for user in self.model.all_users if user['role'].lower() == role.lower()]
            self.view.populate_user_table_with_data(
                filtered_users,
                self.edit_user,
                self.delete_user
            )

    def add_new_user(self):
        """Function to handle adding a new user (Staff or Customer)"""
        dialog = AddUserDialog(self.view)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()

            if user_data:
                success = False
                message = ""

                if user_data["role"] == "Customer":
                    success, message = self.model.create_customer(
                        full_name=user_data["fullname"],
                        email=user_data["email"],
                        phone=user_data["phone"],
                        address=user_data["address"],
                        password=user_data["password"]
                    )

                elif user_data["role"] == "Staff":
                    success, message = self.model.create_staff(
                        staff_name=user_data["fullname"],
                        staff_email=user_data["email"],
                        staff_phone=user_data["phone"],
                        staff_address=user_data["address"],
                        staff_password=user_data["password"]
                    )

                if success:
                    # Log the activity
                    self.model.log_activity(
                        f"Added new {user_data['role'].lower()}",
                        f"{user_data['fullname']} ({user_data['email']})"
                    )

                    self.view.show_message("Success", message, QMessageBox.Icon.Information)
                    # Refresh user data
                    self.refresh_users()
                else:
                    self.view.show_message("Error", f"Failed to create {user_data['role'].lower()}: {message}",
                                           QMessageBox.Icon.Warning)

    def edit_user(self, row, user):
        """Edit an existing user"""
        dialog = EditUserDialog(self.view, user)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_user_data()

            if updated_data:
                success = False
                message = ""

                if user['type'] == "customer":
                    success, message = self.model.update_customer(
                        customer_id=user['id'],
                        full_name=updated_data['fullname'],
                        email=updated_data['email'],
                        phone=updated_data['phone'],
                        address=updated_data['address'],
                        password=updated_data['password']
                    )

                elif user['type'] == "staff":
                    success, message = self.model.update_staff(
                        staff_id=user['id'],
                        staff_name=updated_data['fullname'],
                        staff_email=updated_data['email'],
                        staff_phone=updated_data['phone'],
                        staff_address=updated_data['address'],
                        staff_password=updated_data['password']
                    )

                if success:
                    # Log the activity
                    self.model.log_activity(
                        f"Updated {user['type']}",
                        f"{user['name']} → {updated_data['fullname']}"
                    )

                    self.view.show_message("Success", message, QMessageBox.Icon.Information)
                    # Refresh user data
                    self.refresh_users()
                else:
                    self.view.show_message("Error", f"Failed to update user: {message}", QMessageBox.Icon.Warning)

    def delete_user(self, row, user):
        """Delete a user with confirmation"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete {user['name']} ({user['email']})?")
        msg.setInformativeText("This action cannot be undone.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        yes_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #dc2626;
                border: 1px solid #b91c1c;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            success = False
            message = ""

            try:
                if user['type'] == "customer":
                    success, message = self.model.delete_customer(user['id'])

                elif user['type'] == "staff":
                    success, message = self.model.delete_staff(user['id'])

                if success:
                    # Log the activity
                    self.model.log_activity(
                        f"Deleted {user['type']}",
                        f"{user['name']} ({user['email']})"
                    )

                    self.view.show_message("Success", message, QMessageBox.Icon.Information)
                    # Refresh user data
                    self.refresh_users()
                else:
                    self.view.show_message("Error", f"Failed to delete user: {message}", QMessageBox.Icon.Warning)

            except Exception as e:
                print(f"DEBUG: Exception during delete: {e}")
                self.view.show_message("Error", f"An error occurred: {str(e)}", QMessageBox.Icon.Critical)

    def refresh_activity_logs(self):
        """Refresh activity logs from database"""
        try:
            # Check if a period filter is active
            if hasattr(self.view, 'period_filter_combo') and self.view.period_filter_combo.currentText() != "All Time":
                # Apply the current period filter
                self.filter_activities_by_period(self.view.period_filter_combo.currentText())
            else:
                # Load all activities
                success, activities = self.model.get_all_activities(limit=100)

                if success:
                    self.view.populate_activity_table(activities)
                    # Update stats label
                    self.view.activity_stats_label.setText(f"Total activities: {len(activities)}")
                else:
                    self.view.show_message("Error", "Failed to load activity logs", QMessageBox.Icon.Warning)

        except Exception as e:
            print(f"Error refreshing activity logs: {e}")
            self.view.show_message("Error", "Failed to refresh activity logs", QMessageBox.Icon.Warning)

    def search_activities(self):
        """Search activities"""
        search_term = self.view.activity_search_input.text().strip()

        if not search_term:
            self.refresh_activity_logs()
            return

        success, activities = self.model.search_activities(search_term)

        if success:
            self.view.populate_activity_table(activities)
        else:
            self.view.show_message("Error", "Failed to search activities", QMessageBox.Icon.Warning)

    def show_todays_activities(self):
        """Show today's activity logs"""
        try:
            today = date.today()

            # Get all activities
            success, all_activities = self.model.get_all_activities(limit=1000)

            if not success:
                self.view.show_message("Error", "Failed to load activities", QMessageBox.Icon.Warning)
                return

            # Filter activities for today
            todays_activities = []
            for activity in all_activities:
                timestamp = activity.get('created_at', '')
                if timestamp:
                    try:
                        if isinstance(timestamp, datetime):
                            activity_date = timestamp.date()
                        elif isinstance(timestamp, str):
                            # Try to extract date from timestamp string
                            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f",
                                        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]:
                                try:
                                    activity_dt = datetime.strptime(timestamp.split('.')[0], fmt)
                                    activity_date = activity_dt.date()
                                    break
                                except:
                                    continue
                            else:
                                continue
                        else:
                            continue

                        if activity_date == today:
                            todays_activities.append(activity)
                    except:
                        continue

            # Display filtered activities
            self.view.populate_activity_table(todays_activities)

            # Update stats label
            self.view.activity_stats_label.setText(f"Today's activities: {len(todays_activities)}")

            # Reset the combobox to "All Time" when showing today's logs
            if hasattr(self.view, 'period_filter_combo'):
                self.view.period_filter_combo.setCurrentText("All Time")

            if todays_activities:
                self.view.show_message("Today's Logs",
                                       f"Showing {len(todays_activities)} activities from today",
                                       QMessageBox.Icon.Information)
            else:
                self.view.show_message("Today's Logs",
                                       "No activities found for today",
                                       QMessageBox.Icon.Information)

        except Exception as e:
            print(f"Error showing today's activities: {e}")
            self.view.show_message("Error",
                                   f"Failed to load today's activities: {str(e)}",
                                   QMessageBox.Icon.Warning)

    def filter_activities_by_period(self, period):
        """Filter activities by time period (Last 3 days, 7 days, 30 days)"""
        if period == "All Time":
            # Load all activities
            self.refresh_activity_logs()
            return

        try:
            # Calculate the start date based on the period
            today = date.today()

            if period == "Last 3 Days":
                start_date = today - timedelta(days=2)  # Today + 2 previous days
            elif period == "Last 7 Days":
                start_date = today - timedelta(days=6)  # Today + 6 previous days
            elif period == "Last 30 Days":
                start_date = today - timedelta(days=29)  # Today + 29 previous days
            else:
                return

            # Get all activities
            success, all_activities = self.model.get_all_activities(limit=1000)

            if not success:
                self.view.show_message("Error", "Failed to load activities", QMessageBox.Icon.Warning)
                return

            # Filter activities by date range
            filtered_activities = []
            for activity in all_activities:
                timestamp = activity.get('created_at', '')
                if timestamp:
                    try:
                        if isinstance(timestamp, datetime):
                            activity_date = timestamp.date()
                        elif isinstance(timestamp, str):
                            # Try to extract date from timestamp string
                            timestamp_str = str(timestamp).split('.')[0]  # Remove microseconds if present

                            # Try different date formats
                            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f",
                                        "%Y-%m-%dT%H:%M:%S", "%Y-%m-dT%H:%M:%S.%f"]:
                                try:
                                    activity_dt = datetime.strptime(timestamp_str, fmt)
                                    activity_date = activity_dt.date()
                                    break
                                except ValueError:
                                    continue
                            else:
                                # If none of the formats work, try to extract just the date part
                                try:
                                    date_part = timestamp_str.split(' ')[0]
                                    activity_date = datetime.strptime(date_part, "%Y-%m-%d").date()
                                except:
                                    continue
                        else:
                            continue

                        # Check if activity date is within the range
                        if start_date <= activity_date <= today:
                            filtered_activities.append(activity)

                    except Exception as e:
                        print(f"DEBUG: Error parsing timestamp '{timestamp}': {e}")
                        continue

            # Display filtered activities
            self.view.populate_activity_table(filtered_activities)

            # Update stats label
            period_text = period.lower()
            if period == "Last 3 Days":
                period_text = "last 3 days"
            elif period == "Last 7 Days":
                period_text = "last 7 days"
            elif period == "Last 30 Days":
                period_text = "last 30 days"

            self.view.activity_stats_label.setText(f"Activities in the {period_text}: {len(filtered_activities)}")

        except Exception as e:
            print(f"Error filtering activities by period: {e}")
            self.view.show_message("Error",
                                   f"Failed to filter activities: {str(e)}",
                                   QMessageBox.Icon.Warning)

    def clear_activity_logs(self):
        """Clear all activity logs with confirmation"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Clear Logs")
        msg.setText("Are you sure you want to clear ALL activity logs?")
        msg.setInformativeText("This action cannot be undone!")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        yes_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #dc2626;
                border: 1px solid #b91c1c;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            success, message = self.model.clear_all_activities()

            if success:
                self.refresh_activity_logs()
                self.view.show_message("Success", "All activity logs have been cleared", QMessageBox.Icon.Information)
            else:
                self.view.show_message("Error", f"Failed to clear logs: {message}", QMessageBox.Icon.Warning)

    def handle_logout(self):
        """Show confirmation dialog before logging out"""
        result = self.view.show_logout_confirmation()
        if result == QMessageBox.StandardButton.Yes:
            # Log logout activity
            self.model.log_activity("Admin logged out")
            self.view.logout_requested.emit()

    def show(self):
        """Show the dashboard window"""
        self.view.show()

    def close(self):
        """Close the dashboard window"""
        self.view.close()

    def export_overview_to_pdf(self):
        """Export all overview page content to PDF"""
        try:
            # Ask user for save location
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Export Overview to PDF",
                f"Admin_Dashboard_Overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return  # User cancelled

            # Ensure .pdf extension
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'

            # Get current overview data
            total_revenue = self.model.get_total_revenue_from_db()
            today_orders = self.model.get_todays_orders_count()
            pending_orders = self.model.get_pending_orders_count()
            user_count = len([u for u in self.model.all_users if u['role'].lower() != 'admin'])

            # Get accurate monthly revenue data from database
            monthly_revenue = self._get_accurate_monthly_revenue_data()

            # Get accurate popular items data from database
            popular_items = self._get_accurate_popular_items_data()

            # Create PDF document
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#4F39F6')
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=colors.HexColor('#333333')
            )

            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6
            )

            bold_style = ParagraphStyle(
                'CustomBold',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                fontName='Helvetica-Bold'
            )

            # Create a clean style without bullets
            clean_style = ParagraphStyle(
                'CleanStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                leftIndent=0,
                firstLineIndent=0,
                bulletIndent=0
            )

            # Build story (content)
            story = []

            # Title
            story.append(Paragraph("Admin Dashboard - Analytics Overview", title_style))
            story.append(Spacer(1, 20))

            # Date and Admin Info
            current_date = datetime.now().strftime("%B %d, %Y %I:%M %p")
            story.append(Paragraph(f"<b>Report Generated:</b> {current_date}", clean_style))
            story.append(
                Paragraph(f"<b>Admin:</b> {self.model.admin_name} | <b>ID:</b> {self.model.admin_id}", clean_style))
            story.append(Spacer(1, 30))

            # Analytics Cards Section
            story.append(Paragraph("Key Performance Indicators", heading_style))
            story.append(Spacer(1, 15))

            # Create a clean table for the KPIs without bullet points
            kpi_data = [
                ["Metric", "Value"],
                ["Total Revenue", f"₱{total_revenue:,.2f}"],
                ["Today's Orders", str(today_orders)],
                ["Pending Orders", str(pending_orders)],
                ["Active Users", str(user_count)]
            ]

            kpi_table = Table(kpi_data, colWidths=[2.5 * inch, 2.5 * inch])
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F39F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f9f9f9')),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (0, -1), 11),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 1), (1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
            ]))

            story.append(kpi_table)
            story.append(Spacer(1, 30))

            # Revenue Trend Section
            story.append(Paragraph("Monthly Revenue Trend (Last 6 Months)", heading_style))
            story.append(Spacer(1, 15))

            # Create revenue data table
            if monthly_revenue:
                revenue_data = [["Month", "Revenue (₱)"]]

                # Sort months in chronological order
                month_order = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]

                # Get current month index
                current_month_index = datetime.now().month - 1

                # Get last 6 months in correct order
                sorted_months = []
                for i in range(6):
                    month_index = (current_month_index - i) % 12
                    month_name = month_order[month_index]
                    if month_name in monthly_revenue:
                        sorted_months.append(month_name)

                # Add data in chronological order
                for month in reversed(sorted_months):
                    revenue = monthly_revenue.get(month, 0)
                    revenue_data.append([month, f"₱{revenue:,.2f}"])

                revenue_table = Table(revenue_data, colWidths=[2 * inch, 2 * inch])
                revenue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F39F6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ]))
                story.append(revenue_table)

                # Add total for the period with clean formatting
                total_period_revenue = sum(monthly_revenue.values())
                story.append(Spacer(1, 10))
                story.append(
                    Paragraph(f"<b>Total Revenue (Last 6 Months): ₱{total_period_revenue:,.2f}</b>", clean_style))
            else:
                story.append(Paragraph("No revenue data available for the past 6 months.", clean_style))

            story.append(Spacer(1, 30))

            # Popular Items Section
            story.append(Paragraph("Most Popular Menu Items", heading_style))
            story.append(Spacer(1, 15))

            if popular_items:
                items_data = [["Rank", "Item", "Category", "Orders", "Revenue (₱)"]]
                for idx, item in enumerate(popular_items[:10], 1):  # Top 10 items
                    items_data.append([
                        str(idx),
                        item.get('name', 'Unknown'),
                        item.get('category', 'Unknown'),
                        str(item.get('order_count', 0)),
                        f"₱{item.get('total_revenue', 0):,.2f}"
                    ])

                items_table = Table(items_data, colWidths=[0.5 * inch, 2 * inch, 1.5 * inch, 1 * inch, 1.5 * inch])
                items_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F39F6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Rank column centered
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Item name left aligned
                    ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Orders centered
                    ('ALIGN', (4, 1), (4, -1), 'RIGHT'),  # Revenue right aligned
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ]))
                story.append(items_table)

                # Add summary statistics with clean formatting
                total_orders = sum(item.get('order_count', 0) for item in popular_items[:10])
                total_revenue_popular = sum(item.get('total_revenue', 0) for item in popular_items[:10])
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    f"<b>Top 10 Items Summary:</b> {total_orders} orders, Total Revenue: ₱{total_revenue_popular:,.2f}",
                    clean_style))
            else:
                story.append(Paragraph("No popular items data available.", clean_style))

            story.append(Spacer(1, 30))

            # Summary Section
            story.append(Paragraph("Summary", heading_style))
            story.append(Spacer(1, 15))

            # Clean summary without bullet points
            summary_lines = [
                f"This report summarizes the current state of the restaurant management system.",
                f"",
                f"<b>Total Revenue:</b> ₱{total_revenue:,.2f} - Total income from all completed orders.",
                f"<b>Today's Orders:</b> {today_orders} orders - Orders placed today.",
                f"<b>Pending Orders:</b> {pending_orders} orders - Orders awaiting processing or delivery.",
                f"<b>Active Users:</b> {user_count} users - Registered customers and staff (excluding admins).",
                f"",
                f"The monthly revenue trend shows performance over the past 6 months, while the popular items section highlights the most frequently ordered menu items and their contribution to revenue.",
                f"",
                f"<b>Report Generated:</b> {current_date}",
                f"<b>Generated by:</b> {self.model.admin_name}"
            ]

            for line in summary_lines:
                if line.strip():  # Skip empty lines
                    story.append(Paragraph(line, clean_style))
                    story.append(Spacer(1, 4))

            story.append(Spacer(1, 20))

            # Footer
            footer_text = f"FoodDash Restaurant Management System | Report generated on {current_date}"
            story.append(Paragraph(footer_text, ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.gray,
                alignment=TA_CENTER
            )))

            # Build PDF
            doc.build(story)

            # Log the activity
            self.model.log_activity(
                "Exported overview to PDF",
                f"File saved as: {os.path.basename(file_path)}"
            )

            # Show success message
            self.view.show_message(
                "Export Successful",
                f"Dashboard overview has been exported to PDF:\n{file_path}",
                QMessageBox.Icon.Information
            )

            return True

        except Exception as e:
            print(f"Error exporting PDF: {e}")
            import traceback
            traceback.print_exc()
            self.view.show_message(
                "Export Failed",
                f"Failed to export PDF: {str(e)}",
                QMessageBox.Icon.Warning
            )
            return False

    def _get_accurate_monthly_revenue_data(self):
        """Get accurate monthly revenue data from database for the past 6 months"""
        try:
            # Import orders_db to query orders
            from db.orders_db import orders_db_instance as orders_db

            # Get all completed orders
            success, orders = orders_db.get_all_orders()
            if not success:
                print("Failed to get orders for monthly revenue data")
                return {}

            # Initialize monthly revenue dictionary for last 6 months
            monthly_revenue = {}
            current_date = datetime.now()

            # Generate last 6 months
            for i in range(6):
                month_date = current_date - timedelta(days=30 * i)
                month_name = month_date.strftime("%B")
                monthly_revenue[month_name] = 0.0

            # Process orders
            for order in orders:
                # Only count completed orders
                if order.get('status', '').lower() == 'completed':
                    order_date_str = order.get('created_at', '')
                    if order_date_str:
                        try:
                            order_date = self.model.parse_date_string(order_date_str)
                            if order_date:
                                # Check if order is within last 6 months
                                six_months_ago = current_date - timedelta(days=180)
                                if order_date >= six_months_ago:
                                    month_name = order_date.strftime("%B")
                                    amount = float(order.get('total_amount', 0))
                                    if month_name in monthly_revenue:
                                        monthly_revenue[month_name] += amount
                        except Exception as e:
                            print(f"Error processing order date: {e}")
                            continue

            return monthly_revenue

        except Exception as e:
            print(f"Error getting accurate monthly revenue data: {e}")
            return {}

    def _get_accurate_popular_items_data(self):
        """Get accurate popular menu items data from database"""
        try:
            # Import orders_db to query orders
            from db.orders_db import orders_db_instance as orders_db
            # Import menu_db to get item names
            from db.menu_db import menu_db

            # Get all completed orders
            success, orders = orders_db.get_all_orders()
            if not success:
                print("Failed to get orders for popular items data")
                return []

            # Dictionary to track item statistics
            item_stats = {}

            # Process orders
            for order in orders:
                # Only count completed orders
                if order.get('status', '').lower() == 'completed':
                    items = order.get('items', [])
                    for item in items:
                        item_id = item.get('item_id')
                        item_name = item.get('title', 'Unknown')
                        item_price = float(item.get('price', 0).replace('₱', '').replace(',', '')) if '₱' in str(
                            item.get('price', 0)) else float(item.get('price', 0))
                        quantity = int(item.get('qty', 1))

                        # Get category from menu_db if possible
                        item_category = 'Unknown'
                        try:
                            if item_id:
                                menu_item = menu_db.get_menu_item_by_id(item_id)
                                if menu_item:
                                    item_category = menu_item.get('category', 'Unknown')
                        except:
                            pass

                        if item_name not in item_stats:
                            item_stats[item_name] = {
                                'name': item_name,
                                'category': item_category,
                                'order_count': 0,
                                'total_quantity': 0,
                                'total_revenue': 0.0
                            }

                        item_stats[item_name]['order_count'] += 1
                        item_stats[item_name]['total_quantity'] += quantity
                        item_stats[item_name]['total_revenue'] += (item_price * quantity)

            # Convert to list and sort by order count (most popular first)
            popular_items = list(item_stats.values())
            popular_items.sort(key=lambda x: x['order_count'], reverse=True)

            return popular_items[:20]  # Return top 20 items

        except Exception as e:
            print(f"Error getting accurate popular items data: {e}")
            return []