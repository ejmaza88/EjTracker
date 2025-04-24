from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                            QHeaderView, QTabWidget)
from PyQt6.QtCore import Qt
import pandas as pd
import os
from pathlib import Path
import datetime
import re

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Path to time entries CSV file
        self.csv_path = Path.home() / ".time_tracker" / "time_entries.csv"
        
        # Initialize UI components
        self.init_ui()
        
        # Load data if CSV exists
        if os.path.exists(self.csv_path):
            self.load_data()
        
    def init_ui(self):
        self.setWindowTitle("Time Tracker Dashboard")
        self.setFixedSize(800, 600)
        
        # Set window to appear on top of other windows
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Create central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = QWidget()
        header.setStyleSheet("background-color: #8E5BB6;")
        header.setFixedHeight(30)
        main_layout.addWidget(header)
        
        # Create content area
        content = QWidget()
        content.setStyleSheet("background-color: #3A3A47; color: white;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Filters section
        filter_layout = QHBoxLayout()
        
        # Month dropdown
        month_layout = QVBoxLayout()
        month_label = QLabel("Month:")
        month_label.setStyleSheet("font-size: 14px;")
        self.month_combo = QComboBox()
        self.month_combo.setStyleSheet("""
            QComboBox {
                background-color: #2D2D38;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                min-width: 150px;
            }
            QComboBox QAbstractItemView {
                background-color: #2D2D38;
                color: white;
                selection-background-color: #8E5BB6;
            }
        """)
        self.month_combo.currentIndexChanged.connect(self.update_dashboard)
        month_layout.addWidget(month_label)
        month_layout.addWidget(self.month_combo)
        
        # Year dropdown
        year_layout = QVBoxLayout()
        year_label = QLabel("Year:")
        year_label.setStyleSheet("font-size: 14px;")
        self.year_combo = QComboBox()
        self.year_combo.setStyleSheet("""
            QComboBox {
                background-color: #2D2D38;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox QAbstractItemView {
                background-color: #2D2D38;
                color: white;
                selection-background-color: #8E5BB6;
            }
        """)
        self.year_combo.currentIndexChanged.connect(self.update_dashboard)
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_combo)
        
        # Add filter components to filter layout
        filter_layout.addLayout(month_layout)
        filter_layout.addLayout(year_layout)
        filter_layout.addStretch()
        
        # Add filter layout to content layout
        content_layout.addLayout(filter_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #2D2D38;
            }
            QTabBar::tab {
                background-color: #1E1E28;
                color: white;
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #8E5BB6;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3A3A47;
            }
        """)
        
        # Create aggregate tab
        aggregate_tab = QWidget()
        aggregate_layout = QVBoxLayout(aggregate_tab)
        aggregate_layout.setContentsMargins(5, 10, 5, 5)
        
        # Table for aggregated time entries
        self.aggregate_table = QTableWidget()
        self.aggregate_table.setStyleSheet("""
            QTableWidget {
                background-color: #2D2D38;
                color: white;
                border: 1px solid #555;
                gridline-color: #555;
            }
            QTableWidget::item:selected {
                background-color: #8E5BB6;
            }
            QHeaderView::section {
                background-color: #1E1E28;
                color: white;
                padding: 5px;
                border: 1px solid #555;
            }
        """)
        self.aggregate_table.setColumnCount(2)
        self.aggregate_table.setHorizontalHeaderLabels(["Date", "Total Hours"])
        self.aggregate_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        aggregate_layout.addWidget(self.aggregate_table)
        
        # Create raw tab
        raw_tab = QWidget()
        raw_layout = QVBoxLayout(raw_tab)
        raw_layout.setContentsMargins(5, 10, 5, 5)
        
        # Table for raw time entries
        self.raw_table = QTableWidget()
        self.raw_table.setStyleSheet("""
            QTableWidget {
                background-color: #2D2D38;
                color: white;
                border: 1px solid #555;
                gridline-color: #555;
            }
            QTableWidget::item:selected {
                background-color: #8E5BB6;
            }
            QHeaderView::section {
                background-color: #1E1E28;
                color: white;
                padding: 5px;
                border: 1px solid #555;
            }
        """)
        self.raw_table.setColumnCount(4)
        self.raw_table.setHorizontalHeaderLabels(["Start Time", "End Time", "Duration", "Work Description"])
        
        # Set column widths for raw table (percentage-based)
        self.raw_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Start Time
        self.raw_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # End Time
        self.raw_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Duration
        self.raw_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Work Description
        
        raw_layout.addWidget(self.raw_table)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(aggregate_tab, "Aggregate")
        self.tab_widget.addTab(raw_tab, "Raw")
        
        # Add tab widget to content layout
        content_layout.addWidget(self.tab_widget)
        
        # Add content to main layout
        main_layout.addWidget(content)
        
    def load_data(self):
        try:
            # Load CSV file into pandas DataFrame
            df = pd.read_csv(self.csv_path)
            
            # Print the first few rows for debugging
            print("CSV Data Sample:")
            print(df.head())
            
            # Convert dates from strings to datetime objects
            df['Start Time'] = pd.to_datetime(df['Start Time'], format='%m/%d/%Y %I:%M %p', errors='coerce')
            
            # Handle potential parsing errors
            if df['Start Time'].isna().any():
                print("Warning: Some dates couldn't be parsed. Using alternative format.")
                # Try alternative format
                mask = df['Start Time'].isna()
                df.loc[mask, 'Start Time'] = pd.to_datetime(df.loc[mask, 'Start Time'], errors='ignore')
            
            # Extract month and year from Start Time
            df['Month'] = df['Start Time'].dt.month
            df['Year'] = df['Start Time'].dt.year
            df['Date'] = df['Start Time'].dt.date
            
            # Get unique months and years for dropdowns
            self.df = df  # Store the dataframe for later use
            
            # Populate year dropdown
            years = sorted(df['Year'].unique(), reverse=True)
            self.year_combo.clear()
            for year in years:
                self.year_combo.addItem(str(year), year)
            
            # Populate month dropdown with names instead of numbers
            month_names = {
                1: 'January', 2: 'February', 3: 'March', 4: 'April',
                5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'
            }
            
            months = sorted(df['Month'].unique())
            self.month_combo.clear()
            for month in months:
                self.month_combo.addItem(month_names[month], month)
            
            # Update the dashboard with initial data
            self.update_dashboard()
            
        except Exception as e:
            # If there's an error loading the CSV, display empty dashboard
            print(f"Error loading data: {e}")
            self.aggregate_table.setRowCount(0)
            self.raw_table.setRowCount(0)
    
    def update_dashboard(self):
        if not hasattr(self, 'df') or self.df.empty:
            return
        
        try:
            # Get selected month and year
            month_idx = self.month_combo.currentIndex()
            year_idx = self.year_combo.currentIndex()
            
            if month_idx == -1 or year_idx == -1:
                return
                
            selected_month = self.month_combo.itemData(month_idx)
            selected_year = self.year_combo.itemData(year_idx)
            
            print(f"Selected month: {selected_month}, Selected year: {selected_year}")
            
            # Filter data for selected month and year
            filtered_df = self.df[(self.df['Month'] == selected_month) & 
                                  (self.df['Year'] == selected_year)]
                                  
            print(f"Found {len(filtered_df)} entries for selected month/year")
            
            # Update the raw table with all entries
            self.update_raw_table(filtered_df)
            
            # Update the aggregate table with daily totals
            self.update_aggregate_table(filtered_df)
                
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            import traceback
            traceback.print_exc()
    
    def parse_duration(self, duration_str):
        """Parse duration string into minutes, handling various formats."""
        if not duration_str or pd.isna(duration_str):
            return 0
        
        hours = 0
        minutes = 0
        
        # Handle format like "0h 0m"
        h_match = re.search(r'(\d+)h', duration_str)
        if h_match:
            hours = int(h_match.group(1))
            
        m_match = re.search(r'(\d+)m', duration_str)
        if m_match:
            minutes = int(m_match.group(1))
        
        return hours * 60 + minutes
    
    def update_aggregate_table(self, filtered_df):
        """Update the aggregate table with daily totals."""
        try:
            if filtered_df.empty:
                self.aggregate_table.setRowCount(0)
                return
                
            # Group by date and calculate total hours per day
            daily_totals = {}
            
            for _, row in filtered_df.iterrows():
                # Skip rows with NaN dates
                if pd.isna(row['Date']):
                    continue
                    
                date = row['Date']
                total_minutes = self.parse_duration(row['Duration'])
                
                if date in daily_totals:
                    daily_totals[date] += total_minutes
                else:
                    daily_totals[date] = total_minutes
            
            # Convert daily totals to hours and format them
            formatted_totals = []
            for date, minutes in daily_totals.items():
                hours = minutes / 60
                formatted_hours = f"{int(hours)}h {int((hours - int(hours)) * 60)}m"
                formatted_totals.append((date, formatted_hours))
            
            # Sort by date
            formatted_totals.sort(key=lambda x: x[0])
            
            # Update table
            self.aggregate_table.setRowCount(len(formatted_totals))
            
            for i, (date, hours) in enumerate(formatted_totals):
                # Format date as MM/DD/YYYY
                date_str = date.strftime('%m/%d/%Y') if hasattr(date, 'strftime') else str(date)
                date_item = QTableWidgetItem(date_str)
                hours_item = QTableWidgetItem(hours)
                
                # Center-align items
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                hours_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                self.aggregate_table.setItem(i, 0, date_item)
                self.aggregate_table.setItem(i, 1, hours_item)
        except Exception as e:
            print(f"Error in update_aggregate_table: {e}")
            import traceback
            traceback.print_exc()
    
    def update_raw_table(self, filtered_df):
        """Update the raw table with all entries for the selected month/year."""
        try:
            # Update raw table
            self.raw_table.setRowCount(len(filtered_df))
            
            for i, (_, row) in enumerate(filtered_df.iterrows()):
                # Format start time
                if pd.notna(row['Start Time']):
                    start_time_str = row['Start Time'].strftime('%m/%d/%Y %I:%M %p')
                else:
                    start_time_str = str(row['Start Time'])
                
                # Create table items
                start_time = QTableWidgetItem(start_time_str)
                end_time = QTableWidgetItem(str(row['End Time']))
                duration = QTableWidgetItem(str(row['Duration']))
                description = QTableWidgetItem(str(row['Work Description']))
                
                # Set alignment
                start_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                end_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                duration.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                description.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
                # Add items to table
                self.raw_table.setItem(i, 0, start_time)
                self.raw_table.setItem(i, 1, end_time)
                self.raw_table.setItem(i, 2, duration)
                self.raw_table.setItem(i, 3, description)
        except Exception as e:
            print(f"Error in update_raw_table: {e}")
            import traceback
            traceback.print_exc()