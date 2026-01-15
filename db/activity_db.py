# activity_db.py
from datetime import datetime, timedelta

import mysql.connector
from mysql.connector import Error


class ActivityDB:
    """Database manager for activity logs"""

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
            print(f"Activity DB connection error: {e}")
            return None

    def create_table(self):
        """Create activity_logs table if it doesn't exist"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    staff_name VARCHAR(100) NOT NULL,
                    staff_id VARCHAR(20) NOT NULL,
                    action VARCHAR(255) NOT NULL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_staff_name (staff_name),
                    INDEX idx_staff_id (staff_id),
                    INDEX idx_created_at (created_at)
                )
            """)
            connection.commit()

            cursor.close()
            connection.close()
            return True, "Activity logs table created/verified"

        except Error as e:
            print(f"Error creating activity table: {e}")
            return False, f"Database error: {str(e)}"

    def get_activities_by_date_range(self, start_date, end_date):
        """Get activities within a date range"""
        try:
            query = """
                SELECT * FROM activity_logs 
                WHERE DATE(created_at) BETWEEN %s AND %s 
                ORDER BY created_at DESC
            """
            self.cursor.execute(query, (start_date, end_date))
            activities = self.cursor.fetchall()

            # Convert to list of dictionaries
            result = []
            for activity in activities:
                result.append({
                    'id': activity[0],
                    'staff_name': activity[1],
                    'staff_id': activity[2],
                    'action': activity[3],
                    'details': activity[4],
                    'created_at': activity[5]
                })
            return True, result
        except Exception as e:
            print(f"Error getting activities by date range: {e}")
            return False, str(e)

    def get_todays_activities(self):
        """Get today's activities"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            query = """
                SELECT * FROM activity_logs 
                WHERE DATE(created_at) = %s 
                ORDER BY created_at DESC
            """
            self.cursor.execute(query, (today,))
            activities = self.cursor.fetchall()

            # Convert to list of dictionaries
            result = []
            for activity in activities:
                result.append({
                    'id': activity[0],
                    'staff_name': activity[1],
                    'staff_id': activity[2],
                    'action': activity[3],
                    'details': activity[4],
                    'created_at': activity[5]
                })
            return True, result
        except Exception as e:
            print(f"Error getting today's activities: {e}")
            return False, str(e)

    def get_activities_last_n_days(self, days):
        """Get activities from the last N days"""
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days - 1)).strftime("%Y-%m-%d")
            query = """
                SELECT * FROM activity_logs 
                WHERE DATE(created_at) BETWEEN %s AND %s 
                ORDER BY created_at DESC
            """
            self.cursor.execute(query, (start_date, end_date))
            activities = self.cursor.fetchall()

            # Convert to list of dictionaries
            result = []
            for activity in activities:
                result.append({
                    'id': activity[0],
                    'staff_name': activity[1],
                    'staff_id': activity[2],
                    'action': activity[3],
                    'details': activity[4],
                    'created_at': activity[5]
                })
            return True, result
        except Exception as e:
            print(f"Error getting activities for last {days} days: {e}")
            return False, str(e)
    def add_activity(self, staff_name, staff_id, action, details=""):
        """Add a new activity log"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO activity_logs (staff_name, staff_id, action, details)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(insert_query, (staff_name, staff_id, action, details))
            connection.commit()

            cursor.close()
            connection.close()
            return True, "Activity logged successfully"

        except Error as e:
            print(f"Error adding activity: {e}")
            return False, f"Database error: {str(e)}"

    def get_all_activities(self, limit=100):
        """Get all activities"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT * FROM activity_logs 
            ORDER BY created_at DESC 
            LIMIT %s
            """

            cursor.execute(query, (limit,))
            activities = cursor.fetchall()

            cursor.close()
            connection.close()
            return True, activities

        except Error as e:
            print(f"Error getting activities: {e}")
            return False, f"Database error: {str(e)}"

    def search_activities(self, search_term, limit=50):
        """Search activities by staff name, action, or details"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT * FROM activity_logs 
            WHERE staff_name LIKE %s 
               OR action LIKE %s 
               OR details LIKE %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """

            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, limit))
            activities = cursor.fetchall()

            cursor.close()
            connection.close()
            return True, activities

        except Error as e:
            print(f"Error searching activities: {e}")
            return False, f"Database error: {str(e)}"

    def clear_all_activities(self):
        """Clear all activity logs (admin only)"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            query = "DELETE FROM activity_logs"
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()
            return True, "All activity logs cleared"

        except Error as e:
            print(f"Error clearing activities: {e}")
            return False, f"Database error: {str(e)}"

    def get_total_count(self):
        """Get total count of activity logs"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            query = "SELECT COUNT(*) as count FROM activity_logs"
            cursor.execute(query)
            result = cursor.fetchone()

            cursor.close()
            connection.close()
            return True, result[0] if result else 0

        except Error as e:
            print(f"Error getting activity count: {e}")
            return False, f"Database error: {str(e)}"


# Create singleton instance
activity_db = ActivityDB()