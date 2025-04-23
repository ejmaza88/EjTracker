from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")

class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("border: 1px solid #ccc; padding: 10px; font-size: 14px;")

class CustomLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 14px; font-weight: bold;")

class VerticalLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def add_widget(self, widget):
        self.layout.addWidget(widget)