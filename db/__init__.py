"""
Database Package
Contains all database operations for the application
"""
from .customer_db import customer_db
from .staff_db import staff_db
from .admin_db import admin_db

__all__ = ['customer_db', 'staff_db', 'admin_db']