from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class InputDialog(QDialog):
    def __init__(self, title, label_text):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        
        self.label = QLabel(label_text)
        self.layout.addWidget(self.label)
        
        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)

    def get_input(self):
        return self.input_field.text()

class ConfirmationDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Confirmation")
        self.layout = QVBoxLayout()
        
        self.message_label = QLabel(message)
        self.layout.addWidget(self.message_label)
        
        self.confirm_button = QPushButton("OK")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)
        
        self.setLayout(self.layout)

def show_message(message):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.exec_()