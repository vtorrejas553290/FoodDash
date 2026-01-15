"""
Staff Login View
Handles the UI components and user interactions for staff login
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal


class StaffLoginView(QWidget):
    """View for staff login page"""

    # Signals emitted by the view
    login_attempted = pyqtSignal(str, str)  # identifier, password
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init_ui()
        self._setup_connections()

    def _init_ui(self):
        """Initialize UI components"""
        self.setStyleSheet("background-color: #f4f8ff;")

        main = QVBoxLayout()
        main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
            }
        """)
        container.setFixedSize(450, 650)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        pix = QPixmap("picture/logo.png").scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo.setPixmap(pix)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texts
        title = QLabel("Staff Portal")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Staff Login")
        sub.setFont(QFont("Arial", 11))
        sub.setStyleSheet("color: gray;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Staff ID or Email
        id_label = QLabel("Staff ID or Email")
        id_label.setFont(QFont("Arial", 12))
        id_label.setStyleSheet("color: black;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.identifier_input = QLineEdit()
        self.identifier_input.setPlaceholderText("Enter your Staff ID or Email")
        self.identifier_input.setFixedHeight(40)
        self.identifier_input.setMinimumWidth(350)
        self.identifier_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                border: 1px solid #e3e3e3;
                padding-left: 10px;
                color: black;
            }
        """)

        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("color: black;")
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setMinimumWidth(350)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                border: 1px solid #e3e3e3;
                padding-left: 10px;
                color: black;
            }
        """)

        # Show/Hide password button
        password_row = QHBoxLayout()
        password_row.setSpacing(5)
        password_row.addWidget(self.password_input)

        self.show_pass_btn = QPushButton()
        self.show_pass_btn.setCheckable(True)
        self.show_pass_btn.setFixedSize(25, 25)
        self.show_pass_btn.setStyleSheet("border: none;")
        self.show_pass_btn.setIcon(QIcon("picture/hide.png"))

        password_row.addWidget(self.show_pass_btn)

        # Login button
        self.login_btn = QPushButton("Login as Staff")
        self.login_btn.setFixedHeight(50)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b6bff;
                color: white;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #8a5cff;
            }
        """)

        # Layout
        layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addSpacing(5)
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(id_label)
        layout.addWidget(self.identifier_input)
        layout.addWidget(password_label)
        layout.addLayout(password_row)
        layout.addSpacing(15)
        layout.addWidget(self.login_btn)

        container.setLayout(layout)
        main.addWidget(container)
        self.setLayout(main)

    def _setup_connections(self):
        """Setup signal-slot connections"""
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.login_btn.clicked.connect(self._on_login_clicked)
        self.show_pass_btn.toggled.connect(self._toggle_password_visibility)

    def _on_login_clicked(self):
        """Handle login button click"""
        identifier = self.identifier_input.text().strip()
        password = self.password_input.text().strip()
        self.login_attempted.emit(identifier, password)

    def _toggle_password_visibility(self, checked: bool):
        """Toggle password visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_pass_btn.setIcon(QIcon("picture/show.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_pass_btn.setIcon(QIcon("picture/hide.png"))

    def clear_fields(self):
        """Clear all input fields"""
        self.identifier_input.clear()
        self.password_input.clear()

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