"""
Customer Login Model
Handles customer authentication logic and data operations
"""
from typing import Optional, Dict, Tuple
from db.customer_db import customer_db


class CustomerLoginModel:
    """Model for customer login operations"""

    @staticmethod
    def authenticate(email: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """
        Authenticate customer credentials

        Args:
            email: Customer email
            password: Customer password

        Returns:
            Tuple of (success, customer_info)
        """
        if not email or not password:
            return False, None

        return customer_db.authenticate_customer(email, password)

    @staticmethod
    def get_customer_info(customer_id: int) -> Optional[Dict]:
        """
        Get customer information by ID

        Args:
            customer_id: Customer ID

        Returns:
            Customer information dictionary or None
        """
        return customer_db.get_customer_info(customer_id)

    @staticmethod
    def validate_input(email: str, password: str) -> Tuple[bool, str]:
        """
        Validate login input fields

        Args:
            email: Email input
            password: Password input

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email.strip():
            return False, "Email is required"
        if not password.strip():
            return False, "Password is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, ""