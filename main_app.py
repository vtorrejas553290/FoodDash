# main_app.py (Updated main file)
"""
Main Application File - Updated for Package Structure
Entry point for the Food Dash application
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

# Import from packages
from views.home_view import HomeView
from controllers.customer_login_controller import CustomerLoginController
from controllers.customer_menu_controller import CustomerMenuController
from controllers.customer_create_controller import CustomerCreateController
from controllers.staff_login_controller import StaffLoginController
from controllers.admin_login_controller import AdminLoginController
from controllers.staff_dashboard_controller import StaffDashboardController

# Import the admin dashboard components directly
from controllers.admin_dashboard_controller import AdminDashboardController


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Food Dash")
        self.setMinimumSize(1100, 650)
        self.setStyleSheet("background-color: #f4f8ff;")

        # Create stacked widget for pages
        self.stack = QStackedWidget()

        # Initialize home view
        self.home_view = HomeView()

        # Initialize controllers (others will be created dynamically)
        self.customer_login_controller = CustomerLoginController()
        self.customer_create_controller = CustomerCreateController()
        self.staff_login_controller = StaffLoginController()
        self.admin_login_controller = AdminLoginController()

        # These controllers will be created dynamically when users log in
        self.customer_menu_controller = None
        self.customer_menu_added = False
        self.staff_dashboard_controller = None
        self.staff_dashboard_added = False
        self.admin_dashboard_controller = None
        self.admin_dashboard_added = False

        # Set up all signal connections
        self._setup_connections()

        # Add views to stack (Home is index 0)
        self.stack.addWidget(self.home_view)
        self.stack.addWidget(self.customer_login_controller.get_view())
        self.stack.addWidget(self.customer_create_controller.get_view())
        self.stack.addWidget(self.staff_login_controller.get_view())
        self.stack.addWidget(self.admin_login_controller.get_view())

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect home view cards to navigation
        self.home_view.customer_card.mousePressEvent = lambda e: self.show_customer_login()
        self.home_view.staff_card.mousePressEvent = lambda e: self.show_staff_login()
        self.home_view.admin_card.mousePressEvent = lambda e: self.show_admin_login()

    def _setup_connections(self):
        """Setup all signal connections between controllers"""

        # Customer Login Controller connections
        self.customer_login_controller.login_successful.connect(self.handle_customer_login_success)
        self.customer_login_controller.navigate_back.connect(self.show_home_page)
        self.customer_login_controller.navigate_to_create_account.connect(self.show_create_account_page)

        # Customer Create Controller connections
        self.customer_create_controller.account_created.connect(self.handle_account_created)
        self.customer_create_controller.navigate_back.connect(self.show_customer_login)

        # Staff Login Controller connections
        self.staff_login_controller.login_successful.connect(self.handle_staff_login_success)
        self.staff_login_controller.navigate_back.connect(self.show_home_page)

        # Admin Login Controller connections
        self.admin_login_controller.login_successful.connect(self.handle_admin_login_success)
        self.admin_login_controller.navigate_back.connect(self.show_home_page)

    def show_home_page(self):
        """Navigate to home page"""
        self.stack.setCurrentIndex(0)

    def show_customer_login(self):
        """Navigate to customer login page"""
        self.customer_login_controller.reset_view()
        self.stack.setCurrentIndex(1)

    def show_create_account_page(self):
        """Navigate to create account page"""
        self.customer_create_controller.reset_view()
        self.stack.setCurrentIndex(2)

    def show_staff_login(self):
        """Navigate to staff login page"""
        self.staff_login_controller.reset_view()
        self.stack.setCurrentIndex(3)

    def show_admin_login(self):
        """Navigate to admin login page"""
        self.admin_login_controller.reset_view()
        self.stack.setCurrentIndex(4)

    def handle_customer_login_success(self, customer_info):
        """Handle successful customer login"""
        print(f"Customer logged in: {customer_info}")

        # Clean up existing customer menu controller if any
        if self.customer_menu_controller:
            self.stack.removeWidget(self.customer_menu_controller.get_view())
            self.customer_menu_controller.deleteLater()
            self.customer_menu_controller = None
            self.customer_menu_added = False

        # Create new customer menu controller with customer info
        self.customer_menu_controller = CustomerMenuController(customer_info)

        # Connect logout signal
        self.customer_menu_controller.logout_requested.connect(self.logout_customer)

        # Add to stack
        self.stack.addWidget(self.customer_menu_controller.get_view())
        self.customer_menu_added = True

        # Navigate to customer menu
        self.stack.setCurrentWidget(self.customer_menu_controller.get_view())

    def handle_account_created(self):
        """Handle successful account creation"""
        self.show_customer_login()

    def handle_staff_login_success(self, staff_info):
        """Handle successful staff login"""
        print(f"Staff logged in: {staff_info}")

        # Clean up existing staff dashboard controller if any
        if self.staff_dashboard_controller:
            self.stack.removeWidget(self.staff_dashboard_controller.get_view())
            self.staff_dashboard_controller.deleteLater()
            self.staff_dashboard_controller = None
            self.staff_dashboard_added = False

        # Create new staff dashboard controller with staff info
        self.staff_dashboard_controller = StaffDashboardController(staff_info)

        # Connect logout signal
        self.staff_dashboard_controller.logout_requested.connect(self.logout_staff)

        # Add to stack
        self.stack.addWidget(self.staff_dashboard_controller.get_view())
        self.staff_dashboard_added = True

        # Navigate to staff dashboard
        self.stack.setCurrentWidget(self.staff_dashboard_controller.get_view())

    def handle_admin_login_success(self, admin_info):
        """Handle successful admin login"""
        print(f"Admin logged in: {admin_info}")

        # Clean up existing admin dashboard controller if any
        if self.admin_dashboard_controller:
            self.stack.removeWidget(self.admin_dashboard_controller.get_view())
            self.admin_dashboard_controller.deleteLater()
            self.admin_dashboard_controller = None
            self.admin_dashboard_added = False

        # Create new admin dashboard controller with admin info
        self.admin_dashboard_controller = AdminDashboardController(admin_info)

        # Connect logout signal
        self.admin_dashboard_controller.logout_requested.connect(self.logout_admin)

        # Add to stack
        self.stack.addWidget(self.admin_dashboard_controller.get_view())
        self.admin_dashboard_added = True

        # Navigate to admin dashboard
        self.stack.setCurrentWidget(self.admin_dashboard_controller.get_view())

    def logout_customer(self):
        """Handle customer logout"""
        if self.customer_menu_controller:
            # Remove from stack
            self.stack.removeWidget(self.customer_menu_controller.get_view())
            self.customer_menu_controller.deleteLater()
            self.customer_menu_controller = None
            self.customer_menu_added = False

        # Navigate back to home
        self.show_home_page()

    def logout_staff(self):
        """Handle staff logout"""
        if self.staff_dashboard_controller:
            # Remove from stack
            self.stack.removeWidget(self.staff_dashboard_controller.get_view())
            self.staff_dashboard_controller.deleteLater()
            self.staff_dashboard_controller = None
            self.staff_dashboard_added = False

        # Navigate back to home
        self.show_home_page()

    def logout_admin(self):
        """Handle admin logout"""
        if self.admin_dashboard_controller:
            # Remove from stack
            self.stack.removeWidget(self.admin_dashboard_controller.get_view())
            self.admin_dashboard_controller.deleteLater()
            self.admin_dashboard_controller = None
            self.admin_dashboard_added = False

        # Navigate back to home
        self.show_home_page()

    def showEvent(self, event):
        """Center the window when shown"""
        super().showEvent(event)
        self.center()

    def center(self):
        """Center the window on screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2,
            self.width(),
            self.height()
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec())