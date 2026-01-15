"""
Customer Login Controller
Coordinates between Model and View, handles business logic
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional, Dict
from models.customer_login_model import CustomerLoginModel
from views.customer_login_view import CustomerLoginView


class CustomerLoginController(QObject):
    """Controller for customer login functionality"""

    # Signals emitted by controller
    login_successful = pyqtSignal(dict)  # customer_info
    login_failed = pyqtSignal(str)  # error_message - CHANGED BACK
    navigate_to_create_account = pyqtSignal()
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = CustomerLoginModel()
        self.view = CustomerLoginView()

        # Connect view signals to controller methods
        self.view.login_attempted.connect(self.handle_login)
        self.view.create_account_requested.connect(self.handle_create_account_request)
        self.view.back_requested.connect(self.handle_back_request)

        # Connect controller signals to view methods
        # self.login_failed.connect(self.view.show_error_message)  # REMOVE THIS LINE

    def handle_login(self, email: str, password: str):
        """
        Handle login attempt

        Args:
            email: Customer email
            password: Customer password
        """
        # Validate input
        is_valid, error_msg = self.model.validate_input(email, password)
        if not is_valid:
            # Show error message directly on the view
            self.view.show_error_message("Input Error", error_msg)
            self.login_failed.emit(error_msg)  # Emit error message signal
            return

        # Authenticate
        success, customer_info = self.model.authenticate(email, password)

        if success and customer_info:
            # Clear view fields
            self.view.clear_fields()

            # Get full customer info if needed
            full_info = self.model.get_customer_info(customer_info.get('id'))
            if full_info:
                customer_info = full_info

            # Emit success signal
            self.login_successful.emit(customer_info)

            # Show success message
            self.view.show_success_message(
                "Login Successful",
                f"Welcome back, {customer_info.get('full_name', 'Customer')}!"
            )
        else:
            error_msg = "Invalid email or password. Please try again."
            self.view.show_error_message("Login Failed", error_msg)
            self.login_failed.emit(error_msg)

    def handle_create_account_request(self):
        """Handle request to navigate to create account page"""
        self.navigate_to_create_account.emit()

    def handle_back_request(self):
        """Handle request to go back"""
        self.navigate_back.emit()

    def get_view(self) -> CustomerLoginView:
        """Get the view component"""
        return self.view

    def reset_view(self):
        """Reset the view to initial state"""
        self.view.clear_fields()
        if hasattr(self.view, 'show_pass_btn'):
            self.view.show_pass_btn.setChecked(False)
        self.clear_error_messages()

    def set_error_message(self, field: str, message: str):
        """
        Set error message for specific field

        Args:
            field: Field name ('email' or 'password')
            message: Error message to display
        """
        if field == 'email':
            self.view.email_input.setStyleSheet("""
                QLineEdit {
                    border-radius: 10px;
                    border: 2px solid red;
                    padding-left: 10px;
                    color: black;
                }
            """)
        elif field == 'password':
            self.view.password_input.setStyleSheet("""
                QLineEdit {
                    border-radius: 10px;
                    border: 2px solid red;
                    padding-left: 10px;
                    color: black;
                }
            """)

    def clear_error_messages(self):
        """Clear all error messages and styling"""
        self.view.email_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                border: 1px solid #e3e3e3;
                padding-left: 10px;
                color: black;
            }
        """)
        self.view.password_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                border: 1px solid #e3e3e3;
                padding-left: 10px;
                color: black;
            }
        """)