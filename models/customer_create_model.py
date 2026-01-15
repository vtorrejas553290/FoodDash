"""
Customer Create Account Model
Handles customer account creation logic and data operations
"""
from typing import Optional, Dict, Tuple
from db.customer_db import customer_db


class CustomerCreateModel:
    """Model for customer account creation operations"""

    @staticmethod
    def create_customer(full_name: str, email: str, phone: str,
                        address: str, password: str) -> Tuple[bool, str]:
        """
        Create a new customer account

        Args:
            full_name: Customer full name
            email: Customer email
            phone: Customer phone number
            address: Customer address
            password: Customer password

        Returns:
            Tuple of (success, message)
        """
        return customer_db.create_customer(full_name, email, phone, address, password)

    @staticmethod
    def validate_input(full_name: str, email: str, phone: str,
                       address: str, password: str, confirm_password: str) -> Tuple[bool, str, str]:
        """
        Validate all input fields

        Args:
            full_name: Customer full name
            email: Customer email
            phone: Customer phone number
            address: Customer address
            password: Customer password
            confirm_password: Confirmation password

        Returns:
            Tuple of (is_valid, field_name, error_message)
        """
        # Check all fields are filled
        if not all([full_name.strip(), email.strip(), phone.strip(),
                    address.strip(), password, confirm_password]):
            return False, "all", "All fields are required"

        # Validate email format
        if "@" not in email or "." not in email:
            return False, "email", "Invalid email format"

        # Validate phone number (basic check)
        if not phone.replace(" ", "").replace("-", "").isdigit():
            return False, "phone", "Phone number should contain only digits"

        # Validate password length
        if len(password) < 8:
            return False, "password", "Password must be at least 8 characters long"

        # Check password match
        if password != confirm_password:
            return False, "confirm", "Passwords do not match"

        return True, "", ""

    @staticmethod
    def test_connection() -> Tuple[bool, str]:
        """Test database connection"""
        return customer_db.test_connection()