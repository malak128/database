# E-commerce Python GUI Project

## Description
A Python GUI application for managing an E-commerce database using SQL Server.

## Requirements
- Python 3.x
- PySide6
- pyodbc
- SQL Server

## Setup
1. Create the database:
   - Open SQL Server Management Studio (SSMS).
   - Run the `database.sql` file to create tables and insert initial data.

2. Install Python dependencies:
```bash
pip install -r requirements.txt

3. Update the database connection in gui.py if needed:

conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=YOUR_SERVER_NAME;DATABASE=E-commerce;Trusted_Connection=yes;'
)

4. Run the GUI:

python gui.py
