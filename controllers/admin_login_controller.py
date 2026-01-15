"""
Admin Login Controller
Coordinates between Model and View, handles business logic
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional, Dict
from models.admin_login_model import AdminLoginModel
from views.admin_login_view import AdminLoginView


class AdminLoginController(QObject):
    """Controller for admin login functionality"""

    # Signals emitted by controller
    login_successful = pyqtSignal(dict)  # admin_info
    login_failed = pyqtSignal(str, str)  # title, error_message
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = AdminLoginModel()
        self.view = AdminLoginView()

        # Connect view signals to controller methods
        self.view.login_attempted.connect(self.handle_login)
        self.view.back_requested.connect(self.handle_back_request)

        # Connect controller signals to view methods
        self.login_failed.connect(self.view.show_error_message)

    def handle_login(self, identifier: str, password: str):
        """
        Handle admin login attempt

        Args:
            identifier: Admin ID or Email
            password: Admin password
        """
        # Validate input
        is_valid, error_msg = self.model.validate_input(identifier, password)
        if not is_valid:
            self.login_failed.emit("Input Error", error_msg)
            return

        # Authenticate
        success, admin_info = self.model.authenticate(identifier, password)

        if success and admin_info:
            # Clear view fields
            self.view.clear_fields()
            self.view.show_pass_btn.setChecked(False)

            # Emit success signal
            self.login_successful.emit(admin_info)

            # Show success message
            self.view.show_success_message(
                "Login Successful",
                f"Welcome, Administrator {admin_info.get('full_name', 'Admin')}!"
            )
        else:
            self.login_failed.emit(
                "Login Failed",
                "Invalid Admin ID/Email or password. Please try again."
            )

    def handle_back_request(self):
        """Handle request to go back"""
        self.navigate_back.emit()

    def get_view(self) -> AdminLoginView:
        """Get the view component"""
        return self.view

    def reset_view(self):
        """Reset the view to initial state"""
        self.view.clear_fields()
        self.view.show_pass_btn.setChecked(False)