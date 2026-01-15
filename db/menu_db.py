# menu_db.py
import mysql.connector
from mysql.connector import Error


class MenuDB:
    """Database manager for menu items"""

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

    def create_menu_item(self, name, description, category, price, image_url="picture/default.png"):
        """Create a new menu item"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO menu_items (name, description, category, price, image_url)
            VALUES (%s, %s, %s, %s, %s)
            """
            menu_data = (name, description, category, price, image_url)

            cursor.execute(insert_query, menu_data)
            connection.commit()

            item_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return True, f"Menu item created successfully! ID: {item_id}"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def get_all_menu_items(self):
        """Get all menu items"""
        connection = self.get_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM menu_items ORDER BY id DESC"
            cursor.execute(query)
            menu_items = cursor.fetchall()

            cursor.close()
            connection.close()

            return menu_items

        except Error as e:
            print(f"Error getting menu items: {e}")
            return []

    def get_menu_item_by_id(self, item_id):
        """Get menu item by ID"""
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM menu_items WHERE id = %s"
            cursor.execute(query, (item_id,))
            menu_item = cursor.fetchone()

            cursor.close()
            connection.close()

            return menu_item

        except Error as e:
            print(f"Error getting menu item: {e}")
            return None

    def update_menu_item(self, item_id, name=None, description=None, category=None, price=None, image_url=None):
        """Update menu item information"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            # Build dynamic update query
            updates = []
            values = []

            if name:
                updates.append("name = %s")
                values.append(name)
            if description:
                updates.append("description = %s")
                values.append(description)
            if category:
                updates.append("category = %s")
                values.append(category)
            if price:
                updates.append("price = %s")
                values.append(price)
            if image_url:
                updates.append("image_url = %s")
                values.append(image_url)

            if not updates:
                return False, "No updates provided"

            # Add item_id to values
            values.append(item_id)

            update_query = f"UPDATE menu_items SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(update_query, values)
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Menu item updated successfully"
            else:
                return False, "Menu item not found"

        except Error as e:
            return False, f"Database error: {str(e)}"

    def delete_menu_item(self, item_id):
        """Delete menu item by ID"""
        connection = self.get_connection()
        if connection is None:
            return False, "Cannot connect to database"

        try:
            cursor = connection.cursor()

            delete_query = "DELETE FROM menu_items WHERE id = %s"
            cursor.execute(delete_query, (item_id,))
            connection.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()

            if affected_rows > 0:
                return True, "Menu item deleted successfully"
            else:
                return False, "Menu item not found"

        except Error as e:
            return False, f"Database error: {str(e)}"

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


# Global instance
menu_db = MenuDB()