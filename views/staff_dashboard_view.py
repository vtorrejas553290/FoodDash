"""
Staff Dashboard View
Handles the UI components and layout
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView,
    QScrollArea, QStackedWidget, QMessageBox, QInputDialog, QFileDialog,
    QDialog, QLineEdit, QTextEdit, QComboBox, QDialogButtonBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal


class StaffDashboardView(QWidget):
    """View for staff dashboard"""

    # Signals emitted by view
    logout_requested = pyqtSignal()
    page_switched = pyqtSignal(int)
    add_item_clicked = pyqtSignal()
    edit_item_clicked = pyqtSignal(int)
    delete_item_clicked = pyqtSignal(int)
    search_orders_clicked = pyqtSignal()
    filter_orders_changed = pyqtSignal(str)
    refresh_orders_clicked = pyqtSignal()
    order_status_changed = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Staff Dashboard")
        self.resize(1350, 820)
        self.setStyleSheet("background-color: #f6f7fb;")

        # Store UI components
        self.table = None
        self.search_input = None
        self.orders_layout = None
        self.orders_content = None
        self.scroll = None
        self.pages = None
        self.menu_btn = None
        self.order_btn = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface"""
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
        self.title1 = QLabel("Staff Dashboard")
        self.title1.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title1.setStyleSheet("color: #8a5cff;")

        self.title2 = QLabel("Welcome, Staff")
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
        self.logout_btn.clicked.connect(self.logout_requested.emit)

        top_bar.addWidget(logo)
        top_bar.addLayout(title_box)
        top_bar.addStretch()
        top_bar.addWidget(self.logout_btn)
        main.addLayout(top_bar)

        # ----------------------------- TABS -----------------------------
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(28)

        self.menu_btn = QPushButton("  Menu Management")
        try:
            self.menu_btn.setIcon(QIcon("picture/staffmenu.png"))
        except:
            pass
        self.menu_btn.setIconSize(QSize(22, 22))
        self.menu_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #8a5cff;
                font-weight: bold;
            }
        """)

        self.order_btn = QPushButton("  Customer Orders")
        try:
            self.order_btn.setIcon(QIcon("picture/stafforder.png"))
        except:
            pass
        self.order_btn.setIconSize(QSize(22, 22))
        self.order_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 15px;
                color: #444;
            }
            QPushButton:hover { color: #8a5cff; }
        """)

        self.menu_btn.clicked.connect(lambda: self.page_switched.emit(0))
        self.order_btn.clicked.connect(lambda: self.page_switched.emit(1))

        tab_bar.addWidget(self.menu_btn)
        tab_bar.addWidget(self.order_btn)
        tab_bar.addStretch()
        main.addLayout(tab_bar)

        # ----------------------------- STACKED PAGES -----------------------------
        self.pages = QStackedWidget()
        main.addWidget(self.pages)

        self.setLayout(main)

    def set_staff_info(self, staff_name, staff_id):
        """Set staff information in the UI"""
        self.title2.setText(f"Welcome, {staff_name} (ID: {staff_id})")

    def build_menu_page(self, menu_items):
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

        # Add button
        add_btn = QPushButton("+  Add New Item")
        add_btn.setFixedSize(170, 42)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b6bff;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #825af8; }
        """)
        add_btn.clicked.connect(self.add_item_clicked.emit)
        title_layout.addWidget(add_btn)

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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Category", "Price", "Actions"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # MAKE ROWS TALLER
        self.table.verticalHeader().setDefaultSectionSize(100)

        # Set column widths for better spacing
        self.table.setColumnWidth(0, 650)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 100)

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

    def populate_menu_table(self, menu_items):
        """Populate the table with menu items"""
        self.table.setRowCount(len(menu_items))

        for row, item_data in enumerate(menu_items):
            # --- ITEM CELL (image on left, text on right) ---
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_layout.setSpacing(20)
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
            desc_label.setMaximumWidth(500)

            text_layout.addWidget(title_label)
            text_layout.addWidget(desc_label)
            text_widget.setLayout(text_layout)

            # Add image and text to the main layout
            item_layout.addWidget(pic_label)
            item_layout.addWidget(text_widget)
            item_layout.addStretch()

            item_widget.setLayout(item_layout)
            self.table.setCellWidget(row, 0, item_widget)

            # Category
            cat_item = QTableWidgetItem(item_data["category"])
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            cat_item.setFont(QFont("Arial", 12))
            self.table.setItem(row, 1, cat_item)

            # Price
            price_item = QTableWidgetItem(f"₱{item_data['price']}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            self.table.setItem(row, 2, price_item)

            # Actions
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
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_item_clicked.emit(r))

            delete_btn = QPushButton()
            try:
                delete_btn.setIcon(QIcon("picture/delete.png"))
            except:
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
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_item_clicked.emit(r))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            actions_widget.setLayout(action_layout)

            self.table.setCellWidget(row, 3, actions_widget)

    def build_orders_page(self):
        """Build the customer orders page"""
        container = QFrame()
        container.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(container)
        outer.setSpacing(15)

        title = QLabel("Customer Orders")
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

        search_btn = QPushButton("Search")
        search_btn.setFixedSize(100, 40)
        search_btn.setStyleSheet("""
            QPushButton {
                background: #9b6bff;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #825af8; }
        """)
        search_btn.clicked.connect(self.search_orders_clicked.emit)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Status", "Pending", "Preparing", "Delivering", "Completed"])
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
        self.filter_combo.currentTextChanged.connect(self.filter_orders_changed.emit)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFixedSize(100, 40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background: #e5e7eb; }
        """)
        refresh_btn.clicked.connect(self.refresh_orders_clicked.emit)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(self.filter_combo)
        search_layout.addStretch()
        search_layout.addWidget(refresh_btn)

        outer.addLayout(search_layout)

        # Scroll Area
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

    def build_order_card(self, order_data):
        """Build order card from data"""
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

            btn.clicked.connect(lambda checked, oid=order_data['id'], s=status: self.order_status_changed.emit(oid, s))
            status_layout.addWidget(btn)

        top.addLayout(status_layout)
        card_layout.addLayout(top)

        # CUSTOMER CONTACT INFORMATION
        contact_layout = QVBoxLayout()
        contact_layout.setSpacing(5)

        # Order Date
        date_label = QLabel(f"Order Date: {order_data.get('created_at', 'N/A')}")
        date_label.setFont(QFont("Arial", 11))
        date_label.setStyleSheet("color: #888;")
        contact_layout.addWidget(date_label)

        # Customer Address
        customer_address = order_data.get('customer_address', '')
        if customer_address and customer_address != "No address saved. Please update your address.":
            address_label = QLabel(f"📍 Delivery Address: {customer_address}")
            address_label.setFont(QFont("Arial", 11))
            address_label.setStyleSheet("color: #888; padding-left: 5px;")
            address_label.setWordWrap(True)
            contact_layout.addWidget(address_label)
        elif customer_address:
            address_label = QLabel(f"📍 Delivery Address: Not specified")
            address_label.setFont(QFont("Arial", 11))
            address_label.setStyleSheet("color: #999; padding-left: 5px; font-style: italic;")
            contact_layout.addWidget(address_label)

        # Customer Phone Number
        customer_phone = order_data.get('customer_phone', '')
        if customer_phone:
            phone_label = QLabel(f"📞 Contact Number: {customer_phone}")
            phone_label.setFont(QFont("Arial", 11))
            phone_label.setStyleSheet("color: #888; padding-left: 5px;")
            contact_layout.addWidget(phone_label)
        else:
            phone_label = QLabel(f"📞 Contact Number: Not provided")
            phone_label.setFont(QFont("Arial", 11))
            phone_label.setStyleSheet("color: #999; padding-left: 5px; font-style: italic;")
            contact_layout.addWidget(phone_label)

        card_layout.addLayout(contact_layout)

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
        total_amount.setStyleSheet("color: #9b6bff;")

        total_row.addWidget(total_label)
        total_row.addStretch()
        total_row.addWidget(total_amount)
        card_layout.addLayout(total_row)

        return card

    def display_orders(self, orders_to_display):
        """Display orders in the layout"""
        # Clear current orders
        for i in reversed(range(self.orders_layout.count())):
            widget = self.orders_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if not orders_to_display:
            no_orders = QLabel("No orders match the selected filter")
            no_orders.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            no_orders.setStyleSheet("color: #55606a; padding: 20px;")
            no_orders.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_layout.addWidget(no_orders)
            self.orders_layout.addStretch()
            return

        # Display orders
        for order in orders_to_display:
            order_id = str(order.get('id', ''))
            card = self.build_order_card(order)
            card.order_id = order_id
            self.orders_layout.addWidget(card)

        # Add stretch at the end
        self.orders_layout.addStretch()

    def show_add_item_dialog(self):
        """Show dialog to add new menu item"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Menu Item")
        dialog.setFixedSize(500, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Title:")
        title_input = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Description
        desc_label = QLabel("Description:")
        desc_input = QTextEdit()
        desc_input.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        # Category
        cat_label = QLabel("Category:")
        cat_input = QComboBox()
        cat_input.addItems(["Burgers", "Sides", "Chicken", "Drinks", "Pizza"])
        cat_input.setStyleSheet("""
            QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #f3f0ff;
                selection-color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        layout.addWidget(cat_label)
        layout.addWidget(cat_input)

        # Price
        price_label = QLabel("Price (₱):")
        price_input = QLineEdit()
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Image path
        image_label = QLabel("Image Path:")
        image_input = QLineEdit("picture/default.png")
        layout.addWidget(image_label)
        layout.addWidget(image_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            return {
                'title': title_input.text().strip(),
                'description': desc_input.toPlainText().strip(),
                'category': cat_input.currentText(),
                'price': price_input.text().strip(),
                'image': image_input.text().strip()
            }
        return None

    def show_edit_item_dialog(self, item_data):
        """Show dialog to edit menu item"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Menu Item")
        dialog.setFixedSize(500, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                border: 1px solid #ccc;    
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Title:")
        title_input = QLineEdit(item_data["title"])
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Description
        desc_label = QLabel("Description:")
        desc_input = QTextEdit(item_data["description"])
        desc_input.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        # Category
        cat_label = QLabel("Category:")
        cat_input = QComboBox()
        cat_input.addItems(["Burgers", "Sides", "Chicken", "Drinks", "Pizza"])
        cat_input.setCurrentText(item_data["category"])
        cat_input.setStyleSheet("""
            QComboBox {
                color: black;
                background-color: white;
                border: 1px solid #d0ced7;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #f3f0ff;
                selection-color: black;
            }
        """)
        layout.addWidget(cat_label)
        layout.addWidget(cat_input)

        # Price
        price_value = item_data["price"].replace("₱", "") if "₱" in item_data["price"] else item_data["price"]
        price_label = QLabel("Price (₱):")
        price_input = QLineEdit(price_value)
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Image path
        image_label = QLabel("Image Path:")
        image_input = QLineEdit(item_data["image"])
        layout.addWidget(image_label)
        layout.addWidget(image_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            return {
                'title': title_input.text().strip(),
                'description': desc_input.toPlainText().strip(),
                'category': cat_input.currentText(),
                'price': price_input.text().strip(),
                'image': image_input.text().strip()
            }
        return None

    def show_delete_confirmation(self, item_name):
        """Show confirmation dialog for deleting item"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete '{item_name}' from the database?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

        return msg.exec() == QMessageBox.StandardButton.Yes

    def show_logout_confirmation(self):
        """Show confirmation dialog before logging out"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

        return msg.exec() == QMessageBox.StandardButton.Yes

    def show_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Show message box"""
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
        msg.exec()

    def get_search_term(self):
        """Get search term from input"""
        return self.search_input.text().strip()

    def switch_page(self, index):
        """Switch between pages"""
        self.pages.setCurrentIndex(index)

        if index == 0:  # Menu Management active
            self.menu_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #8a5cff;
                    font-weight: bold;
                }
            """)
            self.order_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #444;
                }
                QPushButton:hover { color: #8a5cff; }
            """)
        else:  # Customer Orders active
            self.menu_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #444;
                }
                QPushButton:hover { color: #8a5cff; }
            """)
            self.order_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 15px;
                    color: #8a5cff;
                    font-weight: bold;
                }
            """)