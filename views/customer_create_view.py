"""
Customer Create Account View
Handles the UI components and user interactions for account creation
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QLineEdit, QPushButton,
    QScrollArea, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal


class CustomerCreateView(QWidget):
    """View for customer account creation page"""

    # Signals emitted by the view
    create_account_attempted = pyqtSignal(dict)  # form_data dict
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._setup_connections()

    def _init_ui(self):
        """Initialize UI components"""
        self.setStyleSheet("background-color: #f4f8ff;")

        # Main layout + scroll area
        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card container
        card = QFrame()
        card.setFixedSize(500, 950)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
            }
        """)

        form = QVBoxLayout(card)
        form.setAlignment(Qt.AlignmentFlag.AlignTop)
        form.setContentsMargins(30, 20, 30, 20)
        form.setSpacing(15)

        # Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedSize(60, 30)
        self.back_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #0080ff;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #e0e0e0;
                border-radius: 5px;
            }
        """)

        # Logo
        logo = QLabel()
        try:
            pix = QPixmap("picture/logo.png").scaled(
                100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pix)
        except Exception:
            pass
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titles
        title = QLabel("Join Food Dash Today")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Create Account")
        sub.setFont(QFont("Arial", 12))
        sub.setStyleSheet("color: gray;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input creator
        def create_input(placeholder, echo=None):
            box = QLineEdit()
            box.setPlaceholderText(placeholder)
            if echo is not None:
                box.setEchoMode(echo)
            box.setFixedHeight(40)
            box.setMinimumWidth(400)
            box.setStyleSheet("""
                QLineEdit {
                    border-radius: 12px;
                    border: 1px solid #bfbfbf;
                    background: #f9fafc;
                    padding-left: 12px;
                    font-size: 14px;
                    color: black;
                }
                QLineEdit:focus {
                    border: 1px solid #4aa3ff;
                }
            """)
            return box

        def create_label(text):
            label = QLabel(text)
            label.setFont(QFont("Arial", 12))
            label.setStyleSheet("color: black;")
            return label

        # Helper for show/hide icon button
        def add_password_toggle(line_edit):
            toggle_btn = QPushButton()
            toggle_btn.setCheckable(True)
            toggle_btn.setFixedSize(25, 25)
            toggle_btn.setStyleSheet("border: none;")
            toggle_btn.setIcon(QIcon("picture/hide.png"))

            def toggle_password(checked):
                if checked:
                    line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                    toggle_btn.setIcon(QIcon("picture/show.png"))
                else:
                    line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                    toggle_btn.setIcon(QIcon("picture/hide.png"))

            toggle_btn.toggled.connect(toggle_password)
            return toggle_btn

        # Start form fields
        form.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        form.addWidget(logo)
        form.addWidget(title)
        form.addWidget(sub)
        form.addSpacing(10)

        # Full Name
        form.addWidget(create_label("Full Name"))
        self.fullname_input = create_input("Enter your full name")
        form.addWidget(self.fullname_input)

        # Email
        form.addWidget(create_label("Email"))
        self.email_input = create_input("Enter your email")
        form.addWidget(self.email_input)

        # Phone
        form.addWidget(create_label("Phone Number"))
        self.phone_input = create_input("Enter your phone number")
        form.addWidget(self.phone_input)

        # Address
        form.addWidget(create_label("Address"))
        self.address_input = create_input("Enter your address")
        form.addWidget(self.address_input)

        # Password + icon button + error
        form.addWidget(create_label("Password"))

        password_row = QHBoxLayout()
        password_row.setSpacing(8)
        self.password_input = create_input("Create a password", QLineEdit.EchoMode.Password)
        password_row.addWidget(self.password_input)

        self.show_pass_btn = add_password_toggle(self.password_input)
        password_row.addWidget(self.show_pass_btn)
        form.addLayout(password_row)

        self.pass_error_label = QLabel("")
        self.pass_error_label.setStyleSheet("color: red; font-size: 11px;")
        form.addWidget(self.pass_error_label)

        # Confirm Password + icon button + error
        form.addWidget(create_label("Confirm Password"))

        confirm_row = QHBoxLayout()
        confirm_row.setSpacing(8)
        self.confirm_input = create_input("Confirm your password", QLineEdit.EchoMode.Password)
        confirm_row.addWidget(self.confirm_input)

        self.show_confirm_btn = add_password_toggle(self.confirm_input)
        confirm_row.addWidget(self.show_confirm_btn)
        form.addLayout(confirm_row)

        self.confirm_error_label = QLabel("")
        self.confirm_error_label.setStyleSheet("color: red; font-size: 11px;")
        form.addWidget(self.confirm_error_label)

        form.addSpacing(20)

        # Create button
        self.create_btn = QPushButton("Create Account")
        self.create_btn.setFixedHeight(50)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #0080ff;
                color: white;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
        """)
        form.addWidget(self.create_btn)

        # Add card to scroll area
        scroll_layout.addWidget(card)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    def _setup_connections(self):
        """Setup signal-slot connections"""
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.create_btn.clicked.connect(self._on_create_clicked)

    def _on_create_clicked(self):
        """Handle create account button click"""
        form_data = {
            'full_name': self.fullname_input.text().strip(),
            'email': self.email_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'address': self.address_input.text().strip(),
            'password': self.password_input.text(),
            'confirm_password': self.confirm_input.text()
        }
        self.create_account_attempted.emit(form_data)

    def clear_fields(self):
        """Clear all input fields and error messages"""
        self.fullname_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.clear_error_messages()

    def clear_error_messages(self):
        """Clear all error messages"""
        self.pass_error_label.setText("")
        self.confirm_error_label.setText("")

    def set_error_message(self, field: str, message: str):
        """
        Set error message for specific field

        Args:
            field: Field name ('password' or 'confirm')
            message: Error message to display
        """
        if field == 'password':
            self.pass_error_label.setText(message)
            self.password_input.setStyleSheet("""
                QLineEdit {
                    border-radius: 12px;
                    border: 2px solid red;
                    background: #f9fafc;
                    padding-left: 12px;
                    font-size: 14px;
                    color: black;
                }
            """)
        elif field == 'confirm':
            self.confirm_error_label.setText(message)
            self.confirm_input.setStyleSheet("""
                QLineEdit {
                    border-radius: 12px;
                    border: 2px solid red;
                    background: #f9fafc;
                    padding-left: 12px;
                    font-size: 14px;
                    color: black;
                }
            """)

    def reset_field_styles(self):
        """Reset all field styles to default"""
        style = """
            QLineEdit {
                border-radius: 12px;
                border: 1px solid #bfbfbf;
                background: #f9fafc;
                padding-left: 12px;
                font-size: 14px;
                color: black;
            }
            QLineEdit:focus {
                border: 1px solid #4aa3ff;
            }
        """
        self.fullname_input.setStyleSheet(style)
        self.email_input.setStyleSheet(style)
        self.phone_input.setStyleSheet(style)
        self.address_input.setStyleSheet(style)
        self.password_input.setStyleSheet(style)
        self.confirm_input.setStyleSheet(style)

    def show_error_message(self, title: str, message: str):
        """Display error message to user"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
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

    def show_success_message(self, title: str, message: str):
        """Display success message to user"""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
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