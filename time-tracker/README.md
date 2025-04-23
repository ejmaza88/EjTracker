# Time Tracker Application

This is a time tracker application designed for macOS with a graphical user interface (GUI). The application allows users to track their time entries efficiently and effectively.

## Features

- User-friendly GUI for easy interaction
- Ability to start, stop, and save time entries
- Dialogs for user confirmations and input
- Reusable components for consistent design
- Utility functions for date and time manipulation

## Project Structure

```
time-tracker
├── src
│   ├── time_tracker
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── app.py
│   │   ├── gui
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py
│   │   │   ├── dialogs.py
│   │   │   └── components.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── time_entry.py
│   │   ├── controllers
│   │   │   ├── __init__.py
│   │   │   └── tracker_controller.py
│   │   └── utils
│   │       ├── __init__.py
│   │       └── date_utils.py
├── tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_utils.py
├── resources
│   ├── icons
│   │   └── app_icon.icns
│   └── styles
│       └── default.qss
├── setup.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd time-tracker
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/time_tracker/main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.