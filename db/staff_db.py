# staff_db.py
import mysql.connector
from mysql.connector import Error
import hashlib


class StaffDB:
    """Database manager for staff accounts"""

    def __init__(self):
        self.host = 'localhost'
        self.database = 'food_dash_db'  # Changed to unified database
        self.user = 'root'
        self.password = ''  # Default for XAMPP

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
        """For compatibility - use get_connection() instead"""
        return self.get_connection()

    def disconnect(self):
        """For compatibility - connections are closed in each method"""
        pass

    def hash_password(self, password):
        """Hash password using SHA-256"""
        salt = "food_dash_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def create_staff(self, staff_name, staff_email, staff_phone, staff_address, staff_password):
        """Create a new staff account"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # Check if email exists
            check_query = "SELECT id FROM staff WHERE staff_email = %s"
            cursor.execute(check_query, (staff_email,))
            if cursor.fetchone():
                return False, "Email already registered"

            # Hash password
            hashed_password = self.hash_password(staff_password)

            # Insert staff
            insert_query = """
            INSERT INTO staff (staff_name, staff_email, staff_phone, staff_address, staff_password)
            VALUES (%s, %s, %s, %s, %s)
            """
            staff_data = (staff_name, staff_email, staff_phone, staff_address, hashed_password)

            cursor.execute(insert_query, staff_data)
            connection.commit()

            staff_db_id = cursor.lastrowid
            staff_id = f"EMP{staff_db_id:05d}"

            # Update staff_id with EMP prefix
            update_query = "UPDATE staff SET staff_id = %s WHERE id = %s"
            cursor.execute(update_query, (staff_id, staff_db_id))
            connection.commit()

            cursor.close()
            connection.close()

            return True, f"Staff account created successfully! ID: {staff_id}"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def authenticate_staff(self, identifier, password):
        """Authenticate staff login using staff_id OR email and password"""
        connection = self.get_connection()
        if connection is None:
            return False, None

        try:
            cursor = connection.cursor(dictionary=True)

            # Try to find by staff_id OR email
            query = "SELECT * FROM staff WHERE staff_id = %s OR staff_email = %s"
            cursor.execute(query, (identifier, identifier))
            staff = cursor.fetchone()

            cursor.close()
            connection.close()

            if staff:
                hashed_input = self.hash_password(password)
                if staff['staff_password'] == hashed_input:
                    staff.pop('staff_password', None)  # Remove password before returning
                    return True, staff

            return False, None

        except Error as e:
            print(f"Error during authentication: {e}")
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

    def get_staff_info(self, staff_id):
        """Get staff information by ID"""
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id, staff_id, staff_name, staff_email, staff_phone, staff_address, role, created_at 
            FROM staff WHERE staff_id = %s OR id = %s
            """
            cursor.execute(query, (staff_id, staff_id))
            staff = cursor.fetchone()

            cursor.close()
            connection.close()

            return staff

        except Error as e:
            print(f"Error getting staff info: {e}")
            return None

    def get_all_staff(self):
        """Get all staff members"""
        connection = self.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id, staff_id, staff_name, staff_email, staff_phone, staff_address, role, created_at 
            FROM staff ORDER BY id DESC
            """
            cursor.execute(query)
            staff_list = cursor.fetchall()

            cursor.close()
            connection.close()

            return staff_list

        except Error as e:
            print(f"Error getting all staff: {e}")
            return []

    def update_staff_role(self, staff_id, new_role):
        """Update staff role"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            update_query = "UPDATE staff SET role = %s WHERE staff_id = %s"
            cursor.execute(update_query, (new_role, staff_id))
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, f"Staff role updated to {new_role}"
            else:
                return False, "Staff not found"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def update_staff(self, staff_id, staff_name, staff_email, staff_phone, staff_address, staff_password=None):
        """Update staff information in database"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # First check if staff exists
            check_query = "SELECT id FROM staff WHERE id = %s"
            cursor.execute(check_query, (staff_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Staff member not found"

            # Check if email already exists for another staff member
            check_email_query = "SELECT id FROM staff WHERE staff_email = %s AND id != %s"
            cursor.execute(check_email_query, (staff_email, staff_id))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Email already registered by another staff member"

            if staff_password:
                # Hash the new password
                hashed_password = self.hash_password(staff_password)

                update_query = """
                UPDATE staff 
                SET staff_name = %s, staff_email = %s, staff_phone = %s, staff_address = %s, staff_password = %s 
                WHERE id = %s
                """
                values = (staff_name, staff_email, staff_phone, staff_address, hashed_password, staff_id)
            else:
                # Don't update password
                update_query = """
                UPDATE staff 
                SET staff_name = %s, staff_email = %s, staff_phone = %s, staff_address = %s 
                WHERE id = %s
                """
                values = (staff_name, staff_email, staff_phone, staff_address, staff_id)

            cursor.execute(update_query, values)
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Staff member updated successfully"
            else:
                return False, "No changes made or staff not found"

        except Error as e:
            print(f"Error updating staff: {e}")
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        except Exception as e:
            print(f"Unexpected error updating staff: {e}")
            return False, f"Unexpected error: {str(e)}"

    def delete_staff(self, staff_id):
        """Delete a staff member from database"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # First check if staff exists
            check_query = "SELECT id FROM staff WHERE id = %s"
            cursor.execute(check_query, (staff_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "Staff member not found"

            # Delete the staff member
            delete_query = "DELETE FROM staff WHERE id = %s"
            cursor.execute(delete_query, (staff_id,))
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Staff member deleted successfully"
            else:
                return False, "Failed to delete staff member"

        except Error as e:
            print(f"Error deleting staff: {e}")
            if connection:
                connection.rollback()
            return False, f"Database error: {str(e)}"
        except Exception as e:
            print(f"Unexpected error deleting staff: {e}")
            return False, f"Unexpected error: {str(e)}"


# Global instance
staff_db = StaffDB()