"""
Staff Login Controller
Coordinates between Model and View, handles business logic
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional, Dict
from models.staff_login_model import StaffLoginModel
from views.staff_login_view import StaffLoginView


class StaffLoginController(QObject):
    """Controller for staff login functionality"""

    # Signals emitted by controller
    login_successful = pyqtSignal(dict)  # staff_info
    login_failed = pyqtSignal(str, str)  # title, error_message
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = StaffLoginModel()
        self.view = StaffLoginView()

        # Connect view signals to controller methods
        self.view.login_attempted.connect(self.handle_login)
        self.view.back_requested.connect(self.handle_back_request)

        # Connect controller signals to view methods
        self.login_failed.connect(self.view.show_error_message)

    def handle_login(self, identifier: str, password: str):
        """
        Handle staff login attempt

        Args:
            identifier: Staff ID or Email
            password: Staff password
        """
        # Validate input
        is_valid, error_msg = self.model.validate_input(identifier, password)
        if not is_valid:
            self.login_failed.emit("Input Error", error_msg)
            return

        # Authenticate
        success, staff_info = self.model.authenticate(identifier, password)

        if success and staff_info:
            # Clear view fields
            self.view.clear_fields()
            self.view.show_pass_btn.setChecked(False)

            # Emit success signal
            self.login_successful.emit(staff_info)

            # Show success message
            self.view.show_success_message(
                "Login Successful",
                f"Welcome, {staff_info.get('full_name', 'Staff')}!"
            )
        else:
            self.login_failed.emit(
                "Login Failed",
                "Invalid Staff ID/Email or password. Please try again."
            )

    def handle_back_request(self):
        """Handle request to go back"""
        self.navigate_back.emit()

    def get_view(self) -> StaffLoginView:
        """Get the view component"""
        return self.view

    def reset_view(self):
        """Reset the view to initial state"""
        self.view.clear_fields()
        self.view.show_pass_btn.setChecked(False)