"""
Customer Menu View
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QScrollArea, QGridLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog
)
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import os


class TopBar(QFrame):
    logout_requested = pyqtSignal()

    def __init__(self, customer_info=None):
        super().__init__()
        self.setObjectName("topbar")
        self.setFixedHeight(72)
        self.setStyleSheet("""
            QFrame#topbar {
                background: white;
                border-bottom: 1px solid #eef2f6;
            }
        """)
        layout = QHBoxLayout()
        layout.setContentsMargins(18, 8, 18, 8)

        logo = QLabel()
        logo_pix = QPixmap("picture/logo.png").scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(logo_pix)

        title = QLabel("Food Dash")
        title.setFont(QFont("Arial", 18, QFont.Weight.DemiBold))
        title.setStyleSheet("color:#0080ff;")

        left = QHBoxLayout()
        left.addWidget(logo)
        left.addSpacing(8)
        left.addWidget(title)
        left.addStretch()

        if customer_info:
            welcome_text = f"Welcome, {customer_info['full_name']}"
        else:
            welcome_text = "Welcome, Customer"

        self.welcome_label = QLabel(welcome_text)
        self.welcome_label.setFont(QFont("Arial", 11))
        self.welcome_label.setStyleSheet("color:#55606a;")

        self.logout = QPushButton("Logout")
        self.logout.setFixedHeight(42)
        try:
            self.logout.setIcon(QIcon("picture/logout.png"))
        except:
            pass
        self.logout.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 10px;
                padding: 8px 22px;
                border: 1px solid #d0ced7;
                color: black;
            }
            QPushButton:hover { background: #ececec; }
        """)
        self.logout.clicked.connect(self.confirm_logout)

        right = QHBoxLayout()
        right.addStretch()
        right.addWidget(self.welcome_label)
        right.addSpacing(12)
        right.addWidget(self.logout)

        layout.addLayout(left)
        layout.addLayout(right)
        self.setLayout(layout)

    def confirm_logout(self):
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

        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def update_welcome_text(self, customer_info):
        if customer_info:
            self.welcome_label.setText(f"Welcome, {customer_info['full_name']}")
        else:
            self.welcome_label.setText("Welcome, Customer")


class MenuCard(QFrame):
    add_to_cart = pyqtSignal(str, str, str)

    def __init__(self, img, title, subtitle, price):
        super().__init__()
        self.setObjectName("card")
        self.setFixedSize(320, 400)
        self.setStyleSheet("""
            QFrame#card {
                background:white;
                border-radius:14px;
                border:1px solid #eef2f6;
            }
        """)
        main = QVBoxLayout()
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(12)

        img_lbl = QLabel()
        try:
            pix = QPixmap(img).scaled(300, 220, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                      Qt.TransformationMode.SmoothTransformation)
            img_lbl.setPixmap(pix)
        except:
            pix = QPixmap(300, 220)
            pix.fill(Qt.GlobalColor.lightGray)
            img_lbl.setPixmap(pix)

        img_lbl.setFixedSize(300, 220)
        img_lbl.setStyleSheet("border-radius:12px;")

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 14, QFont.Weight.DemiBold))
        title_lbl.setStyleSheet("color:#213547;")

        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setFont(QFont("Arial", 10))
        subtitle_lbl.setStyleSheet("color:#8a98a6;")
        subtitle_lbl.setWordWrap(True)

        bottom = QHBoxLayout()
        price_lbl = QLabel(price)
        price_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        price_lbl.setStyleSheet("color: black;")

        add_btn = QPushButton("Add  +")
        add_btn.setFixedSize(90, 38)
        add_btn.setStyleSheet("""
            QPushButton {
                background:#2ea1ff;
                color:white;
                border-radius:19px;
            }
            QPushButton:hover {
                background:#1e90ff;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_to_cart.emit(title, price, img))

        bottom.addWidget(price_lbl)
        bottom.addStretch()
        bottom.addWidget(add_btn)

        main.addWidget(img_lbl)
        main.addWidget(title_lbl)
        main.addWidget(subtitle_lbl)
        main.addStretch()
        main.addLayout(bottom)

        self.setLayout(main)


class CartWidget(QWidget):
    quantity_changed = pyqtSignal(int, int)
    item_deleted = pyqtSignal(int)

    def __init__(self, cart_items, orders_items, customer_info=None):
        super().__init__()
        self.cart_items = cart_items
        self.orders_items = orders_items
        self.customer_info = customer_info
        self.setStyleSheet("background:#f6f8fb;")

        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(15)

        title = QLabel("Your Order")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color:#213547;")
        main.addWidget(title)

        subtitle = QLabel("Review and edit items")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color:#55606a;")
        main.addWidget(subtitle)

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

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.cart_list = QListWidget()
        self.cart_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                padding: 0px;
                border: none;
            }
        """)
        scroll_layout.addWidget(self.cart_list)

        scroll_area.setWidget(scroll_content)
        main.addWidget(scroll_area)

        self.subtotal_label = QLabel("Subtotal: ₱0")
        self.subtotal_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.subtotal_label.setStyleSheet("color:#213547; padding:10px; background:#edf4ff; border-radius:10px;")
        main.addWidget(self.subtotal_label)

        self.checkout_btn = QPushButton("Proceed to Checkout")
        self.checkout_btn.setFixedHeight(50)
        self.checkout_btn.setFixedWidth(200)
        self.checkout_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2ea1ff, stop:1 #0080ff);
                color:white;
                font-size:16px;
                font-weight:bold;
                border-radius:12px;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e90ff, stop:1 #006fcc);
            }
        """)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.checkout_btn)
        button_layout.addStretch()

        main.addWidget(button_container)
        self.setLayout(main)

    def update_cart(self):
        self.cart_list.clear()
        total = 0

        if not self.cart_items:
            empty_label = QLabel("Your cart is empty")
            empty_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #55606a; padding:20px;")

            empty_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(empty_label)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_widget.setLayout(layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(empty_widget.sizeHint())
            self.cart_list.addItem(list_item)
            self.cart_list.setItemWidget(list_item, empty_widget)

            self.subtotal_label.setText("Subtotal: ₱0")
            return

        for i, item in enumerate(self.cart_items):
            title = item['title']
            price = item['price']
            img = item['img']
            qty = item.get('qty', 1)

            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(15)
            widget.setStyleSheet("background:white; border-radius:12px;")

            img_label = QLabel()
            try:
                pix = QPixmap(img).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
                img_label.setPixmap(pix)
            except:
                pix = QPixmap(80, 80)
                pix.fill(Qt.GlobalColor.lightGray)
                img_label.setPixmap(pix)
            layout.addWidget(img_label)

            vbox = QVBoxLayout()
            name_lbl = QLabel(title)
            name_lbl.setFont(QFont("Arial", 16, QFont.Weight.DemiBold))
            name_lbl.setStyleSheet("color: black;")
            price_lbl = QLabel(price)
            price_lbl.setFont(QFont("Arial", 14))
            price_lbl.setStyleSheet("color: black;")
            vbox.addWidget(name_lbl)
            vbox.addWidget(price_lbl)

            hbox_qty = QHBoxLayout()
            minus_btn = QPushButton()
            minus_btn.setFixedSize(34, 34)
            try:
                minus_btn.setIcon(QIcon("picture/minus.png"))
            except:
                minus_btn.setText("-")
            minus_btn.setIconSize(QSize(26, 26))
            minus_btn.setStyleSheet("border:none; background:transparent;")
            minus_btn.clicked.connect(lambda _, index=i: self.change_quantity(index, -1))

            qty_lbl = QLabel(str(qty))
            qty_lbl.setFixedWidth(20)
            qty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_lbl.setFont(QFont("Arial", 12))
            qty_lbl.setStyleSheet("color: gray;")

            plus_btn = QPushButton()
            plus_btn.setFixedSize(34, 34)
            try:
                plus_btn.setIcon(QIcon("picture/plus.png"))
            except:
                plus_btn.setText("+")
            plus_btn.setIconSize(QSize(26, 26))
            plus_btn.setStyleSheet("border:none; background:transparent;")
            plus_btn.clicked.connect(lambda _, index=i: self.change_quantity(index, 1))

            hbox_qty.addWidget(minus_btn)
            hbox_qty.addWidget(qty_lbl)
            hbox_qty.addWidget(plus_btn)
            vbox.addLayout(hbox_qty)

            layout.addLayout(vbox)
            layout.addStretch()

            del_btn = QPushButton()
            del_btn.setFixedSize(36, 36)
            try:
                del_btn.setIcon(QIcon("picture/delete.png"))
            except:
                del_btn.setText("×")
            del_btn.setIconSize(QSize(28, 28))
            del_btn.setStyleSheet("border:none; background:transparent;")
            del_btn.clicked.connect(lambda _, index=i: self.delete_item(index))
            layout.addWidget(del_btn)

            widget.setLayout(layout)
            list_item = QListWidgetItem()
            list_item.setSizeHint(widget.sizeHint())
            self.cart_list.addItem(list_item)
            self.cart_list.setItemWidget(list_item, widget)

            price_val = self.extract_price(price) * qty
            total += price_val

        if total.is_integer():
            self.subtotal_label.setText(f"Subtotal: ₱{int(total)}")
        else:
            self.subtotal_label.setText(f"Subtotal: ₱{total:.2f}")

    def change_quantity(self, index, delta):
        self.quantity_changed.emit(index, delta)

    def delete_item(self, index):
        self.item_deleted.emit(index)

    def extract_price(self, price_str):
        try:
            clean_str = str(price_str).replace("₱", "").replace("P", "").strip()
            import re
            clean_str = re.sub(r'[^\d.]', '', clean_str)
            if not clean_str:
                return 0.0
            return float(clean_str)
        except Exception:
            return 0.0


class OrdersWidget(QWidget):
    def __init__(self, customer_info):
        super().__init__()
        self.customer_info = customer_info
        self.setStyleSheet("background:#f6f8fb;")
        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Your Orders")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color:#213547;")
        main.addWidget(title)

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

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.orders_list = QListWidget()
        self.orders_list.setStyleSheet("""
            QListWidget {
                background: white;
                border: 1px solid #eef2f6;
                border-radius: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eef2f6;
            }
        """)
        scroll_layout.addWidget(self.orders_list)

        scroll_area.setWidget(scroll_content)
        main.addWidget(scroll_area)

        self.setLayout(main)

    def add_order_card(self, order_data):
        card = QWidget()
        card.setStyleSheet("background:white; border-radius:18px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        status = order_data.get('status', 'pending').capitalize()
        status_colors = {
            'Pending': '#e5e7eb',
            'Preparing': '#fef3c7',
            'Delivering': '#dbeafe',
            'Completed': '#d1fae5',
            'Cancelled': '#fee2e2'
        }

        header = QWidget()
        header.setStyleSheet(f"""
            background: {status_colors.get(status, '#e5e7eb')};
            border-top-left-radius:18px;
            border-top-right-radius:18px;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 16, 18, 16)

        order_info = QVBoxLayout()
        order_id = QLabel(f"Order #{order_data.get('order_number', 'N/A')}")
        order_id.setStyleSheet("color:black; font-size:16px; font-weight:600;")

        date_str = order_data.get('created_at', '')
        formatted_date = self.format_database_date(date_str)

        date_label = QLabel(formatted_date)
        date_label.setStyleSheet("color:black; font-size:12px;")

        order_info.addWidget(order_id)
        order_info.addWidget(date_label)
        header_layout.addLayout(order_info)

        header_layout.addStretch()

        status_widget = QWidget()
        status_widget_layout = QHBoxLayout(status_widget)
        status_widget_layout.setContentsMargins(10, 5, 10, 5)
        status_widget.setStyleSheet("background: white; border-radius:12px;")

        status_text = QLabel(status)
        status_text.setStyleSheet("color:black; font-size:14px; font-weight:600;")
        status_widget_layout.addWidget(status_text)
        header_layout.addWidget(status_widget)

        card_layout.addWidget(header)

        items = order_data.get('items', [])
        for item in items:
            if isinstance(item, dict):
                product_row = QWidget()
                product_layout = QHBoxLayout(product_row)
                product_layout.setContentsMargins(18, 14, 18, 14)

                img = QLabel()
                try:
                    image_path = item.get('img', '')
                    if image_path:
                        image_pix = QPixmap(image_path).scaled(
                            60, 60,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        img.setPixmap(image_pix)
                except:
                    pix = QPixmap(60, 60)
                    pix.fill(Qt.GlobalColor.lightGray)
                    img.setPixmap(pix)
                product_layout.addWidget(img)

                vbox = QVBoxLayout()
                name = QLabel(item.get('title', 'Unknown'))
                name.setStyleSheet("font-size:15px; font-weight:600; color:#213547;")
                qty = QLabel(f"Qty: {item.get('qty', 1)}")
                qty.setStyleSheet("font-size:13px; color:#626f82;")
                vbox.addWidget(name)
                vbox.addWidget(qty)
                product_layout.addLayout(vbox)

                product_layout.addStretch()

                price = QLabel(item.get('price', '₱0'))
                price.setStyleSheet("font-size:15px; color:#213547; font-weight:500;")
                product_layout.addWidget(price)

                card_layout.addWidget(product_row)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color:#e5e7eb;")
        card_layout.addWidget(divider)

        totals = QWidget()
        totals_layout = QVBoxLayout(totals)
        totals_layout.setContentsMargins(20, 20, 20, 20)

        subtotal = float(order_data.get('subtotal', 0))
        delivery_fee = float(order_data.get('delivery_fee', 50))
        grand_total = float(order_data.get('total_amount', 0))

        lbl_sub = QLabel(f"Subtotal             ₱{subtotal:,.2f}")
        lbl_fee = QLabel(f"Delivery Fee     ₱{delivery_fee:,.2f}")
        lbl_total = QLabel(f"Total                 ₱{grand_total:,.2f}")

        lbl_sub.setStyleSheet("font-size:15px; color:black;")
        lbl_fee.setStyleSheet("font-size:15px; color:black;")
        lbl_total.setStyleSheet("font-size:18px; font-weight:700; color:black;")

        totals_layout.addWidget(lbl_sub)
        totals_layout.addWidget(lbl_fee)
        totals_layout.addWidget(lbl_total)

        card_layout.addWidget(totals)

        list_item = QListWidgetItem()
        list_item.setSizeHint(card.sizeHint())
        self.orders_list.addItem(list_item)
        self.orders_list.setItemWidget(list_item, card)

    def show_no_orders(self, message):
        empty_label = QLabel(message)
        empty_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("color: #55606a; padding:20px;")

        empty_widget = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(empty_label)
        layout.addStretch()
        empty_widget.setLayout(layout)

        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(0, 150))
        self.orders_list.addItem(list_item)
        self.orders_list.setItemWidget(list_item, empty_widget)

    def format_database_date(self, date_str):
        if not date_str:
            return "Date not available"

        try:
            import re
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
                r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{2}/\d{2}/\d{4})',
            ]

            for pattern in date_patterns:
                match = re.search(pattern, str(date_str))
                if match:
                    date_part = match.group(1)
                    time_formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%dT%H:%M:%S',
                        '%Y-%m-%d',
                        '%m/%d/%Y'
                    ]

                    for time_format in time_formats:
                        try:
                            from datetime import datetime
                            date_obj = datetime.strptime(date_part, time_format)
                            formatted_date = date_obj.strftime("%m/%d/%Y • %I:%M %p")
                            return formatted_date
                        except ValueError:
                            continue

            if isinstance(date_str, str):
                clean_str = date_str.split('.')[0]
                clean_str = clean_str.replace('T', ' ')
                return clean_str[:19]

            return "Date not available"
        except Exception as e:
            return "Date not available"


class ProfileWidget(QWidget):
    logout_requested = pyqtSignal()
    back_requested = pyqtSignal()
    profile_edit_requested = pyqtSignal(str, str, str)  # field, new_value, current_password

    def __init__(self, customer_info=None):
        super().__init__()
        self.customer_info = customer_info
        self.setStyleSheet("background:#f6f8fb;")

        self.name_label = None
        self.email_label = None
        self.phone_label = None
        self.name_value_label = None
        self.email_value_label = None
        self.phone_value_label = None
        self.address_value_label = None
        self.password_value_label = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI - EXACT COPY FROM ORIGINAL CODE"""
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)

        # Profile header
        header = QFrame()
        header.setFixedHeight(180)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0078F0, stop:1 #00B4F0);
            }
        """)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 30)

        # Back button (top left)
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self.back_requested.emit)

        # Profile info
        profile_info = QVBoxLayout()
        profile_info.setSpacing(5)

        # Create name and email labels
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: white;")

        self.email_label = QLabel()
        self.email_label.setFont(QFont("Arial", 13))
        self.email_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")

        self.phone_label = QLabel()
        self.phone_label.setFont(QFont("Arial", 12))
        self.phone_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")

        profile_info.addWidget(self.name_label)
        profile_info.addWidget(self.email_label)
        profile_info.addWidget(self.phone_label)

        header_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch()
        header_layout.addLayout(profile_info)

        main.addWidget(header)

        # Profile options (scrollable) - Updated with menu scroll bar styling
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
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
            QScrollBar:horizontal {
                height: 8px;
                background: #f0f0f0;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                border-radius: 4px;
                min-width: 25px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)  # Reduced spacing between cards

        # Title for Personal Information Section
        personal_title = QLabel("Personal Information")
        personal_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        personal_title.setStyleSheet("color: #213547; margin-bottom: 5px;")
        content_layout.addWidget(personal_title)

        # Create edit cards for each personal info field
        personal_info_fields = [
            ("Name", "", "picture/user.png", self.edit_name),
            ("Email", "", "picture/email.png", self.edit_email),
            ("Phone", "", "picture/phone.png", self.edit_phone),
            ("Address", "", "picture/address.png", self.edit_address),
            ("Password", "********", "picture/lock.png", self.edit_password)
        ]

        for title, value, icon_path, callback in personal_info_fields:
            card = self.create_info_card(title, value, icon_path, callback)
            content_layout.addWidget(card)

        content_layout.addSpacing(15)

        # Empty space note
        empty_note = QLabel("")
        empty_note.setFont(QFont("Arial", 11))
        empty_note.setStyleSheet("color: #9aa6b2; text-align: center;")
        empty_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(empty_note)

        content_layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedHeight(50)
        logout_btn.setFixedWidth(150)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: #ff6b6b;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: #ff5252;
            }
        """)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.confirm_logout)

        # Add to layout with center alignment
        content_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(content)
        main.addWidget(scroll)

        self.setLayout(main)

        # Initialize with customer info if available
        if self.customer_info:
            self.update_customer_info(self.customer_info)

    def create_info_card(self, title, value, icon_path, callback):
        """Create a card for personal information with edit button - EXACT COPY FROM ORIGINAL"""
        card = QFrame()
        card.setObjectName("info_card")
        card.setFixedHeight(70)  # Reduced height from ~100px to 70px
        card.setStyleSheet("""
            QFrame#info_card {
                background: white;
                border-radius: 10px;  /* Slightly smaller radius */
                border: 1px solid #eef2f6;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)  # Reduced margins
        layout.setSpacing(5)  # Reduced spacing

        # Card header
        header = QHBoxLayout()
        header.setSpacing(8)  # Reduced spacing

        # Icon
        icon = QLabel()
        try:
            icon_pix = QPixmap(icon_path).scaled(
                20, 20, Qt.AspectRatioMode.KeepAspectRatio,  # Smaller icon
                Qt.TransformationMode.SmoothTransformation
            )
            icon.setPixmap(icon_pix)
        except:
            icon.setText("•")
            icon.setFont(QFont("Arial", 10))  # Smaller font for placeholder

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.DemiBold))  # Smaller font
        title_label.setStyleSheet("color: #213547;")

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(50, 25)  # Smaller button
        edit_btn.setStyleSheet("""
            QPushButton {
                background: #f0f8ff;
                color: #0080ff;
                border: 1px solid #cce5ff;
                border-radius: 6px;  /* Smaller radius */
                font-size: 10px;  /* Smaller font */
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e1f0ff;
            }
        """)
        edit_btn.clicked.connect(callback)

        header.addWidget(icon)
        header.addWidget(title_label)
        header.addStretch()
        header.addWidget(edit_btn)

        # Value (this will be updated when customer info is loaded)
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 11))  # Smaller font
        value_label.setStyleSheet("color: #55606a;")
        value_label.setWordWrap(True)
        value_label.setMaximumHeight(30)  # Limit height for value text

        # Store reference to value label for updating
        if title == "Name":
            self.name_value_label = value_label
        elif title == "Email":
            self.email_value_label = value_label
        elif title == "Phone":
            self.phone_value_label = value_label
        elif title == "Address":
            self.address_value_label = value_label
        elif title == "Password":
            self.password_value_label = value_label

        layout.addLayout(header)
        layout.addWidget(value_label)

        return card

    def edit_name(self):
        """Edit name functionality - EXACT COPY FROM ORIGINAL"""
        if not self.customer_info or 'id' not in self.customer_info:
            self.show_message("Error", "No customer information available.", QMessageBox.Icon.Warning)
            return

        current_name = self.customer_info.get('full_name', '')

        # Create input dialog with black text
        dialog = QInputDialog()
        dialog.setWindowTitle("Edit Name")
        dialog.setLabelText("Enter your full name:")
        dialog.setTextValue(current_name)

        # Set minimum size for better visibility
        dialog.setMinimumWidth(400)

        # Apply styling with black font and consistent button styling
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: normal;
                padding: 10px;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #2ea1ff;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2ea1ff;
            }
            QPushButton {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: normal;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        ok = dialog.exec()
        new_name = dialog.textValue()

        if ok and new_name.strip():
            # Emit signal for controller to handle
            self.profile_edit_requested.emit('name', new_name.strip(), "")

    def edit_email(self):
        """Edit email functionality - EXACT COPY FROM ORIGINAL"""
        if not self.customer_info or 'id' not in self.customer_info:
            self.show_message("Error", "No customer information available.", QMessageBox.Icon.Warning)
            return

        current_email = self.customer_info.get('email', '')

        # Create input dialog with black text
        dialog = QInputDialog()
        dialog.setWindowTitle("Edit Email")
        dialog.setLabelText("Enter your email address:")
        dialog.setTextValue(current_email)

        # Set minimum size for better visibility
        dialog.setMinimumWidth(400)

        # Apply styling with black font and consistent button styling
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: normal;
                padding: 10px;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #2ea1ff;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2ea1ff;
            }
            QPushButton {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: normal;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        ok = dialog.exec()
        new_email = dialog.textValue()

        if ok and new_email.strip():
            # Basic email validation
            if '@' not in new_email or '.' not in new_email:
                self.show_message("Invalid Email", "Please enter a valid email address.", QMessageBox.Icon.Warning)
                return

            # Emit signal for controller to handle
            self.profile_edit_requested.emit('email', new_email.strip(), "")

    def edit_phone(self):
        """Edit phone functionality - EXACT COPY FROM ORIGINAL"""
        if not self.customer_info or 'id' not in self.customer_info:
            self.show_message("Error", "No customer information available.", QMessageBox.Icon.Warning)
            return

        current_phone = self.customer_info.get('phone', '')

        # Create input dialog with black text
        dialog = QInputDialog()
        dialog.setWindowTitle("Edit Phone Number")
        dialog.setLabelText("Enter your phone number:")
        dialog.setTextValue(current_phone)

        # Set minimum size for better visibility
        dialog.setMinimumWidth(400)

        # Apply styling with black font and consistent button styling
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: normal;
                padding: 10px;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #2ea1ff;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2ea1ff;
            }
            QPushButton {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: normal;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        ok = dialog.exec()
        new_phone = dialog.textValue()

        if ok and new_phone.strip():
            # Emit signal for controller to handle
            self.profile_edit_requested.emit('phone', new_phone.strip(), "")

    def edit_address(self):
        """Edit address functionality - EXACT COPY FROM ORIGINAL"""
        if not self.customer_info or 'id' not in self.customer_info:
            self.show_message("Error", "No customer information available.", QMessageBox.Icon.Warning)
            return

        current_address = self.customer_info.get('address', '')

        # Create a custom styled input dialog with black text
        dialog = QInputDialog()
        dialog.setWindowTitle("Edit Address")
        dialog.setLabelText("Enter your new delivery address:")
        dialog.setTextValue(current_address)

        # Set minimum size for better visibility
        dialog.setMinimumWidth(400)

        # Apply styling with black font and consistent button styling
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                font-weight: normal;
                padding: 10px;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #2ea1ff;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2ea1ff;
            }
            QPushButton {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: normal;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

        ok = dialog.exec()
        new_address = dialog.textValue()

        if ok and new_address.strip():
            # Emit signal for controller to handle
            self.profile_edit_requested.emit('address', new_address.strip(), "")

    def edit_password(self):
        """Edit password functionality with show/hide toggle - EXACT COPY FROM ORIGINAL"""
        if not self.customer_info or 'id' not in self.customer_info:
            self.show_message("Error", "No customer information available.", QMessageBox.Icon.Warning)
            return

        # Create a custom dialog for password change
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Password")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2ea1ff;
            }
            QPushButton {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: normal;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 1px solid #999;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border: 1px solid #999999;
                color: #666666;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Current password
        current_label = QLabel("Current Password:")
        current_input = QLineEdit()
        current_input.setEchoMode(QLineEdit.EchoMode.Password)
        current_input.setPlaceholderText("Enter your current password")

        # Create show/hide button for current password
        current_password_row = QHBoxLayout()
        current_password_row.addWidget(current_input)

        show_current_pass_btn = QPushButton()
        show_current_pass_btn.setCheckable(True)
        show_current_pass_btn.setFixedSize(25, 25)
        show_current_pass_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)

        try:
            show_current_pass_btn.setIcon(QIcon("picture/hide.png"))
        except:
            show_current_pass_btn.setText("👁")

        def toggle_current_password(checked):
            if checked:
                current_input.setEchoMode(QLineEdit.EchoMode.Normal)
                try:
                    show_current_pass_btn.setIcon(QIcon("picture/show.png"))
                except:
                    show_current_pass_btn.setText("🙈")
            else:
                current_input.setEchoMode(QLineEdit.EchoMode.Password)
                try:
                    show_current_pass_btn.setIcon(QIcon("picture/hide.png"))
                except:
                    show_current_pass_btn.setText("👁")

        show_current_pass_btn.toggled.connect(toggle_current_password)
        current_password_row.addWidget(show_current_pass_btn)

        layout.addWidget(current_label)
        layout.addLayout(current_password_row)

        # New password
        new_label = QLabel("New Password:")
        new_input = QLineEdit()
        new_input.setEchoMode(QLineEdit.EchoMode.Password)
        new_input.setPlaceholderText("Enter your new password")

        # Create show/hide button for new password
        new_password_row = QHBoxLayout()
        new_password_row.addWidget(new_input)

        show_new_pass_btn = QPushButton()
        show_new_pass_btn.setCheckable(True)
        show_new_pass_btn.setFixedSize(25, 25)
        show_new_pass_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)

        try:
            show_new_pass_btn.setIcon(QIcon("picture/hide.png"))
        except:
            show_new_pass_btn.setText("👁")

        def toggle_new_password(checked):
            if checked:
                new_input.setEchoMode(QLineEdit.EchoMode.Normal)
                try:
                    show_new_pass_btn.setIcon(QIcon("picture/show.png"))
                except:
                    show_new_pass_btn.setText("🙈")
            else:
                new_input.setEchoMode(QLineEdit.EchoMode.Password)
                try:
                    show_new_pass_btn.setIcon(QIcon("picture/hide.png"))
                except:
                    show_new_pass_btn.setText("👁")

        show_new_pass_btn.toggled.connect(toggle_new_password)
        new_password_row.addWidget(show_new_pass_btn)

        layout.addWidget(new_label)
        layout.addLayout(new_password_row)

        # Confirm new password
        confirm_label = QLabel("Confirm New Password:")
        confirm_input = QLineEdit()
        confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_input.setPlaceholderText("Confirm your new password")

        # Create show/hide button for confirm password
        confirm_password_row = QHBoxLayout()
        confirm_password_row.addWidget(confirm_input)

        show_confirm_pass_btn = QPushButton()
        show_confirm_pass_btn.setCheckable(True)
        show_confirm_pass_btn.setFixedSize(25, 25)
        show_confirm_pass_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
        """)

        try:
            show_confirm_pass_btn.setIcon(QIcon("picture/hide.png"))
        except:
            show_confirm_pass_btn.setText("👁")

        def toggle_confirm_password(checked):
            if checked:
                confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
                try:
                    show_confirm_pass_btn.setIcon(QIcon("picture/show.png"))
                except:
                    show_confirm_pass_btn.setText("🙈")
            else:
                confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
                try:
                    show_confirm_pass_btn.setIcon(QIcon("picture/hide.png"))
                except:
                    show_confirm_pass_btn.setText("👁")

        show_confirm_pass_btn.toggled.connect(toggle_confirm_password)
        confirm_password_row.addWidget(show_confirm_pass_btn)

        layout.addWidget(confirm_label)
        layout.addLayout(confirm_password_row)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Change Password")
        cancel_button = QPushButton("Cancel")

        # Style the Change Password button with red background
        ok_button.setStyleSheet("""
            QPushButton {
                background: #ff6b6b;
                color: white;
                border: 1px solid #ff5252;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #ff5252;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border: 1px solid #999999;
                color: #666666;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

        # Connect signals
        def validate_passwords():
            ok_button.setEnabled(
                current_input.text().strip() != "" and
                new_input.text().strip() != "" and
                new_input.text() == confirm_input.text() and
                len(new_input.text()) >= 6
            )

        current_input.textChanged.connect(validate_passwords)
        new_input.textChanged.connect(validate_passwords)
        confirm_input.textChanged.connect(validate_passwords)

        def change_password():
            dialog.accept()
            # Emit signal for controller to handle
            self.profile_edit_requested.emit('password', new_input.text(), current_input.text())

        def cancel():
            dialog.reject()

        ok_button.clicked.connect(change_password)
        cancel_button.clicked.connect(cancel)

        validate_passwords()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Password was changed successfully
            pass

    def confirm_logout(self):
        """Show confirmation dialog before logging out - EXACT COPY FROM ORIGINAL"""
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Make text black
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

        # Set Yes button to red for emphasis
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

        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def show_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Helper method to show messages with black text - EXACT COPY FROM ORIGINAL"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon_type)
        # Make text black
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QPushButton {
                color: white;
                background-color: #2ea1ff;
                border: 1px solid #2ea1ff;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1e90ff;
            }
        """)
        msg.exec()

    def update_customer_info(self, customer_info):
        """Update profile with customer information from database - EXACT COPY FROM ORIGINAL"""
        self.customer_info = customer_info

        if customer_info:
            # Update all fields
            name = customer_info.get('full_name', 'Customer')
            email = customer_info.get('email', 'customer@fooddash.com')
            phone = customer_info.get('phone', 'No phone number')
            address = customer_info.get('address', 'No address saved. Please update your address.')

            # Update header labels
            if self.name_label:
                self.name_label.setText(name)

            if self.email_label:
                self.email_label.setText(email)

            if self.phone_label:
                self.phone_label.setText(phone)

            # Update card value labels
            if hasattr(self, 'name_value_label'):
                self.name_value_label.setText(name)

            if hasattr(self, 'email_value_label'):
                self.email_value_label.setText(email)

            if hasattr(self, 'phone_value_label'):
                self.phone_value_label.setText(phone)

            if hasattr(self, 'address_value_label'):
                self.address_value_label.setText(address)

            if hasattr(self, 'password_value_label'):
                self.password_value_label.setText("********")

        else:
            # Set default values
            if self.name_label:
                self.name_label.setText("Customer")

            if self.email_label:
                self.email_label.setText("customer@fooddash.com")

            if self.phone_label:
                self.phone_label.setText("No phone number")

            if hasattr(self, 'name_value_label'):
                self.name_value_label.setText("Customer")

            if hasattr(self, 'email_value_label'):
                self.email_value_label.setText("customer@fooddash.com")

            if hasattr(self, 'phone_value_label'):
                self.phone_value_label.setText("No phone number")

            if hasattr(self, 'address_value_label'):
                self.address_value_label.setText("No address saved. Please update your address.")

            if hasattr(self, 'password_value_label'):
                self.password_value_label.setText("********")


class BottomNav(QFrame):
    page_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("bottomnav")
        self.setFixedHeight(84)
        self.setStyleSheet("""
            QFrame#bottomnav {
                background:white;
                border-top:1px solid #eef2f6;
            }
        """)
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 6, 20, 6)

        self.nav_items = {}

        self.home_widget = self.create_nav_item("picture/home.png", "Menu")
        self.orders_widget = self.create_nav_item("picture/orders.png", "Orders")
        self.cart_widget = self.create_nav_item("picture/cart.png", "Cart")
        self.profile_widget = self.create_nav_item("picture/profile.png", "Profile")

        layout.addStretch()
        layout.addWidget(self.home_widget)
        layout.addStretch()
        layout.addWidget(self.orders_widget)
        layout.addStretch()
        layout.addWidget(self.cart_widget)
        layout.addStretch()
        layout.addWidget(self.profile_widget)
        layout.addStretch()
        self.setLayout(layout)

        self.set_active("Menu")

    def create_nav_item(self, icon_path, text):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(2)

        icon = QLabel()
        try:
            pix = QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
            icon.setPixmap(pix)
        except:
            icon.setText("•")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(text)
        label.setFont(QFont("Arial", 11))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color:#9aa6b2;")

        layout.addWidget(icon)
        layout.addWidget(label)
        widget.setLayout(layout)

        widget.mousePressEvent = lambda event, t=text: self.on_nav_click(t)
        self.nav_items[text] = label
        return widget

    def on_nav_click(self, nav_item):
        self.set_active(nav_item)
        self.page_changed.emit(nav_item)

    def set_active(self, active_item):
        for name, label in self.nav_items.items():
            if name == active_item:
                label.setStyleSheet("color:#0080ff; font-weight:600;")
            else:
                label.setStyleSheet("color:#9aa6b2;")


class CustomerMenuView(QWidget):
    """Main view class that integrates all components"""

    # Signals
    logout_requested = pyqtSignal()
    add_to_cart_requested = pyqtSignal(str, str, str)  # title, price, img
    filter_category_signal = pyqtSignal(str)
    switch_page_signal = pyqtSignal(str)
    profile_edit_requested = pyqtSignal(str, str, str)  # field, new_value, current_password

    def __init__(self, customer_info=None):
        super().__init__()
        self.setWindowTitle("Food Dash - Grid Menu")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background:#f6f8fb;")

        self.customer_info = customer_info
        self.cart_items = []
        self.orders_items = []
        self.menu_items = []

        self.stack = QStackedWidget()

        # Create components
        self.topbar = TopBar(customer_info)
        self.bottomnav = BottomNav()

        # Menu Page
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Cart Page - FIXED: Remove place_order_callback parameter
        self.cart_page = CartWidget(self.cart_items, self.orders_items, customer_info)
        self.stack.addWidget(self.cart_page)

        # Orders Page
        self.orders_page = OrdersWidget(customer_info)
        self.stack.addWidget(self.orders_page)

        # Profile Page
        self.profile_page = ProfileWidget(customer_info)
        self.stack.addWidget(self.profile_page)

        # Connect signals
        self._connect_signals()

        # Main layout
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        main.addWidget(self.topbar)
        main.addWidget(self.stack)
        main.addWidget(self.bottomnav)

        self.setLayout(main)

    def _connect_signals(self):
        """Connect internal signals"""
        self.topbar.logout_requested.connect(self.logout_requested.emit)
        self.profile_page.logout_requested.connect(self.logout_requested.emit)
        self.profile_page.back_requested.connect(lambda: self.switch_page("Menu"))
        self.profile_page.profile_edit_requested.connect(self.profile_edit_requested.emit)
        self.bottomnav.page_changed.connect(self.switch_page)

    def create_menu_page(self):
        """Create menu page with category filters"""
        page = QWidget()
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)

        # Category section
        self.category_section = self.create_category_section()
        main.addWidget(self.category_section)

        # Scroll area for menu items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
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
            QScrollBar:horizontal {
                height: 8px;
                background: #f0f0f0;
                border-radius: 4px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                border-radius: 4px;
                min-width: 25px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        self.menu_content = QWidget()
        self.menu_grid = QGridLayout(self.menu_content)
        self.menu_grid.setContentsMargins(20, 20, 20, 20)
        self.menu_grid.setSpacing(20)

        scroll.setWidget(self.menu_content)
        main.addWidget(scroll)

        page.setLayout(main)
        return page

    def create_category_section(self):
        """Create category filter buttons"""
        category_widget = QWidget()
        category_widget.setStyleSheet("background: white;")

        category_layout = QVBoxLayout(category_widget)
        category_layout.setContentsMargins(20, 15, 20, 15)
        category_layout.setSpacing(10)

        title = QLabel("Categories")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #213547;")
        category_layout.addWidget(title)

        self.category_button_layout = QHBoxLayout()
        self.category_button_layout.setSpacing(10)

        self.categories = ["All", "Burger", "Sides", "Chicken", "Pizza", "Drinks"]

        for category in self.categories:
            btn = QPushButton(category)
            btn.setFixedHeight(40)

            if category == "All":
                btn.setStyleSheet("""
                    QPushButton {
                        background: #2ea1ff;
                        color: white;
                        border-radius: 20px;
                        padding: 0px 25px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #f0f8ff;
                        color: #2ea1ff;
                        border: 1px solid #cce5ff;
                        border-radius: 20px;
                        padding: 0px 25px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: #e1f0ff;
                    }
                """)

            btn.clicked.connect(lambda checked, cat=category: self._filter_by_category(cat))
            self.category_button_layout.addWidget(btn)

        self.category_button_layout.addStretch()
        category_layout.addLayout(self.category_button_layout)

        return category_widget

    def _filter_by_category(self, category):
        """Handle category filter"""
        self.filter_category_signal.emit(category)

    def display_menu_items(self, menu_items, categories=None):
        """Display menu items in grid"""
        # Clear existing items
        while self.menu_grid.count():
            item = self.menu_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Display new items
        row = 0
        col = 0

        for item in menu_items:
            card = MenuCard(item["img"], item["title"], item["subtitle"], item["price"])
            card.add_to_cart.connect(self.add_to_cart_requested.emit)
            self.menu_grid.addWidget(card, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def switch_page(self, page_name):
        """Switch between pages"""
        if page_name == "Menu":
            self.stack.setCurrentWidget(self.menu_page)
            self.bottomnav.set_active("Menu")
        elif page_name == "Cart":
            self.stack.setCurrentWidget(self.cart_page)
            self.bottomnav.set_active("Cart")
        elif page_name == "Orders":
            self.stack.setCurrentWidget(self.orders_page)
            self.bottomnav.set_active("Orders")
        elif page_name == "Profile":
            self.stack.setCurrentWidget(self.profile_page)
            self.bottomnav.set_active("Profile")

    def update_customer_info(self, customer_info):
        """Update customer information in all components"""
        self.customer_info = customer_info
        self.topbar.update_welcome_text(customer_info)
        self.profile_page.update_customer_info(customer_info)
        self.orders_page.customer_info = customer_info
        self.cart_page.customer_info = customer_info

    def update_category_buttons(self, active_category):
        """Update category button styles"""
        for i in range(self.category_button_layout.count()):
            widget = self.category_button_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                if widget.text() == active_category:
                    widget.setStyleSheet("""
                        QPushButton {
                            background: #2ea1ff;
                            color: white;
                            border-radius: 20px;
                            padding: 0px 25px;
                            font-weight: bold;
                        }
                    """)
                else:
                    widget.setStyleSheet("""
                        QPushButton {
                            background: #f0f8ff;
                            color: #2ea1ff;
                            border: 1px solid #cce5ff;
                            border-radius: 20px;
                            padding: 0px 25px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background: #e1f0ff;
                        }
                    """)

    def get_view(self):
        """Get the QWidget instance"""
        return self