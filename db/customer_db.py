# customer_db.py
import mysql.connector
from mysql.connector import Error
import hashlib


class CustomerDB:
    """Simple database manager for customer accounts"""

    def __init__(self):
        self.host = 'localhost'
        self.database = 'food_dash_db'  # Changed to unified database
        self.user = 'root'
        self.password = ''  # XAMPP default

    def get_connection(self):
        """Get database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def connect(self):
        """Alternative connection method for consistency"""
        return self.get_connection()

    def disconnect(self):
        """For compatibility with existing code patterns"""
        pass  # Connection is closed in each method

    def hash_password(self, password):
        """Hash password using SHA-256"""
        salt = "food_dash_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def create_customer(self, full_name, email, phone, address, password):
        """Create a new customer account"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # Check if email exists
            check_query = "SELECT id FROM customers WHERE email = %s"
            cursor.execute(check_query, (email,))
            if cursor.fetchone():
                return False, "Email already registered"

            # Hash password
            hashed_password = self.hash_password(password)

            # Insert customer
            insert_query = """
            INSERT INTO customers (full_name, email, phone, address, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            customer_data = (full_name, email, phone, address, hashed_password)

            cursor.execute(insert_query, customer_data)
            connection.commit()

            customer_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return True, f"Account created successfully! Customer ID: {customer_id}"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def get_customer_info(self, customer_id):
        """Get complete customer information by ID"""
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT id, full_name, email, phone, address FROM customers WHERE id = %s"
            cursor.execute(query, (customer_id,))
            customer = cursor.fetchone()

            cursor.close()
            connection.close()

            return customer

        except Error as e:
            print(f"Error getting customer info: {e}")
            return None

    def authenticate_customer(self, email, password):
        """Check if email and password match - return FULL customer info"""
        connection = self.get_connection()
        if connection is None:
            return False, None

        try:
            cursor = connection.cursor(dictionary=True)

            # Get customer by email
            query = "SELECT * FROM customers WHERE email = %s"
            cursor.execute(query, (email,))
            customer = cursor.fetchone()

            cursor.close()
            connection.close()

            if customer:
                # Verify password
                hashed_input = self.hash_password(password)
                if customer['password'] == hashed_input:
                    # Remove password from returned data
                    customer.pop('password', None)
                    return True, customer

            return False, None

        except Error as e:
            print(f"Authentication error: {e}")
            return False, None

    def test_connection(self):
        """Test database connection"""
        try:
            connection = self.get_connection()
            if connection and connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                connection.close()

                if result and result[0] == 1:
                    return True, "Database connection successful"

            return False, "Cannot connect to database"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def update_customer_address(self, customer_id, new_address):
        """Update customer's address in database"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            update_query = "UPDATE customers SET address = %s WHERE id = %s"
            cursor.execute(update_query, (new_address, customer_id))
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Address updated successfully"
            else:
                return False, "Customer not found"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def get_customer_address(self, customer_id):
        """Get customer's address from database"""
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT address FROM customers WHERE id = %s"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result:
                return result['address']
            return None

        except Error as e:
            print(f"Error getting customer address: {e}")
            return None

    def get_all_customers(self):
        """Get all customers (for admin purposes)"""
        connection = self.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT id, full_name, email, phone, address, created_at FROM customers ORDER BY id DESC"
            cursor.execute(query)
            customers = cursor.fetchall()

            cursor.close()
            connection.close()

            return customers

        except Error as e:
            print(f"Error getting all customers: {e}")
            return []

    def update_customer(self, customer_id, full_name, email, phone, address, password=None):
        """Update customer information in database"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # Check if customer exists
            check_query = "SELECT id FROM customers WHERE id = %s"
            cursor.execute(check_query, (customer_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Customer not found"

            # Check if email already exists for another customer
            check_email_query = "SELECT id FROM customers WHERE email = %s AND id != %s"
            cursor.execute(check_email_query, (email, customer_id))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Email already registered by another user"

            if password:
                # Hash the new password
                hashed_password = self.hash_password(password)

                update_query = """
                UPDATE customers 
                SET full_name = %s, email = %s, phone = %s, address = %s, password = %s 
                WHERE id = %s
                """
                values = (full_name, email, phone, address, hashed_password, customer_id)
            else:
                # Don't update password
                update_query = """
                UPDATE customers 
                SET full_name = %s, email = %s, phone = %s, address = %s 
                WHERE id = %s
                """
                values = (full_name, email, phone, address, customer_id)

            cursor.execute(update_query, values)
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Customer updated successfully"
            else:
                return False, "No changes made"

        except Error as e:
            print(f"Error updating customer: {e}")
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        except Exception as e:
            print(f"Unexpected error updating customer: {e}")
            return False, f"Unexpected error: {str(e)}"

    def delete_customer(self, customer_id):
        """Delete a customer from database"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # First check if customer exists
            check_query = "SELECT id FROM customers WHERE id = %s"
            cursor.execute(check_query, (customer_id,))
            customer = cursor.fetchone()

            if not customer:
                cursor.close()
                connection.close()
                return False, "Customer not found"

            # Delete the customer
            delete_query = "DELETE FROM customers WHERE id = %s"
            cursor.execute(delete_query, (customer_id,))
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Customer deleted successfully"
            else:
                return False, "Failed to delete customer"

        except Error as e:
            print(f"Error deleting customer: {e}")
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        except Exception as e:
            print(f"Unexpected error deleting customer: {e}")
            return False, f"Unexpected error: {str(e)}"


# Create a global instance for easy access
customer_db = CustomerDB()