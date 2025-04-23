from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTextEdit, QPushButton, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QKeyEvent
import datetime
import csv
import os
from pathlib import Path

class TimeTrackerWindow(QMainWindow):
    def __init__(self, start_time, end_time):
        super().__init__()
        
        # Convert times to readable format with AM/PM
        self.start_time = start_time
        self.end_time = end_time
        self.start_time_str = start_time.strftime("%m/%d/%Y %I:%M %p")
        self.end_time_str = end_time.strftime("%m/%d/%Y %I:%M %p")
        
        # Calculate duration in minutes
        duration = end_time - start_time
        total_minutes = int(duration.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        self.total_time_str = f"{hours}h {minutes}m"
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Time Tracker")
        self.setFixedSize(600, 450)
        
        # Set window to appear on top of other windows
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Create central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header - thinner without text
        header = QWidget()
        header.setStyleSheet("background-color: #8E5BB6;")
        
        # Reduce header height from 80px to 30px
        header.setFixedHeight(30)
        main_layout.addWidget(header)
        
        # Create content area
        content = QWidget()
        content.setStyleSheet("background-color: #3A3A47; color: white;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        # Reduce spacing between items in the main layout
        content_layout.setSpacing(5)
        
        # Time information
        time_layout = QHBoxLayout()
        time_layout.setSpacing(5)
        
        # Start time
        start_layout = QVBoxLayout()
        start_layout.setSpacing(2)  # Tight spacing between label and value
        start_label = QLabel("Start Time:")
        start_label.setStyleSheet("font-size: 14px;")
        start_value = QLabel(self.start_time_str)
        start_value.setStyleSheet("font-size: 14px;")
        start_layout.addWidget(start_label)
        start_layout.addWidget(start_value)
        
        # End time
        end_layout = QVBoxLayout()
        end_layout.setSpacing(2)  # Tight spacing between label and value
        end_label = QLabel("End Time:")
        end_label.setStyleSheet("font-size: 14px;")
        end_value = QLabel(self.end_time_str)
        end_value.setStyleSheet("font-size: 14px;")
        end_layout.addWidget(end_label)
        end_layout.addWidget(end_value)
        
        time_layout.addLayout(start_layout)
        time_layout.addLayout(end_layout)
        content_layout.addLayout(time_layout)
        
        # Total time
        total_label = QLabel("Total Time:")
        total_label.setStyleSheet("font-size: 14px;")
        content_layout.addWidget(total_label)
        
        total_value = QLabel(self.total_time_str)
        total_value.setStyleSheet("font-size: 14px;")
        content_layout.addWidget(total_value)
        total_value.setContentsMargins(0, 0, 0, 2)  # Add a small bottom margin
        
        # Work done - directly add widgets to content layout
        work_label = QLabel("Work Done:")
        work_label.setStyleSheet("font-size: 14px;")
        # Set a small top margin to create separation
        work_label.setContentsMargins(0, 3, 0, 0)
        content_layout.addWidget(work_label)
        
        self.work_edit = QTextEdit()
        self.work_edit.setStyleSheet("background-color: #2D2D38; color: white; border: 1px solid #555;")
        self.work_edit.setFixedHeight(170)
        # No margin for the text edit
        self.work_edit.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.work_edit)
        
        # Button section
        button_layout = QHBoxLayout()
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ADADAD;
                color: black;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #999999;
            }
        """)
        self.cancel_btn.setFixedSize(180, 40)
        self.cancel_btn.clicked.connect(self.close)
        
        # Save button
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #ADADAD;
                color: black;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #999999;
            }
        """)
        self.save_btn.setFixedSize(180, 40)
        self.save_btn.clicked.connect(self.save_entry)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        
        # Add some spacing before buttons
        content_layout.addSpacing(5)
        content_layout.addLayout(button_layout)
        main_layout.addWidget(content)
        
    def save_entry(self):
        """Save the time entry to a CSV file"""
        # Get the work description
        work_description = self.work_edit.toPlainText()
        
        # Prepare data for CSV
        data = [
            self.start_time_str,
            self.end_time_str,
            self.total_time_str,
            work_description
        ]
        
        # Ensure data directory exists
        csv_path = Path.home() / ".time_tracker" / "time_entries.csv"
        os.makedirs(csv_path.parent, exist_ok=True)
        
        # Check if file exists to determine if we need headers
        file_exists = csv_path.exists()
        
        # Write to CSV
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Start Time", "End Time", "Duration", "Work Description"])
            writer.writerow(data)
            
        self.close()
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events, specifically for Enter/Return key to save"""
        # Check if Return/Enter key is pressed (not in text edit mode)
        if event.key() == Qt.Key.Key_Return and not self.work_edit.hasFocus():
            self.save_entry()
        else:
            super().keyPressEvent(event)
            
    def showEvent(self, event):
        """Override showEvent to set focus to the text area when window appears"""
        super().showEvent(event)
        # Set focus to work description text area
        self.work_edit.setFocus()