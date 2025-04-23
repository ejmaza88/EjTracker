from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, QToolBar, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.create_menus()
        self.create_toolbar()
        self.create_central_widget()

    def create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        start_action = QAction("Start", self)
        start_action.triggered.connect(self.start_tracking)
        toolbar.addAction(start_action)

        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.stop_tracking)
        toolbar.addAction(stop_action)

    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Time Tracker!")
        layout.addWidget(self.label)

        central_widget.setLayout(layout)

    def start_tracking(self):
        self.label.setText("Tracking started...")

    def stop_tracking(self):
        self.label.setText("Tracking stopped.")