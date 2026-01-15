# admin_db.py
import mysql.connector
from mysql.connector import Error
import hashlib


class AdminDB:
    """Database manager for admin accounts with admin_ prefixed attributes"""

    def __init__(self):
        self.host = 'localhost'
        self.database = 'food_dash_db'
        self.user = 'root'
        self.password = ''

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

    def hash_password(self, password):
        """Hash password using SHA-256"""
        salt = "food_dash_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def create_admin(self, admin_name, admin_email, admin_phone, admin_address, admin_password):
        """Create a new admin account"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            check_query = "SELECT admin_id FROM admins WHERE admin_email = %s"
            cursor.execute(check_query, (admin_email,))
            if cursor.fetchone():
                return False, "Email already registered"

            hashed_password = self.hash_password(admin_password)

            insert_query = """
            INSERT INTO admins (admin_name, admin_email, admin_phone, admin_address, admin_password)
            VALUES (%s, %s, %s, %s, %s)
            """
            admin_data = (admin_name, admin_email, admin_phone, admin_address, hashed_password)

            cursor.execute(insert_query, admin_data)
            connection.commit()

            admin_db_id = cursor.lastrowid
            admin_id = f"ADM{admin_db_id:05d}"

            update_query = "UPDATE admins SET admin_id = %s WHERE id = %s"
            cursor.execute(update_query, (admin_id, admin_db_id))
            connection.commit()

            cursor.close()
            connection.close()

            return True, f"Admin account created successfully! ID: {admin_id}"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def authenticate_admin(self, identifier, password):
        """Authenticate admin login using admin_id OR email and password"""
        connection = self.get_connection()
        if connection is None:
            return False, None

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM admins WHERE admin_id = %s OR admin_email = %s"
            cursor.execute(query, (identifier, identifier))
            admin = cursor.fetchone()

            cursor.close()
            connection.close()

            if admin:
                hashed_input = self.hash_password(password)
                if admin['admin_password'] == hashed_input:
                    admin.pop('admin_password', None)
                    return True, admin

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

    def get_admin_info(self, admin_id):
        """Get admin information by ID"""
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id, admin_id, admin_name, admin_email, admin_phone, admin_address, created_at 
            FROM admins WHERE admin_id = %s OR id = %s
            """
            cursor.execute(query, (admin_id, admin_id))
            admin = cursor.fetchone()

            cursor.close()
            connection.close()

            return admin

        except Error as e:
            print(f"Error getting admin info: {e}")
            return None

    def get_all_admins(self):
        """Get all admin accounts"""
        connection = self.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id, admin_id, admin_name, admin_email, admin_phone, admin_address, created_at 
            FROM admins ORDER BY id DESC
            """
            cursor.execute(query)
            admin_list = cursor.fetchall()

            cursor.close()
            connection.close()

            return admin_list

        except Error as e:
            print(f"Error getting all admins: {e}")
            return []


admin_db = AdminDB()