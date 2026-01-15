"""
Customer Create Account Controller
Coordinates between Model and View, handles business logic
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict
from models.customer_create_model import CustomerCreateModel
from views.customer_create_view import CustomerCreateView


class CustomerCreateController(QObject):
    """Controller for customer account creation functionality"""

    # Signals emitted by controller
    account_created = pyqtSignal()
    creation_failed = pyqtSignal(str, str)  # title, error_message
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = CustomerCreateModel()
        self.view = CustomerCreateView()

        # Connect view signals to controller methods
        self.view.create_account_attempted.connect(self.handle_create_account)
        self.view.back_requested.connect(self.handle_back_request)

        # Connect controller signals to view methods
        self.creation_failed.connect(self.view.show_error_message)

        # Test database connection on initialization
        self._test_database_connection()

    def _test_database_connection(self):
        """Test database connection and show warning if needed"""
        success, message = self.model.test_connection()
        if not success:
            self.view.show_error_message(
                "Database Warning",
                f"Database connection issue: {message}\nAccounts will not be saved."
            )

    def handle_create_account(self, form_data: Dict):
        """
        Handle account creation attempt

        Args:
            form_data: Dictionary containing all form fields
        """
        # Extract data
        full_name = form_data['full_name']
        email = form_data['email']
        phone = form_data['phone']
        address = form_data['address']
        password = form_data['password']
        confirm_password = form_data['confirm_password']

        # Validate input
        is_valid, field, error_msg = self.model.validate_input(
            full_name, email, phone, address, password, confirm_password
        )

        if not is_valid:
            # Reset all field styles first
            self.view.reset_field_styles()

            if field == "all":
                self.view.show_error_message("Missing Fields", error_msg)
            else:
                self.view.set_error_message(field, error_msg)
            return

        # Create account in database
        success, message = self.model.create_customer(
            full_name, email, phone, address, password
        )

        if success:
            # Clear form and show success
            self.view.clear_fields()
            self.view.reset_field_styles()
            self.view.show_success_message("Success", message)

            # Emit account created signal
            self.account_created.emit()
        else:
            self.creation_failed.emit("Registration Failed", message)

    def handle_back_request(self):
        """Handle request to go back"""
        self.navigate_back.emit()

    def get_view(self) -> CustomerCreateView:
        """Get the view component"""
        return self.view

    def reset_view(self):
        """Reset the view to initial state"""
        self.view.clear_fields()
        self.view.reset_field_styles()
        self.view.clear_error_messages()
        if hasattr(self.view, 'show_pass_btn'):
            self.view.show_pass_btn.setChecked(False)
        if hasattr(self.view, 'show_confirm_btn'):
            self.view.show_confirm_btn.setChecked(False)