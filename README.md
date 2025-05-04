# Record Store Management System

A Python-based record store management system with MySQL database integration.

## Features

- Customer , Band, Album, Genre, Record Label management
- Order Processing
- Analytics


## Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- setuptools (`pip install setuptools`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ericknief/database_project.git
cd database_project
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```
Note: Make sure to include the dot (.) at the end of the command. This tells pip to install the package from the current directory.
This will install all required dependencies automatically.

4. Set up the database password:
```bash
setup-database
```

## Usage

Start the application:
```bash
record-store
```

## Development

The project uses setuptools for package management. Dependencies are specified in setup.py and will be automatically installed when you run `pip install -e .`

To update dependencies, modify the `install_requires` list in setup.py.
