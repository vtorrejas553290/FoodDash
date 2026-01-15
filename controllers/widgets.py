# widgets.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QDialog, QLineEdit, QTextEdit, QComboBox, QDialogButtonBox,
    QScrollArea, QMessageBox, QTableWidgetItem
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta, date

# Import databases
from db.orders_db import orders_db_instance as orders_db
from db.activity_db import activity_db


class RevenueGraphWidget(QWidget):
    """Widget to display revenue line graph with year selector"""

    def __init__(self):
        super().__init__()

        # Create figure and canvas
        self.figure = Figure(figsize=(8, 3), dpi=80)
        self.canvas = FigureCanvas(self.figure)

        # Set up MONTHLY data
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Store data for multiple years
        self.yearly_data = {}  # Format: {year: [revenue_per_month]}
        self.current_year = datetime.now().year

        # Generate year list for past 5 years
        self.years = [str(self.current_year - i) for i in range(5)]

        # Initialize with current year data
        self.revenue = [0] * 12

        # Load initial data from database for current year
        self.load_monthly_data_from_db(self.current_year)

        # Create year selector combo box FIRST - MATCHING ORDER TRACKING DESIGN
        self.year_combo = QComboBox()
        self.year_combo.addItems(self.years)
        self.year_combo.setCurrentText(str(self.current_year))
        self.year_combo.setFixedHeight(40)  # Same height as order tracking
        self.year_combo.setMinimumWidth(150)  # Same minimum width
        self.year_combo.setStyleSheet("""
            QComboBox {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                min-width: 150px;
                color: black;
                background-color: white;
            }
            QComboBox:hover {
                border: 1px solid #a0a0a0;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: black;
                color: white;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
                selection-background-color: #5b7bff;
                selection-color: white;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                min-height: 36px;
                border-bottom: 1px solid #333;
            }
            QComboBox QAbstractItemView::item:last {
                border-bottom: none;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #333;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #5b7bff;
                color: white;
            }
        """)
        self.year_combo.currentTextChanged.connect(self.on_year_changed)

        # Create the plot AFTER creating year_combo
        self.create_plot()

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Create header with title, total revenue, and year selector
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)  # Space between elements

        # Graph title on the left
        title_label = QLabel("Monthly Revenue Trends")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: black;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Add total revenue display
        self.total_revenue_label = QLabel("Total: ₱0")
        self.total_revenue_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.total_revenue_label.setStyleSheet("color: #4F39F6; padding: 0 10px;")

        # Update total revenue for current year
        self.update_total_revenue_label()

        header_layout.addWidget(self.total_revenue_label)

        # Add year selector combo with label
        year_label = QLabel("Year:")
        year_label.setFont(QFont("Arial", 12))
        year_label.setStyleSheet("color: #666; margin-right: 8px;")

        header_layout.addWidget(year_label)
        header_layout.addWidget(self.year_combo)

        layout.addLayout(header_layout)
        layout.addWidget(self.canvas)

    def on_year_changed(self, year_str):
        """Handle year selection change"""
        try:
            year = int(year_str)
            # Check if data for this year is already loaded
            if year in self.yearly_data:
                self.revenue = self.yearly_data[year]
            else:
                # Load data for this year from database
                self.load_monthly_data_from_db(year)
                self.yearly_data[year] = self.revenue.copy()

            # Update the plot
            self.create_plot()
            self.canvas.draw()

            # Update total revenue label
            self.update_total_revenue_label()

        except ValueError:
            print(f"Invalid year selected: {year_str}")

    def update_total_revenue_label(self):
        """Update the total revenue label for the selected year"""
        try:
            if hasattr(self, 'year_combo') and self.year_combo.currentText():
                current_year = int(self.year_combo.currentText())
            else:
                current_year = self.current_year

            # Calculate total revenue for the selected year
            total_revenue = sum(self.revenue)
            self.total_revenue_label.setText(f"Total: ₱{total_revenue:,.2f}")
        except:
            self.total_revenue_label.setText("Total: ₱0")

    def load_monthly_data_from_db(self, year=None):
        """Load monthly revenue data from database for specific year"""
        try:
            if year is None:
                year = self.current_year

            print(f"Loading monthly data for year {year}...")
            # Initialize monthly revenue
            monthly_revenue = [0] * 12

            # Get orders from database
            success, orders = orders_db.get_all_orders()

            if success and orders:
                print(f"Found {len(orders)} orders total")
                completed_count = 0

                for order in orders:
                    status = order.get('status', '').lower()
                    if status == 'completed':
                        completed_count += 1
                        try:
                            order_date = order.get('created_at', '')
                            total_amount = float(order.get('total_amount', 0))

                            if order_date:
                                # Handle datetime object or string
                                from datetime import datetime

                                if isinstance(order_date, datetime):  # It's a datetime object
                                    month = order_date.month
                                    order_year = order_date.year
                                else:  # It's a string
                                    try:
                                        # Try different date formats
                                        if ' ' in str(order_date):
                                            date_str = str(order_date).split(' ')[0]
                                        elif 'T' in str(order_date):
                                            date_str = str(order_date).split('T')[0]
                                        else:
                                            date_str = str(order_date)

                                        # Parse the date
                                        if '-' in date_str:
                                            parts = date_str.split('-')
                                            if len(parts) >= 2:
                                                order_year = int(parts[0])
                                                month = int(parts[1])
                                            else:
                                                continue
                                        else:
                                            continue
                                    except:
                                        continue

                                # Only include orders from the specified year
                                if order_year == year:
                                    month_index = month - 1  # Convert to 0-based index
                                    if 0 <= month_index < 12:
                                        monthly_revenue[month_index] += total_amount
                        except Exception as e:
                            print(f"Error processing order: {e}")
                            continue

                print(f"Processed {completed_count} completed orders for year {year}")

            print(f"Monthly revenue data for {year}: {monthly_revenue}")

            # Update revenue data
            self.revenue = monthly_revenue
            # Store in yearly data cache
            self.yearly_data[year] = monthly_revenue.copy()

            # Update total revenue label
            if hasattr(self, 'total_revenue_label'):
                total_revenue = sum(monthly_revenue)
                self.total_revenue_label.setText(f"Total: ₱{total_revenue:,.2f}")

        except Exception as e:
            print(f"Error loading monthly data from DB for year {year}: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to sample data
            self.revenue = [0] * 12
            if hasattr(self, 'total_revenue_label'):
                self.total_revenue_label.setText("Total: ₱0")

    def create_plot(self):
        """Create or update the line graph"""
        self.figure.clear()

        ax = self.figure.add_subplot(111)

        # Get current year from combo box if it exists, otherwise use self.current_year
        if hasattr(self, 'year_combo') and self.year_combo.currentText():
            current_year = int(self.year_combo.currentText())
        else:
            current_year = self.current_year

        # Plot the line
        line = ax.plot(self.months, self.revenue, marker='o', linestyle='-',
                       color='#5b7bff', linewidth=2.5, markersize=8)

        # Fill under the line
        ax.fill_between(self.months, self.revenue, alpha=0.2, color='#5b7bff')

        # Set labels and title with current year
        ax.set_title(f'Monthly Revenue Trend - {current_year}', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Months', fontsize=12)
        ax.set_ylabel('Revenue (₱)', fontsize=12)

        # Add grid
        ax.grid(True, linestyle='--', alpha=0.3)

        # Add value labels on each point
        max_revenue = max(self.revenue) if self.revenue else 0
        for i, (month, rev) in enumerate(zip(self.months, self.revenue)):
            if rev > 0:  # Only show labels for non-zero values
                y_offset = max_revenue * 0.02 if max_revenue > 0 else 40
                ax.text(month, rev + y_offset,
                        f'₱{rev:,.0f}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold')

        # Set y-axis to start from 0
        ax.set_ylim(bottom=0)

        # Calculate y-axis maximum
        if max_revenue > 2500:
            # Set y-axis max to 30% above the maximum value for better visualization
            ax.set_ylim(top=max_revenue * 1.3)
            print(f"Revenue exceeds ₱2500. Max: ₱{max_revenue:,.2f}, Y-axis set to: ₱{max_revenue * 1.3:,.2f}")
        elif max_revenue > 0:
            # For smaller values, use 15% padding
            ax.set_ylim(top=max_revenue * 1.15)
        else:
            # If all zeros, set a default range
            ax.set_ylim(top=1000)

        # Style the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Adjust layout
        self.figure.tight_layout()

        # Draw the canvas
        self.canvas.draw()
        print(f"Graph plot created successfully for year {current_year}")

    def refresh(self):
        """Refresh the graph with latest data for current year"""
        print("Refreshing graph...")
        if hasattr(self, 'year_combo') and self.year_combo.currentText():
            current_year = int(self.year_combo.currentText())
        else:
            current_year = self.current_year
        self.load_monthly_data_from_db(current_year)
        self.create_plot()
        self.canvas.draw()
        print("Graph refresh complete")

    def update_monthly_data_from_db(self):
        """Update monthly data from database and refresh graph for all years"""
        print("Updating monthly data for all years...")
        # Clear yearly data cache
        self.yearly_data = {}

        # Reload data for all years
        current_year = datetime.now().year
        for year_offset in range(5):
            year = current_year - year_offset
            self.load_monthly_data_from_db(year)

        # Update combo box if current year has changed
        if current_year != self.current_year:
            self.current_year = current_year
            # Update years list
            self.years = [str(self.current_year - i) for i in range(5)]
            if hasattr(self, 'year_combo'):
                self.year_combo.clear()
                self.year_combo.addItems(self.years)
                self.year_combo.setCurrentText(str(self.current_year))

        # Refresh display
        self.refresh()

    def set_monthly_data(self):
        """Set the graph to display monthly data for current year"""
        if hasattr(self, 'year_combo') and self.year_combo.currentText():
            current_year = int(self.year_combo.currentText())
        else:
            current_year = self.current_year
        self.load_monthly_data_from_db(current_year)
        self.create_plot()

    def update_revenue(self, new_revenue_data=None):
        """Update the revenue graph with new data - KEPT FOR BACKWARD COMPATIBILITY"""
        if new_revenue_data:
            # Handle both monthly and weekly updates
            if len(new_revenue_data) == len(self.revenue):
                self.revenue = new_revenue_data
            else:
                # If data doesn't match monthly format, use as-is but ensure 12 months
                if len(new_revenue_data) < 12:
                    self.revenue = new_revenue_data + [0] * (12 - len(new_revenue_data))
                else:
                    self.revenue = new_revenue_data[:12]

        # Store in current year's data
        if hasattr(self, 'year_combo') and self.year_combo.currentText():
            current_year = int(self.year_combo.currentText())
        else:
            current_year = self.current_year
        self.yearly_data[current_year] = self.revenue.copy()

        # Update the plot
        self.create_plot()


class PopularItemsPieChartWidget(QWidget):
    """Widget to display pie chart of most popular ordered items"""

    def __init__(self):
        super().__init__()

        # Create figure and canvas
        self.figure = Figure(figsize=(8, 4), dpi=80)
        self.canvas = FigureCanvas(self.figure)

        # Initialize data
        self.item_data = {}
        self.item_counts = {}
        self.colors = []

        # Load initial data from database
        self.load_popular_items_from_db()

        # Create the pie chart
        self.create_pie_chart()

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def load_popular_items_from_db(self):
        """Load popular items data from completed orders"""
        try:
            # Get all completed orders
            success, orders = orders_db.get_all_orders()

            if not success:
                print("Failed to load orders for pie chart")
                return

            # Dictionary to store item counts
            item_counts = {}

            for order in orders:
                # Only count completed orders
                if order.get('status', '').lower() == 'completed':
                    items = order.get('items', [])

                    for item in items:
                        item_name = item.get('title', 'Unknown Item')
                        quantity = item.get('qty', 1)

                        if item_name in item_counts:
                            item_counts[item_name] += quantity
                        else:
                            item_counts[item_name] = quantity

            # Sort items by count in descending order
            sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)

            # Take top 10 items
            top_items = dict(sorted_items[:10])

            # Store data
            self.item_counts = top_items

            print(f"Loaded {len(top_items)} popular items from database")
            for item, count in top_items.items():
                print(f"  {item}: {count} orders")

        except Exception as e:
            print(f"Error loading popular items from DB: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to sample data
            self.item_counts = {
                "Classic Burger": 45,
                "Crispy Fries": 38,
                "Fried Chicken": 32,
                "Milk Tea": 28,
                "Pepperoni Pizza": 25,
                "Cheeseburger": 20,
                "Chicken Sandwich": 18,
                "Soft Drinks": 15,
                "Ice Cream": 12,
                "Salad": 8
            }

    def create_pie_chart(self):
        """Create or update the pie chart"""
        self.figure.clear()

        # Check if we have data
        if not self.item_counts:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No order data available',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=14)
            ax.set_axis_off()
            self.canvas.draw()
            return

        ax = self.figure.add_subplot(111)

        # Prepare data for pie chart
        labels = list(self.item_counts.keys())
        sizes = list(self.item_counts.values())

        # Generate colors - using a vibrant color palette
        color_palette = ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2',
                         '#EF476F', '#FF9A76', '#7BC950', '#9D4EDD', '#FF9F1C']

        # If we have more items than colors, generate more colors
        if len(labels) > len(color_palette):
            import colorsys
            for i in range(len(labels) - len(color_palette)):
                hue = i / len(labels)
                rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                color_palette.append('#{:02x}{:02x}{:02x}'.format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))

        self.colors = color_palette[:len(labels)]

        # Create pie chart with explosion effect for the largest slice
        if sizes:
            max_index = sizes.index(max(sizes))
            explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]
        else:
            explode = [0] * len(sizes)

        # Plot the pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=self.colors,
                                          autopct='%1.1f%%', startangle=90,
                                          explode=explode, shadow=True,
                                          textprops={'fontsize': 10, 'fontweight': 'bold'})

        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Add title
        ax.set_title('Top Ordered Items Distribution', fontsize=16, fontweight='bold', pad=20)

        # Add legend
        legend_labels = [f'{label} ({count} orders)' for label, count in zip(labels, sizes)]
        ax.legend(wedges, legend_labels, title="Menu Items",
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

        # Adjust layout to make room for legend
        self.figure.tight_layout(rect=[0, 0, 0.75, 1])

        # Draw the canvas
        self.canvas.draw()

    def refresh(self):
        """Refresh the pie chart with latest data"""
        print("Refreshing pie chart...")
        self.load_popular_items_from_db()
        self.create_pie_chart()
        self.canvas.draw()
        print("Pie chart refresh complete")

    def update_chart(self):
        """Update the pie chart data"""
        self.refresh()


class AddUserDialog(QDialog):
    """Dialog for adding new users (Staff or Customer) - Scrollable with Show/Hide Password"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.setFixedSize(500, 550)  # More reasonable size
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 13px;
                font-weight: bold;
                padding: 3px 0px;
            }
            QLineEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                min-height: 38px;
            }
            QLineEdit:focus {
                border: 1px solid #5b7bff;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        self.user_data = None

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                border-radius: 5px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Create scroll content widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(12)  # Reasonable spacing

        # Title
        title_label = QLabel("Add New User")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #5b7bff; margin-bottom: 8px; padding: 5px 0px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        scroll_layout.addSpacing(5)

        # Full Name
        fullname_label = QLabel("Full Name:")
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        self.fullname_input.setMinimumHeight(38)
        scroll_layout.addWidget(fullname_label)
        scroll_layout.addWidget(self.fullname_input)
        scroll_layout.addSpacing(3)

        # Email
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(38)
        scroll_layout.addWidget(email_label)
        scroll_layout.addWidget(self.email_input)
        scroll_layout.addSpacing(3)

        # Phone
        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setMinimumHeight(38)
        scroll_layout.addWidget(phone_label)
        scroll_layout.addWidget(self.phone_input)
        scroll_layout.addSpacing(3)

        # Address
        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setMinimumHeight(38)
        scroll_layout.addWidget(address_label)
        scroll_layout.addWidget(self.address_input)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # PASSWORD + SHOW/HIDE BUTTON
        # -----------------------------------------------------------
        password_label = QLabel("Password:")
        scroll_layout.addWidget(password_label)

        # Password row with show/hide button
        password_row = QHBoxLayout()
        password_row.setSpacing(8)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password (min 8 characters)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(38)
        password_row.addWidget(self.password_input)

        # Show/hide password button
        self.show_pass_btn = QPushButton()
        self.show_pass_btn.setCheckable(True)
        self.show_pass_btn.setFixedSize(38, 38)
        self.show_pass_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d0ced7;
                background-color: #f9fafc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
            }
        """)

        # Try to load icons, fall back to text if icons not available
        try:
            hide_icon = QIcon("picture/hide.png")
            show_icon = QIcon("picture/show.png")
            if not hide_icon.isNull() and not show_icon.isNull():
                self.show_pass_btn.setIcon(hide_icon)
                self.show_pass_btn.setIconSize(QSize(18, 18))
                self.has_icons = True
            else:
                self.has_icons = False
                self.show_pass_btn.setText("👁")
                self.show_pass_btn.setFont(QFont("Arial", 12))
        except:
            self.has_icons = False
            self.show_pass_btn.setText("👁")
            self.show_pass_btn.setFont(QFont("Arial", 12))

        self.show_pass_btn.toggled.connect(self.toggle_password_visibility)
        password_row.addWidget(self.show_pass_btn)

        scroll_layout.addLayout(password_row)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # CONFIRM PASSWORD + SHOW/HIDE BUTTON
        # -----------------------------------------------------------
        confirm_label = QLabel("Confirm Password:")
        scroll_layout.addWidget(confirm_label)

        # Confirm password row with show/hide button
        confirm_row = QHBoxLayout()
        confirm_row.setSpacing(8)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setMinimumHeight(38)
        confirm_row.addWidget(self.confirm_input)

        # Show/hide confirm password button
        self.show_confirm_btn = QPushButton()
        self.show_confirm_btn.setCheckable(True)
        self.show_confirm_btn.setFixedSize(38, 38)
        self.show_confirm_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d0ced7;
                background-color: #f9fafc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
            }
        """)

        # Try to load icons for confirm button
        if self.has_icons:
            try:
                self.show_confirm_btn.setIcon(QIcon("picture/show.png"))
                self.show_confirm_btn.setIconSize(QSize(18, 18))
            except:
                self.show_confirm_btn.setText("👁")
                self.show_confirm_btn.setFont(QFont("Arial", 12))
        else:
            self.show_confirm_btn.setText("👁")
            self.show_confirm_btn.setFont(QFont("Arial", 12))

        self.show_confirm_btn.toggled.connect(self.toggle_confirm_visibility)
        confirm_row.addWidget(self.show_confirm_btn)

        scroll_layout.addLayout(confirm_row)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # USER TYPE SELECTION
        # -----------------------------------------------------------
        role_label = QLabel("User Type:")
        scroll_layout.addWidget(role_label)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Customer", "Staff"])
        self.role_combo.setMinimumHeight(38)
        self.role_combo.setStyleSheet("""
            QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                min-height: 38px;
            }
            QComboBox:hover {
                border: 1px solid #a0a0a0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #d0ced7;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #f9fafc;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #f3f0ff;
                selection-color: black;
                font-size: 13px;
                padding: 8px;
                border: 1px solid #d0ced7;
                border-radius: 6px;
                margin-top: 3px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                min-height: 32px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f3f0ff;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #5b7bff;
                color: white;
            }
        """)
        scroll_layout.addWidget(self.role_combo)
        scroll_layout.addSpacing(8)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            color: #e53e3e; 
            font-size: 12px; 
            padding: 8px; 
            background-color: #fed7d7; 
            border-radius: 6px;
            border: 1px solid #fc8181;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        scroll_layout.addWidget(self.error_label)

        # Add stretch to push content up
        scroll_layout.addStretch()

        # Set the scroll content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Buttons (outside scroll area, fixed at bottom)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        # Style both buttons
        button_box.setStyleSheet("""
            QDialogButtonBox {
                padding: 12px;
                border-top: 1px solid #e0e0e0;
                background-color: white;
            }
        """)

        # Style the OK button
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedHeight(40)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #5b7bff;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 90px;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4a6aff;
            }
            QPushButton:pressed {
                background-color: #3a5af0;
            }
        """)

        # Style the Cancel button
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setFixedHeight(40)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                font-weight: bold;
                font-size: 13px;
                min-width: 90px;
                border-radius: 8px;
                padding: 8px 16px;
                border: 1px solid #d1d5db;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)

        main_layout.addWidget(button_box)

    def toggle_password_visibility(self, checked):
        """Toggle password field visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.has_icons:
                self.show_pass_btn.setIcon(QIcon("picture/show.png"))
            else:
                self.show_pass_btn.setText("🙈")
                self.show_pass_btn.setFont(QFont("Arial", 12))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            if self.has_icons:
                self.show_pass_btn.setIcon(QIcon("picture/hide.png"))
            else:
                self.show_pass_btn.setText("👁")
                self.show_pass_btn.setFont(QFont("Arial", 12))

    def toggle_confirm_visibility(self, checked):
        """Toggle confirm password field visibility"""
        if checked:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.has_icons:
                self.show_confirm_btn.setIcon(QIcon("picture/show.png"))
            else:
                self.show_confirm_btn.setText("🙈")
                self.show_confirm_btn.setFont(QFont("Arial", 12))
        else:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            if self.has_icons:
                self.show_confirm_btn.setIcon(QIcon("picture/hide.png"))
            else:
                self.show_confirm_btn.setText("👁")
                self.show_confirm_btn.setFont(QFont("Arial", 12))

    def validate_and_accept(self):
        """Validate inputs before accepting"""
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        role = self.role_combo.currentText()

        # Show error label
        self.error_label.setVisible(True)

        # Check all fields are filled
        if not all([fullname, email, phone, address, password, confirm]):
            self.error_label.setText("❌ Please fill in all fields.")
            return

        # Validate email
        if "@" not in email or "." not in email:
            self.error_label.setText("❌ Please enter a valid email address.")
            return

        # Validate phone (basic)
        if not phone.replace(" ", "").replace("-", "").isdigit():
            self.error_label.setText("❌ Phone number should contain only digits.")
            return

        # Validate password
        if len(password) < 8:
            self.error_label.setText("❌ Password must be at least 8 characters long.")
            return

        # Check password match
        if password != confirm:
            self.error_label.setText("❌ Passwords do not match.")
            return

        # All validation passed
        self.user_data = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password,
            "role": role
        }
        self.accept()

    def get_user_data(self):
        """Return the collected user data"""
        return self.user_data


class EditUserDialog(QDialog):
    """Dialog for editing existing users (Staff or Customer)"""

    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit User")
        self.setFixedSize(500, 550)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 13px;
                font-weight: bold;
                padding: 3px 0px;
            }
            QLineEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                min-height: 38px;
            }
            QLineEdit:focus {
                border: 1px solid #5b7bff;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        self.user_data = None
        self.original_user_data = user_data

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                border-radius: 5px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Create scroll content widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(12)

        # Title
        title_label = QLabel("Edit User")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #5b7bff; margin-bottom: 8px; padding: 5px 0px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        scroll_layout.addSpacing(5)

        # Full Name
        fullname_label = QLabel("Full Name:")
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        self.fullname_input.setMinimumHeight(38)
        if user_data:
            self.fullname_input.setText(user_data.get('name', ''))
        scroll_layout.addWidget(fullname_label)
        scroll_layout.addWidget(self.fullname_input)
        scroll_layout.addSpacing(3)

        # Email
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(38)
        if user_data:
            self.email_input.setText(user_data.get('email', ''))
        scroll_layout.addWidget(email_label)
        scroll_layout.addWidget(self.email_input)
        scroll_layout.addSpacing(3)

        # Phone
        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setMinimumHeight(38)
        if user_data:
            self.phone_input.setText(user_data.get('phone', ''))
        scroll_layout.addWidget(phone_label)
        scroll_layout.addWidget(self.phone_input)
        scroll_layout.addSpacing(3)

        # Address
        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setMinimumHeight(38)
        if user_data:
            self.address_input.setText(user_data.get('address', ''))
        scroll_layout.addWidget(address_label)
        scroll_layout.addWidget(self.address_input)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # PASSWORD + SHOW/HIDE BUTTON (optional - only if changing password)
        # -----------------------------------------------------------
        password_label = QLabel("New Password (leave blank to keep current):")
        scroll_layout.addWidget(password_label)

        # Password row with show/hide button
        password_row = QHBoxLayout()
        password_row.setSpacing(8)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password (min 8 characters)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(38)
        password_row.addWidget(self.password_input)

        # Show/hide password button
        self.show_pass_btn = QPushButton()
        self.show_pass_btn.setCheckable(True)
        self.show_pass_btn.setFixedSize(38, 38)
        self.show_pass_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d0ced7;
                background-color: #f9fafc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
            }
        """)

        # Try to load icons, fall back to text if icons not available
        try:
            hide_icon = QIcon("picture/hide.png")
            show_icon = QIcon("picture/show.png")
            if not hide_icon.isNull() and not show_icon.isNull():
                self.show_pass_btn.setIcon(hide_icon)
                self.show_pass_btn.setIconSize(QSize(18, 18))
                self.has_icons = True
            else:
                self.has_icons = False
                self.show_pass_btn.setText("👁")
                self.show_pass_btn.setFont(QFont("Arial", 12))
        except:
            self.has_icons = False
            self.show_pass_btn.setText("👁")
            self.show_pass_btn.setFont(QFont("Arial", 12))

        self.show_pass_btn.toggled.connect(self.toggle_password_visibility)
        password_row.addWidget(self.show_pass_btn)

        scroll_layout.addLayout(password_row)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # CONFIRM PASSWORD + SHOW/HIDE BUTTON
        # -----------------------------------------------------------
        confirm_label = QLabel("Confirm New Password:")
        scroll_layout.addWidget(confirm_label)

        # Confirm password row with show/hide button
        confirm_row = QHBoxLayout()
        confirm_row.setSpacing(8)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm new password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setMinimumHeight(38)
        confirm_row.addWidget(self.confirm_input)

        # Show/hide confirm password button
        self.show_confirm_btn = QPushButton()
        self.show_confirm_btn.setCheckable(True)
        self.show_confirm_btn.setFixedSize(38, 38)
        self.show_confirm_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #d0ced7;
                background-color: #f9fafc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
            }
        """)

        # Try to load icons for confirm button
        if self.has_icons:
            try:
                self.show_confirm_btn.setIcon(QIcon("picture/hide.png"))
                self.show_confirm_btn.setIconSize(QSize(18, 18))
            except:
                self.show_confirm_btn.setText("👁")
                self.show_confirm_btn.setFont(QFont("Arial", 12))
        else:
            self.show_confirm_btn.setText("👁")
            self.show_confirm_btn.setFont(QFont("Arial", 12))

        self.show_confirm_btn.toggled.connect(self.toggle_confirm_visibility)
        confirm_row.addWidget(self.show_confirm_btn)

        scroll_layout.addLayout(confirm_row)
        scroll_layout.addSpacing(3)

        # -----------------------------------------------------------
        # USER TYPE SELECTION (read-only for editing)
        # -----------------------------------------------------------
        role_label = QLabel("User Type:")
        scroll_layout.addWidget(role_label)

        self.role_label_display = QLabel()
        self.role_label_display.setFont(QFont("Arial", 13))
        self.role_label_display.setStyleSheet("color: black; padding: 8px; background: #f8f9fa; border-radius: 6px;")
        if user_data:
            self.role_label_display.setText(user_data.get('role', 'User'))
        scroll_layout.addWidget(self.role_label_display)
        scroll_layout.addSpacing(8)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            color: #e53e3e; 
            font-size: 12px; 
            padding: 8px; 
            background-color: #fed7d7; 
            border-radius: 6px;
            border: 1px solid #fc8181;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        scroll_layout.addWidget(self.error_label)

        # Add stretch to push content up
        scroll_layout.addStretch()

        # Set the scroll content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Buttons (outside scroll area, fixed at bottom)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        # Style both buttons
        button_box.setStyleSheet("""
            QDialogButtonBox {
                padding: 12px;
                border-top: 1px solid #e0e0e0;
                background-color: white;
            }
        """)

        # Style the OK button
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setFixedHeight(40)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #5b7bff;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 90px;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4a6aff;
            }
            QPushButton:pressed {
                background-color: #3a5af0;
            }
        """)

        # Style the Cancel button
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setFixedHeight(40)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                font-weight: bold;
                font-size: 13px;
                min-width: 90px;
                border-radius: 8px;
                padding: 8px 16px;
                border: 1px solid #d1d5db;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
        """)

        main_layout.addWidget(button_box)

    def toggle_password_visibility(self, checked):
        """Toggle password field visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.has_icons:
                self.show_pass_btn.setIcon(QIcon("picture/show.png"))
            else:
                self.show_pass_btn.setText("🙈")
                self.show_pass_btn.setFont(QFont("Arial", 12))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            if self.has_icons:
                self.show_pass_btn.setIcon(QIcon("picture/hide.png"))
            else:
                self.show_pass_btn.setText("👁")
                self.show_pass_btn.setFont(QFont("Arial", 12))

    def toggle_confirm_visibility(self, checked):
        """Toggle confirm password field visibility"""
        if checked:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.has_icons:
                self.show_confirm_btn.setIcon(QIcon("picture/show.png"))
            else:
                self.show_confirm_btn.setText("🙈")
                self.show_confirm_btn.setFont(QFont("Arial", 12))
        else:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            if self.has_icons:
                self.show_confirm_btn.setIcon(QIcon("picture/hide.png"))
            else:
                self.show_confirm_btn.setText("👁")
                self.show_confirm_btn.setFont(QFont("Arial", 12))

    def validate_and_accept(self):
        """Validate inputs before accepting"""
        fullname = self.fullname_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        user_type = self.role_label_display.text()

        # Show error label
        self.error_label.setVisible(True)

        # Check required fields are filled
        if not all([fullname, email, phone, address]):
            self.error_label.setText("❌ Please fill in all required fields.")
            return

        # Validate email
        if "@" not in email or "." not in email:
            self.error_label.setText("❌ Please enter a valid email address.")
            return

        # Validate phone (basic)
        if not phone.replace(" ", "").replace("-", "").isdigit():
            self.error_label.setText("❌ Phone number should contain only digits.")
            return

        # If password is provided, validate it
        if password:
            if len(password) < 8:
                self.error_label.setText("❌ Password must be at least 8 characters long.")
                return

            # Check password match if password is provided
            if password != confirm:
                self.error_label.setText("❌ Passwords do not match.")
                return

        # All validation passed
        self.user_data = {
            "original_data": self.original_user_data,
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password if password else None,  # Only include if changed
            "role": user_type
        }
        self.accept()

    def get_user_data(self):
        """Return the collected user data"""
        return self.user_data


