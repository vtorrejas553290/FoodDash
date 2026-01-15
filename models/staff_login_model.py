"""
Staff Login Model
Handles staff authentication logic and data operations
"""
from typing import Optional, Dict, Tuple
from db.staff_db import staff_db


class StaffLoginModel:
    """Model for staff login operations"""

    @staticmethod
    def authenticate(identifier: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate staff credentials

        Args:
            identifier: Staff ID or Email
            password: Staff password

        Returns:
            Tuple of (success, staff_info)
        """
        if not identifier or not password:
            return False, None

        return staff_db.authenticate_staff(identifier, password)

    @staticmethod
    def validate_input(identifier: str, password: str) -> Tuple[bool, str]:
        """
        Validate login input fields

        Args:
            identifier: Staff ID or Email
            password: Password

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not identifier.strip():
            return False, "Staff ID or Email is required"
        if not password.strip():
            return False, "Password is required"
        return True, ""