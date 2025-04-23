from setuptools import setup, find_packages

setup(
    name="time_tracker",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rumps>=0.4.0",
        "PyQt6>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "time_tracker=time_tracker.main:main",
        ],
    },
)