"""
Admin Login Model
Handles admin authentication logic and data operations
"""
from typing import Optional, Dict, Tuple
from db.admin_db import admin_db


class AdminLoginModel:
    """Model for admin login operations"""

    @staticmethod
    def authenticate(identifier: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate admin credentials

        Args:
            identifier: Admin ID or Email
            password: Admin password

        Returns:
            Tuple of (success, admin_info)
        """
        if not identifier or not password:
            return False, None

        return admin_db.authenticate_admin(identifier, password)

    @staticmethod
    def validate_input(identifier: str, password: str) -> Tuple[bool, str]:
        """
        Validate login input fields

        Args:
            identifier: Admin ID or Email
            password: Password

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not identifier.strip():
            return False, "Admin ID or Email is required"
        if not password.strip():
            return False, "Password is required"
        return True, ""