class AnalyticsCard(QFrame):
    def __init__(self, title, value, icon_bg="#eaf2ff", icon_path=""):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 14px;
            }
        """)

        self.setFixedHeight(140)

        # Create icon container
        icon_container = QWidget()
        icon_container.setFixedSize(44, 44)

        # Create the icon label
        icon_label = QLabel()
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Try to load the icon image if provided
        pixmap_loaded = False
        if icon_path:
            try:
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(pixmap)
                    pixmap_loaded = True
            except:
                pass

        # If no icon loaded, set background color
        if not pixmap_loaded:
            icon_label.setStyleSheet(f"""
                QLabel {{
                    background: {icon_bg};
                    border-radius: 10px;
                }}
            """)
        else:
            icon_label.setStyleSheet(f"""
                QLabel {{
                    background: {icon_bg};
                    border-radius: 10px;
                }}
            """)

        title_label = QLabel(title)
        title_label.setStyleSheet("color:#6b7280; font-size:14px;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        value_label.setStyleSheet("color:#111827;")

        v = QVBoxLayout()
        v.addWidget(title_label)
        v.addWidget(value_label)
        v.setSpacing(5)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(v)
        layout.addStretch()

    def update_value(self, new_value):
        """Update the card's value"""
        # Find and update the value label
        vbox = self.layout().itemAt(1).layout()
        if vbox:
            value_label = vbox.itemAt(1).widget()
            if value_label:
                value_label.setText(new_value)