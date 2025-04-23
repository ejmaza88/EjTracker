from setuptools import setup, find_packages

setup(
    name='time-tracker',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A time tracking application with a GUI for macOS',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5',  # or any other GUI framework you choose
        'pandas',  # if you need pandas for data handling
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'time-tracker= time_tracker.main:main',  # Adjust based on your main function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)