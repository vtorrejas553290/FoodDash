# admin_dashboard_view.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView,
    QScrollArea, QStackedWidget, QMessageBox, QInputDialog, QFileDialog,
    QDialog, QLineEdit, QTextEdit, QComboBox, QDialogButtonBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from controllers.widgets import (
    RevenueGraphWidget,
    PopularItemsPieChartWidget,
    AddUserDialog,
    EditUserDialog,
    AnalyticsCard
)


class AdminDashboardView(QWidget):
    """View for Admin Dashboard - Handles all UI components"""

    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.resize(1350, 820)
        self.setStyleSheet("background-color: #f6f7fb;")

        # Initialize UI components
        self.revenue_graph = None
        self.pie_chart_widget = None
        self.total_revenue_card = None
        self.todays_orders_card = None
        self.pending_orders_card = None
        self.active_users_card = None
        self.refresh_btn = None
        self.search_input = None
        self.filter_combo = None
        self.month_filter_combo = None
        self.user_search_input = None
        self.user_filter_combo = None
        self.activity_search_input = None
        self.period_filter_combo = None
        self.activity_stats_label = None

        # Tab buttons
        self.overview_btn = None
        self.order_btn = None
        self.menu_btn = None
        self.user_btn = None
        self.activity_btn = None

        # Tables
        self.table = None
        self.user_table = None
        self.activity_table = None

        # Layout containers
        self.pages = None
        self.orders_layout = None
        self.orders_content = None
        self.scroll = None
        self.user_card_layout = None

        # Button references (for controller access)
        self.order_search_btn = None
        self.order_today_btn = None
        self.order_refresh_btn = None
        self.menu_add_btn = None
        self.user_add_btn = None
        self.user_search_btn = None
        self.user_refresh_btn = None
        self.activity_search_btn = None
        self.activity_today_btn = None
        self.activity_clear_btn = None
        self.activity_refresh_btn = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI"""
        main = QVBoxLayout()
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(18)

        # ----------------------------- TOP BAR -----------------------------
        top_bar = QHBoxLayout()
        top_bar.setSpacing(20)

        logo = QLabel()
        pix = QPixmap()
        try:
            pix = QPixmap("picture/logo.png")
        except:
            pass
        if not pix.isNull():
            pix = pix.scaled(55, 55, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            pix = QPixmap(55, 55)
            pix.fill(Qt.GlobalColor.purple)
        logo.setPixmap(pix)

        title_box = QVBoxLayout()
        self.title1 = QLabel("Admin Dashboard")
        self.title1.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title1.setStyleSheet("color: #4F39F6;")

        self.title2 = QLabel()
        self.title2.setFont(QFont("Arial", 11))
        self.title2.setStyleSheet("color: black;")

        title_box.addWidget(self.title1)
        title_box.addWidget(self.title2)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setFixedHeight(42)
        try:
            self.logout_btn.setIcon(QIcon("picture/logout.png"))
        except:
            pass
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 10px;
                padding: 8px 22px;
                border: 1px solid #d0ced7;
                color: black;
            }
            QPushButton:hover { background: #ececec; }
        """)

        top_bar.addWidget(logo)
        top_bar.addLayout(title_box)
        top_bar.addStretch()
        top_bar.addWidget(self.logout_btn)
        main.addLayout(top_bar)

        # ----------------------------- TABS -----------------------------
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(28)

        self.overview_btn = QPushButton("  Overview")
        try:
            self.overview_btn.setIcon(QIcon("picture/overview.png"))
        except:
            pass
        self.overview_btn.setIconSize(QSize(22, 22))
        self.overview_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #4F39F6;
                font-weight: bold;
            }
        """)

        self.order_btn = QPushButton("  Order Tracking")
        try:
            self.order_btn.setIcon(QIcon("picture/ordertracking.png"))
        except:
            pass
        self.order_btn.setIconSize(QSize(22, 22))
        self.order_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #444;
            }
            QPushButton:hover { color: #4F39F6; }
        """)

        self.menu_btn = QPushButton("  Menu Management")
        try:
            self.menu_btn.setIcon(QIcon("picture/adminmenu.png"))
        except:
            pass
        self.menu_btn.setIconSize(QSize(22, 22))
        self.menu_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #444;
            }
            QPushButton:hover { color: #4F39F6; }
        """)

        self.user_btn = QPushButton("  User Management")
        try:
            self.user_btn.setIcon(QIcon("picture/usermanagement.png"))
        except:
            pass
        self.user_btn.setIconSize(QSize(22, 22))
        self.user_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #444;
            }
            QPushButton:hover { color: #4F39F6; }
        """)

        self.activity_btn = QPushButton("  Activity Logs")
        try:
            self.activity_btn.setIcon(QIcon("picture/activity.png"))
        except:
            pass
        self.activity_btn.setIconSize(QSize(22, 22))
        self.activity_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #444;
            }
            QPushButton:hover { color: #4F39F6; }
        """)

        tab_bar.addWidget(self.overview_btn)
        tab_bar.addWidget(self.order_btn)
        tab_bar.addWidget(self.menu_btn)
        tab_bar.addWidget(self.user_btn)
        tab_bar.addWidget(self.activity_btn)
        tab_bar.addStretch()
        main.addLayout(tab_bar)

        # ----------------------------- STACKED PAGES -----------------------------
        self.pages = QStackedWidget()
        main.addWidget(self.pages)

        self.setLayout(main)

    def set_admin_info(self, admin_name, admin_id):
        """Set admin information in the UI"""
        self.title2.setText(f"{admin_name} | ID: {admin_id}")

    def build_overview_page(self, user_count, total_revenue, today_orders, pending_orders):
        """Build the overview page with analytics cards and graphs"""
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 25px;
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

        # Create the main container widget
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll_area.setWidget(container)

        # Create layout for the container
        outer = QVBoxLayout(container)
        outer.setSpacing(15)
        outer.setContentsMargins(0, 0, 0, 20)

        # Title and Export Button Row
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Analytics Overview")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        title_row.addWidget(title)

        title_row.addStretch()

        # PDF Export Button
        self.pdf_export_btn = QPushButton("Export to PDF")
        self.pdf_export_btn.setFixedSize(150, 42)
        self.pdf_export_btn.setStyleSheet("""
            QPushButton {
                background: #28a745;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background: #218838;
            }
        """)
        title_row.addWidget(self.pdf_export_btn)

        outer.addLayout(title_row)

        # Analytics Cards with icons
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Create cards
        self.total_revenue_card = AnalyticsCard("Total Revenue", f"₱{total_revenue:,.2f}", "#e9fdf1",
                                                "picture/revenue.png")
        self.todays_orders_card = AnalyticsCard("Today's Orders", f"{today_orders}", "#eaf2ff",
                                                "picture/order_tracking.png")
        self.pending_orders_card = AnalyticsCard("Pending Orders", f"{pending_orders}", "#fff7e6",
                                                 "picture/pending_orders.png")
        self.active_users_card = AnalyticsCard("Active Users", f"{user_count}", "#f0f7ff", "picture/active_users.png")

        # Add cards to layout
        cards_layout.addWidget(self.total_revenue_card)
        cards_layout.addWidget(self.todays_orders_card)
        cards_layout.addWidget(self.pending_orders_card)
        cards_layout.addWidget(self.active_users_card)

        outer.addLayout(cards_layout)

        # ========== REVENUE TREND GRAPH SECTION ==========
        graph_section = QFrame()
        graph_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
            }
        """)
        graph_section.setMinimumHeight(450)
        graph_section.setMaximumHeight(500)

        graph_layout = QVBoxLayout(graph_section)
        graph_layout.setContentsMargins(25, 25, 25, 25)

        # Create and add revenue graph
        self.revenue_graph = RevenueGraphWidget()
        graph_layout.addWidget(self.revenue_graph)

        outer.addWidget(graph_section)

        # ========== POPULAR ITEMS PIE CHART SECTION ==========
        pie_chart_section = QFrame()
        pie_chart_section.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
            }
        """)
        pie_chart_section.setMinimumHeight(500)

        pie_chart_layout = QVBoxLayout(pie_chart_section)
        pie_chart_layout.setContentsMargins(25, 25, 25, 25)

        # Pie chart title
        pie_chart_title = QLabel("Most Popular Menu Items")
        pie_chart_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        pie_chart_title.setStyleSheet("color: black; margin-bottom: 15px;")
        pie_chart_layout.addWidget(pie_chart_title)

        # Create and add pie chart
        self.pie_chart_widget = PopularItemsPieChartWidget()
        pie_chart_layout.addWidget(self.pie_chart_widget)

        # Refresh and Export buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.refresh_btn = QPushButton("Refresh Dashboard")
        self.refresh_btn.setFixedSize(200, 40)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: #4F39F6;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background: #4a6aff;
            }
        """)
        self.refresh_btn.setToolTip("Refresh all dashboard data from database")

        button_layout.addWidget(self.refresh_btn)
        pie_chart_layout.addLayout(button_layout)

        outer.addWidget(pie_chart_section)
        outer.addStretch()

        return scroll_area

    def build_orders_page(self):
        """Build the order tracking page"""
        container = QFrame()
        container.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(container)
        outer.setSpacing(15)

        title = QLabel("Order Tracking")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        outer.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by order number, customer name, or email...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                color: black;
            }
        """)

        # Store button as attribute for controller access
        self.order_search_btn = QPushButton("Search")
        self.order_search_btn.setFixedSize(100, 40)
        self.order_search_btn.setStyleSheet("""
            QPushButton {
                background: #4F39F6;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #4a6aff; }
        """)

        # Create a horizontal layout for filter controls
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        # Filter by status combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["All Status", "Pending", "Preparing", "Delivering", "Completed"])
        self.filter_combo.setFixedHeight(40)
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                min-width: 150px;
                color: black;
            }
        """)

        # Store Today's Orders button as attribute
        self.order_today_btn = QPushButton("Today's Orders")
        self.order_today_btn.setFixedHeight(40)
        self.order_today_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover { 
                background: #e5e7eb;
                border: 1px solid #9ca3af;
            }
        """)

        # Add Monthly filter combo
        self.month_filter_combo = QComboBox()
        self.month_filter_combo.addItems(["All Months", "January", "February", "March", "April", "May", "June",
                                          "July", "August", "September", "October", "November", "December"])
        self.month_filter_combo.setFixedHeight(40)
        self.month_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                min-width: 140px;
                color: black;
            }
        """)

        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.order_today_btn)
        filter_layout.addWidget(self.month_filter_combo)

        # Store Refresh button as attribute
        self.order_refresh_btn = QPushButton("Refresh")
        self.order_refresh_btn.setFixedSize(100, 40)
        self.order_refresh_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #e5e7eb; }
        """)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.order_search_btn)
        search_layout.addLayout(filter_layout)
        search_layout.addStretch()
        search_layout.addWidget(self.order_refresh_btn)

        outer.addLayout(search_layout)

        # ==== Scroll Area ====
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 25px;
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

        self.orders_content = QWidget()
        self.orders_layout = QVBoxLayout(self.orders_content)
        self.orders_layout.setSpacing(18)

        self.scroll.setWidget(self.orders_content)
        outer.addWidget(self.scroll)

        return container

    def build_menu_page(self):
        """Build the menu management page"""
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
                width: 8px;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 25px;
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

        # Create main container
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll_area.setWidget(container)

        outer = QVBoxLayout(container)
        outer.setSpacing(22)
        outer.setContentsMargins(0, 0, 0, 20)

        # Title and Add button
        title_layout = QHBoxLayout()

        menu_title = QLabel("Menu Items")
        menu_title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        menu_title.setStyleSheet("color: black;")
        title_layout.addWidget(menu_title)

        title_layout.addStretch()

        # Store Add button as attribute
        self.menu_add_btn = QPushButton("+  Add New Item")
        self.menu_add_btn.setFixedSize(170, 42)
        self.menu_add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4F39F6;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #4a6aff; }
        """)

        title_layout.addWidget(self.menu_add_btn)

        outer.addLayout(title_layout)

        # ----------------------------- TABLE CONTAINER -----------------------------
        table_container = QFrame()
        table_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(30, 30, 30, 30)

        # ----------------------------- TABLE -----------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Changed from 5 to 4 (removed Status column)
        self.table.setHorizontalHeaderLabels(["Item", "Category", "Price", "Actions"])  # Removed "Status"
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # MAKE ROWS TALLER
        self.table.verticalHeader().setDefaultSectionSize(100)

        # Set column widths for better spacing (adjusted for 4 columns)
        self.table.setColumnWidth(0, 650)  # Item column - slightly wider
        self.table.setColumnWidth(1, 150)  # Category - wider
        self.table.setColumnWidth(2, 120)  # Price
        self.table.setColumnWidth(3, 100)  # Actions - smaller since we removed upload button

        # Set resize modes
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        self.table.setStyleSheet("""
            QTableWidget { 
                border: none; 
                color: black;
                font-size: 14px;
            }
            QHeaderView::section {
                background: #f1f0f6;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: black;
                font-size: 14px;
                text-align: center;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        table_layout.addWidget(self.table)
        outer.addWidget(table_container)

        return scroll_area

    def build_user_management_page(self):
        """Build the user management page"""
        container = QFrame()
        container.setStyleSheet("background: transparent;")

        outer = QVBoxLayout(container)
        outer.setSpacing(15)  # Reduced spacing

        # Title and Add User Button Row
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)

        title = QLabel("User Management")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))  # Smaller font
        title.setStyleSheet("color: black;")
        title_row.addWidget(title)

        title_row.addStretch()

        # Store Add New User Button as attribute
        self.user_add_btn = QPushButton("+ Add New User")
        self.user_add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.user_add_btn.setFixedSize(160, 42)  # Smaller button
        self.user_add_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))  # Smaller font
        self.user_add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4F39F6;
                color: white;
                border-radius: 10px;
                font-size: 13px;
                padding: 10px 16px;
            }
            QPushButton:hover { 
                background-color: #4a6aff; 
            }
            QPushButton:pressed { 
                background-color: #3a5af0; 
            }
        """)
        title_row.addWidget(self.user_add_btn)

        outer.addLayout(title_row)

        # ===== ADD SEARCH BAR SECTION (JUST LIKE ORDER TRACKING) =====
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.user_search_input = QLineEdit()
        self.user_search_input.setPlaceholderText("Search by name, email, or role...")
        self.user_search_input.setFixedHeight(40)
        self.user_search_input.setStyleSheet("""
            QLineEdit {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                color: black;
            }
        """)

        # Store Search button as attribute
        self.user_search_btn = QPushButton("Search")
        self.user_search_btn.setFixedSize(100, 40)
        self.user_search_btn.setStyleSheet("""
            QPushButton {
                background: #4F39F6;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #4a6aff; }
        """)

        # Filter by role combo box
        self.user_filter_combo = QComboBox()
        self.user_filter_combo.addItems(["All Roles", "Customer", "Staff"])
        self.user_filter_combo.setFixedHeight(40)
        self.user_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                min-width: 150px;
                color: black;
            }
        """)

        # Store Refresh button as attribute
        self.user_refresh_btn = QPushButton("Refresh")
        self.user_refresh_btn.setFixedSize(100, 40)
        self.user_refresh_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #e5e7eb; }
        """)

        search_layout.addWidget(self.user_search_input)
        search_layout.addWidget(self.user_search_btn)
        search_layout.addWidget(self.user_filter_combo)
        search_layout.addStretch()
        search_layout.addWidget(self.user_refresh_btn)

        outer.addLayout(search_layout)
        # ===== END OF SEARCH BAR SECTION =====

        # Create scroll area for the table (SCROLLABLE)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 25px;
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

        # Card container (inside scroll area)
        self.user_card = QFrame()
        self.user_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
            }
        """)

        self.user_card_layout = QVBoxLayout(self.user_card)
        self.user_card_layout.setContentsMargins(25, 25, 25, 25)  # Smaller margins

        # Table with 4 columns (excluding admin)
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)  # Changed from 5 to 4 (removed Join Date)
        self.user_table.setHorizontalHeaderLabels(
            ["Name", "Email", "Role", "Actions"]  # Removed "Join Date"
        )
        self.user_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setShowGrid(False)
        self.user_table.setAlternatingRowColors(True)

        # Make only Edit and Delete buttons clickable by setting item flags
        self.user_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.user_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.user_table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 14px;
                color: black;
                alternate-background-color: #fafafa;
            }
            QHeaderView::section {
                background: #f1f0f6;
                padding: 14px 12px;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                color: black;
            }
            QTableWidget::item {
                selection-background-color: transparent;
                padding: 8px;
            }
        """)

        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.user_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        self.user_table.setColumnWidth(2, 130)  # Smaller column for Role
        self.user_table.setColumnWidth(3, 220)  # Increased width for Actions column

        # Smaller row height
        self.user_table.verticalHeader().setDefaultSectionSize(60)

        self.user_card_layout.addWidget(self.user_table)

        # Set the card as the scroll area's widget
        scroll_area.setWidget(self.user_card)

        # Add the scroll area to the outer layout
        outer.addWidget(scroll_area)

        return container

    def build_activity_logs_page(self):
        """Build the activity logs page"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(container)
        outer.setSpacing(15)

        # Title
        title = QLabel("Activity Logs")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        outer.addWidget(title)

        # Search and filter controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Search input
        self.activity_search_input = QLineEdit()
        self.activity_search_input.setPlaceholderText("Search by staff name, action, or details...")
        self.activity_search_input.setFixedHeight(40)
        self.activity_search_input.setStyleSheet("""
            QLineEdit {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                color: black;
            }
        """)

        # Store Search button as attribute
        self.activity_search_btn = QPushButton("Search")
        self.activity_search_btn.setFixedSize(100, 40)
        self.activity_search_btn.setStyleSheet("""
            QPushButton {
                background: #4F39F6;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #4a6aff; }
        """)

        # Store TODAY'S LOGS BUTTON as attribute
        self.activity_today_btn = QPushButton("Today's Logs")
        self.activity_today_btn.setFixedSize(140, 40)
        self.activity_today_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background: #e5e7eb;
                border: 1px solid #9ca3af;
            }
        """)

        # PERIOD FILTER COMBOBOX - MATCHING ORDER TRACKING DESIGN
        self.period_filter_combo = QComboBox()
        self.period_filter_combo.addItems(["All Time", "Last 3 Days", "Last 7 Days", "Last 30 Days"])
        self.period_filter_combo.setFixedHeight(40)
        self.period_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 0 15px;
                border: 1px solid #d0ced7;
                border-radius: 8px;
                font-size: 14px;
                min-width: 150px;
                color: black;
            }
        """)

        # Store Clear logs button as attribute
        self.activity_clear_btn = QPushButton("Clear All Logs")
        self.activity_clear_btn.setFixedSize(140, 40)
        self.activity_clear_btn.setStyleSheet("""
            QPushButton {
                background: #dc2626;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #b91c1c; }
        """)

        controls_layout.addWidget(self.activity_search_input)
        controls_layout.addWidget(self.activity_search_btn)
        controls_layout.addWidget(self.activity_today_btn)
        controls_layout.addWidget(self.period_filter_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.activity_clear_btn)

        outer.addLayout(controls_layout)

        # Create scroll area for the table (IDENTICAL TO MENU MANAGEMENT)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 25px;
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

        # Create a container widget for the table
        table_container = QWidget()
        table_container.setStyleSheet("background: transparent;")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # Activity logs table
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(5)
        self.activity_table.setHorizontalHeaderLabels(["Timestamp", "Staff Name", "Staff ID", "Action", "Details"])
        self.activity_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setShowGrid(False)
        self.activity_table.setAlternatingRowColors(True)

        # Enable word wrap for better text display
        self.activity_table.setWordWrap(True)

        # Set better row height to accommodate wrapped text
        self.activity_table.verticalHeader().setDefaultSectionSize(60)

        # Set column widths with better distribution
        self.activity_table.setColumnWidth(0, 180)  # Timestamp
        self.activity_table.setColumnWidth(1, 200)  # Staff Name
        self.activity_table.setColumnWidth(2, 120)  # Staff ID
        self.activity_table.setColumnWidth(3, 300)  # Action - More space for actions
        self.activity_table.horizontalHeader().setSectionResizeMode(4,
                                                                    QHeaderView.ResizeMode.Stretch)  # Details takes remaining space

        # Also allow Staff Name and Action columns to resize
        self.activity_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.activity_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)

        self.activity_table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 14px;
                color: black;
                alternate-background-color: #fafafa;
                border-radius: 10px;
                background: white;
            }
            QHeaderView::section {
                background: #f1f0f6;
                padding: 12px;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                color: black;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            /* Make text selectable for better UX */
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)

        table_layout.addWidget(self.activity_table)

        # Set the table container as the scroll area's widget
        scroll_area.setWidget(table_container)

        # Add the scroll area to the outer layout
        outer.addWidget(scroll_area)

        # Refresh button and stats
        bottom_layout = QHBoxLayout()

        # Stats label
        self.activity_stats_label = QLabel("Total activities: 0")
        self.activity_stats_label.setFont(QFont("Arial", 11))
        self.activity_stats_label.setStyleSheet("color: #666;")
        bottom_layout.addWidget(self.activity_stats_label)

        bottom_layout.addStretch()

        # Store Refresh button as attribute
        self.activity_refresh_btn = QPushButton("Refresh Logs")
        self.activity_refresh_btn.setFixedSize(150, 40)
        self.activity_refresh_btn.setStyleSheet("""
            QPushButton {
                background: #4F39F6;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #4a6aff; }
        """)

        bottom_layout.addWidget(self.activity_refresh_btn)
        outer.addLayout(bottom_layout)

        return container

    def switch_page(self, index):
        """Switch between different pages"""
        self.pages.setCurrentIndex(index)

        # Reset all buttons to inactive style
        for btn in [self.overview_btn, self.order_btn, self.menu_btn, self.user_btn, self.activity_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #444;
                }
                QPushButton:hover { color: #4F39F6; }
            """)

        # Set active button style
        active_btn = None
        if index == 0:
            active_btn = self.overview_btn
        elif index == 1:
            active_btn = self.order_btn
        elif index == 2:
            active_btn = self.menu_btn
        elif index == 3:
            active_btn = self.user_btn
        elif index == 4:
            active_btn = self.activity_btn

        if active_btn:
            active_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #4F39F6;
                    font-weight: bold;
                }
            """)

    def build_order_card(self, order_data, update_status_callback):
        """Build order card from database data"""
        card = QFrame()
        card.order_id = str(order_data.get('id', ''))
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(16)

        # TOP ROW: ORDER ID + STATUS
        top = QHBoxLayout()

        order_id = QLabel(f"Order #{order_data.get('order_number', 'N/A')}")
        order_id.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        order_id.setStyleSheet("color: black;")

        # Customer info
        customer_info = QLabel(f"{order_data.get('customer_name', 'N/A')} • {order_data.get('customer_email', 'N/A')}")
        customer_info.setFont(QFont("Arial", 12))
        customer_info.setStyleSheet("color: #666;")

        top.addWidget(order_id)
        top.addWidget(customer_info)
        top.addStretch()

        # Status selector
        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)

        statuses = ["Pending", "Preparing", "Delivering", "Completed"]
        current_status = order_data.get('status', 'Pending').capitalize()

        for status in statuses:
            btn = QPushButton(status)
            btn.setFixedHeight(38)
            btn.setFixedWidth(100)

            if status == current_status:
                # Style based on status
                if status == "Pending":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #e5e7eb;
                            color: #374151;
                            border-radius: 14px;
                            padding: 8px 15px;
                            font-weight: bold;
                            font-size: 12px;
                        }
                    """)
                elif status == "Preparing":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #fef3c7;
                            color: #b45309;
                            border-radius: 14px;
                            padding: 8px 15px;
                            font-weight: bold;
                            font-size: 12px;
                        }
                    """)
                elif status == "Delivering":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #dbeafe;
                            color: #1e40af;
                            border-radius: 14px;
                            padding: 8px 15px;
                            font-weight: bold;
                            font-size: 12px;
                        }
                    """)
                elif status == "Completed":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #d1fae5;
                            color: #065f46;
                            border-radius: 14px;
                            padding: 8px 15px;
                            font-weight: bold;
                            font-size: 12px;
                        }
                    """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #f3f4f6;
                        color: #4b5563;
                        border-radius: 14px;
                        padding: 8px 15px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QPushButton:hover { background: #e4e4e7; }
                """)

            # Connect button to update status
            btn.clicked.connect(lambda checked, oid=order_data['id'], s=status: update_status_callback(oid, s))
            status_layout.addWidget(btn)

        top.addLayout(status_layout)
        card_layout.addLayout(top)

        # ORDER DETAILS SECTION WITH ADDRESS AND PHONE - ADDED
        details_layout = QVBoxLayout()
        details_layout.setSpacing(5)

        # Order Date
        date_label = QLabel(f"Order Date: {order_data.get('created_at', 'N/A')}")
        date_label.setFont(QFont("Arial", 11))
        date_label.setStyleSheet("color: #888;")
        details_layout.addWidget(date_label)

        # Customer Address - From database field 'customer_address'
        customer_address = order_data.get('customer_address', '')
        if customer_address and customer_address != "No address saved. Please update your address.":
            address_label = QLabel(f"📍 Delivery Address: {customer_address}")
            address_label.setFont(QFont("Arial", 11))
            address_label.setStyleSheet("color: #888;")
            address_label.setWordWrap(True)
            details_layout.addWidget(address_label)
        elif customer_address:
            # Show only if it's not the default message
            address_label = QLabel(f"📍 Delivery Address: Not specified")
            address_label.setFont(QFont("Arial", 11))
            address_label.setStyleSheet("color: #999; font-style: italic;")
            details_layout.addWidget(address_label)

        # Customer Phone Number - From database field 'customer_phone'
        customer_phone = order_data.get('customer_phone', '')
        if customer_phone:
            phone_label = QLabel(f"📞 Contact Number: {customer_phone}")
            phone_label.setFont(QFont("Arial", 11))
            phone_label.setStyleSheet("color: #888;")
            details_layout.addWidget(phone_label)
        else:
            phone_label = QLabel(f"📞 Contact Number: Not provided")
            phone_label.setFont(QFont("Arial", 11))
            phone_label.setStyleSheet("color: #999; font-style: italic;")
            details_layout.addWidget(phone_label)

        card_layout.addLayout(details_layout)

        # ITEMS LIST
        items = order_data.get('items', [])
        for item in items:
            row = QHBoxLayout()
            item_name = QLabel(f"{item.get('qty', 1)}x {item.get('title', 'Unknown')}")
            item_name.setFont(QFont("Arial", 14))
            item_name.setStyleSheet("color: #333;")

            price_lbl = QLabel(item.get('price', '₱0'))
            price_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            price_lbl.setStyleSheet("color: black;")

            row.addWidget(item_name)
            row.addStretch()
            row.addWidget(price_lbl)
            card_layout.addLayout(row)

        # DIVIDER
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color:#e5e7eb; margin: 10px 0;")
        card_layout.addWidget(divider)

        # TOTAL
        total_row = QHBoxLayout()
        total_label = QLabel("Total Amount:")
        total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        total_label.setStyleSheet("color: black;")

        total_amount = QLabel(f"₱{order_data.get('total_amount', 0):,.2f}")
        total_amount.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        total_amount.setStyleSheet("color: #5b7bff;")

        total_row.addWidget(total_label)
        total_row.addStretch()
        total_row.addWidget(total_amount)
        card_layout.addLayout(total_row)

        return card

    def clear_orders_layout(self):
        """Clear all widgets from orders layout"""
        if self.orders_layout:
            for i in reversed(range(self.orders_layout.count())):
                widget = self.orders_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

    def show_no_orders_message(self, message):
        """Show message when no orders are found"""
        self.clear_orders_layout()

        no_orders = QLabel(message)
        no_orders.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        no_orders.setStyleSheet("color: #55606a; padding: 20px;")
        no_orders.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orders_layout.addWidget(no_orders)

        # Add a button to clear filters
        clear_filter_btn = QPushButton("Show All Orders")
        clear_filter_btn.setFixedHeight(40)
        clear_filter_btn.setStyleSheet("""
            QPushButton {
                background: #5b7bff;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover { background: #4a6aff; }
        """)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.addStretch()
        btn_layout.addWidget(clear_filter_btn)
        btn_layout.addStretch()

        self.orders_layout.addWidget(btn_container)
        self.orders_layout.addStretch()

        return clear_filter_btn

    def display_filtered_orders(self, orders, filter_name, update_status_callback):
        """Display filtered orders in the layout"""
        self.clear_orders_layout()

        if not orders:
            btn = self.show_no_orders_message(f"No {filter_name} found")
            return btn

        # Add filter header
        header_label = QLabel(f"Showing {filter_name} ({len(orders)} orders)")
        header_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #5b7bff; padding: 10px 0;")
        self.orders_layout.addWidget(header_label)

        # Add order cards
        for order in orders:
            card = self.build_order_card(order, update_status_callback)
            self.orders_layout.addWidget(card)

        self.orders_layout.addStretch()
        return None

    def populate_table(self, menu_items):
        """Populate the table with menu items from database"""
        self.table.setRowCount(len(menu_items))

        for row, item_data in enumerate(menu_items):
            # --- ITEM CELL (image on left, text on right) ---
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_layout.setSpacing(20)  # Space between image and text
            item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            # Product Image on LEFT
            pic_label = QLabel()
            pix = QPixmap()
            try:
                pix = QPixmap(item_data["image"])
            except:
                pass
            if not pix.isNull():
                pix = pix.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
            else:
                pix = QPixmap(80, 80)
                if item_data["category"] == "Burgers":
                    pix.fill(Qt.GlobalColor.darkRed)
                elif item_data["category"] == "Sides":
                    pix.fill(Qt.GlobalColor.darkYellow)
                elif item_data["category"] == "Chicken":
                    pix.fill(Qt.GlobalColor.darkGreen)
                elif item_data["category"] == "Drinks":
                    pix.fill(Qt.GlobalColor.blue)
                else:
                    pix.fill(Qt.GlobalColor.darkCyan)
            pic_label.setPixmap(pix)
            pic_label.setFixedSize(80, 80)

            # Text Content on RIGHT of image
            text_widget = QWidget()
            text_layout = QVBoxLayout()
            text_layout.setContentsMargins(0, 0, 0, 0)
            text_layout.setSpacing(5)
            text_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            # Product Name
            title_label = QLabel(f"<b>{item_data['title']}</b>")
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            title_label.setStyleSheet("color: black; margin-bottom: 3px;")

            # Product Description
            desc_label = QLabel(item_data["description"])
            desc_label.setWordWrap(True)
            desc_label.setFont(QFont("Arial", 11))
            desc_label.setStyleSheet("color: #555; line-height: 1.3;")
            desc_label.setMaximumWidth(500)  # Limit width for better readability

            text_layout.addWidget(title_label)
            text_layout.addWidget(desc_label)
            text_widget.setLayout(text_layout)

            # Add image and text to the main layout
            item_layout.addWidget(pic_label)
            item_layout.addWidget(text_widget)
            item_layout.addStretch()  # Push content to the left

            item_widget.setLayout(item_layout)
            self.table.setCellWidget(row, 0, item_widget)

            # Category
            cat_item = QTableWidgetItem(item_data["category"])
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            cat_item.setFont(QFont("Arial", 12))
            self.table.setItem(row, 1, cat_item)

            # Price - CHANGED TO PHP PESO SIGN
            price_item = QTableWidgetItem(f"₱{item_data['price']}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.table.setItem(row, 2, price_item)

            # Actions (Edit and Delete only - Upload removed)
            actions_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            edit_btn = QPushButton()
            try:
                edit_btn.setIcon(QIcon("picture/edit.png"))
            except:
                pass
            edit_btn.setFixedSize(32, 32)
            edit_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: #f3f0ff;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #e8e5ff;
                }
            """)
            edit_btn.row = row  # Store row number

            # Delete button
            delete_btn = QPushButton()
            try:
                delete_btn.setIcon(QIcon("picture/delete.png"))
            except:
                # If no delete icon, use text
                delete_btn.setText("×")
                delete_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            delete_btn.setFixedSize(32, 32)
            delete_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: #ffeaea;
                    border-radius: 8px;
                    color: #d32f2f;
                }
                QPushButton:hover {
                    background-color: #ffdbdb;
                }
            """)
            delete_btn.row = row  # Store row number

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            actions_widget.setLayout(action_layout)

            self.table.setCellWidget(row, 3, actions_widget)

    def populate_user_table_with_data(self, users_data, edit_callback, delete_callback):
        """Populate the user table with provided data"""
        # Clear existing rows
        self.user_table.setRowCount(0)

        # Set row count based on actual users
        self.user_table.setRowCount(len(users_data))

        for row, user in enumerate(users_data):
            # Name
            name_item = QTableWidgetItem(user['name'])
            name_item.setFont(QFont("Arial", 12, QFont.Weight.Medium))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
            self.user_table.setItem(row, 0, name_item)

            # Email
            email_item = QTableWidgetItem(user['email'])
            email_item.setFont(QFont("Arial", 11))
            email_item.setFlags(email_item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
            self.user_table.setItem(row, 1, email_item)

            # Role badge - Ensure first letter is capitalized
            role = user['role']
            if role:  # Ensure role is not empty
                role = role[0].upper() + role[1:].lower()
            else:
                role = "User"  # Default if role is empty

            role_lbl = QLabel(role)
            role_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            role_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))

            if role.lower() == "customer":
                role_lbl.setStyleSheet("""
                    background: #eaf2ff;
                    color: #2563eb;
                    padding: 8px 16px;
                    border-radius: 16px;
                    font-weight: bold;
                        font-size: 12px;
                """)
            elif role.lower() == "staff":
                role_lbl.setStyleSheet("""
                    background: #f3e8ff;
                    color: #7c3aed;
                    padding: 8px 16px;
                    border-radius: 16px;
                    font-weight: bold;
                        font-size: 12px;
                """)
            else:
                role_lbl.setStyleSheet("""
                    background: #f0f0f0;
                    color: #666;
                    padding: 8px 16px;
                    border-radius: 16px;
                    font-weight: bold;
                        font-size: 12px;
                """)

            self.user_table.setCellWidget(row, 2, role_lbl)

            # Actions (Edit & Delete)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setFixedSize(85, 38)
            edit_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            edit_btn.setStyleSheet("""
                QPushButton {
                    background: #f3f4f6;
                    color: black;
                    border-radius: 8px;
                    padding: 6px 12px;
                    border: none;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background: #e5e7eb;
                }
            """)
            edit_btn.clicked.connect(lambda checked, r=row, u=user: edit_callback(r, u))

            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.setFixedSize(95, 38)
            delete_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            delete_btn.setStyleSheet("""
                QPushButton {
                    background: #fee2e2;
                    color: #dc2626;
                    border-radius: 8px;
                    padding: 6px 12px;
                    border: none;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background: #fecaca;
                }
            """)
            delete_btn.clicked.connect(lambda checked, r=row, u=user: delete_callback(r, u))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)

            self.user_table.setCellWidget(row, 3, action_widget)

    def populate_activity_table(self, activities):
        """Populate the activity table with data"""
        self.activity_table.setRowCount(0)

        if not activities:
            return

        self.activity_table.setRowCount(len(activities))

        for row, activity in enumerate(activities):
            # Timestamp - Convert datetime to string
            timestamp = activity.get('created_at', '')
            if isinstance(timestamp, datetime):
                # Format the datetime as a readable string
                timestamp_str = timestamp.strftime("%Y-%m-%d %I:%M %p")
            else:
                timestamp_str = str(timestamp) if timestamp else ''

            timestamp_item = QTableWidgetItem(timestamp_str)
            timestamp_item.setFont(QFont("Arial", 11))
            self.activity_table.setItem(row, 0, timestamp_item)

            # Staff Name - INCREASED COLUMN WIDTH
            staff_item = QTableWidgetItem(activity.get('staff_name', ''))
            staff_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            # Allow word wrap for long names
            staff_item.setFlags(staff_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.activity_table.setItem(row, 1, staff_item)

            # Staff ID - INCREASED COLUMN WIDTH
            id_item = QTableWidgetItem(activity.get('staff_id', ''))
            id_item.setFont(QFont("Arial", 11))
            self.activity_table.setItem(row, 2, id_item)

            # Action - INCREASED COLUMN WIDTH
            action_item = QTableWidgetItem(activity.get('action', ''))
            action_item.setFont(QFont("Arial", 11))
            # Allow word wrap for longer actions
            action_item.setFlags(action_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.activity_table.setItem(row, 3, action_item)

            # Details - Will use stretch mode
            details_item = QTableWidgetItem(activity.get('details', ''))
            details_item.setFont(QFont("Arial", 11))
            details_item.setForeground(Qt.GlobalColor.darkGray)
            # Allow word wrap for details
            details_item.setFlags(details_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.activity_table.setItem(row, 4, details_item)

            # Set row height to accommodate wrapped text
            self.activity_table.setRowHeight(row, 60)

    def show_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Helper method to show messages"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon_type)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 10px 20px;
                border-radius: 8px;
                min-width: 100px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        msg.exec()

    def show_logout_confirmation(self):
        """Show confirmation dialog before logging out"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Apply the same styling as customer dashboard
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Set Yes button to red for emphasis (matches customer dashboard)
        msg.button(QMessageBox.StandardButton.Yes).setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #ff6b6b;
                border: 1px solid #ff5252;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)

        return msg.exec()