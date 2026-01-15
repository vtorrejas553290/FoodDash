"""
Home View
Main landing page with role selection cards
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from .widgets.role_card import RoleCard


class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f4f8ff;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo = QLabel()
        pix = QPixmap("picture/logo.png")
        if not pix.isNull():
            pix = pix.scaled(130, 130, Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pix)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("background: transparent; border: none;")

        # Title
        title = QLabel("Food Dash")
        title.setFont(QFont("Arial", 34, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0080ff; background: transparent; border: none;")

        # Subtitle
        subtitle = QLabel("Select your role to continue")
        subtitle.setFont(QFont("Arial", 15))
        subtitle.setStyleSheet("color: gray; background: transparent; border: none;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Role cards layout
        card_layout = QHBoxLayout()
        card_layout.setSpacing(40)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create role cards
        self.customer_card = RoleCard("picture/customer.png", "Customer",
                                      "Browse menu and place orders", "#4aa3ff")
        self.staff_card = RoleCard("picture/staff.png", "Staff",
                                   "Manage menu and orders", "#9b6bff")
        self.admin_card = RoleCard("picture/admin.png", "Admin",
                                   "Full system management", "#4F39F6")

        # Add cards to layout
        card_layout.addWidget(self.customer_card)
        card_layout.addWidget(self.staff_card)
        card_layout.addWidget(self.admin_card)

        # Assemble the page
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(40)
        layout.addLayout(card_layout)

        self.setLayout(layout)