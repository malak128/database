from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QInputDialog
)
import sys
import pyodbc

# Connect to the database
conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=YOUR_SERVER_NAME;DATABASE=E-commerce;Trusted_Connection=yes;'
)

primary_keys = {
    'customers': 'cust_id',
    'categories': 'category_id',
    'products': 'prod_id',
    'orders': 'order_id',
    'cust_cart': 'cart_id',
    'cart_include_products': 'cart_prod_id',
    'shipment': 'shipment_id',
    'payment': 'transaction_id',
    'order_items': 'order_item_id'
}

class TableSelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Table Selection')
        self.resize(800, 600)
        layout = QVBoxLayout()
        self.tableComboBox = QComboBox()
        self.tableComboBox.addItems(primary_keys.keys())
        layout.addWidget(self.tableComboBox)
        self.openButton = QPushButton('Open Table')
        self.openButton.clicked.connect(self.open_table)
        layout.addWidget(self.openButton)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                background-color: #121212;
            }
            QComboBox, QLineEdit, QTableWidget, QPushButton {
                color: rgb(244, 236, 236);
                background-color: #333333;
                border: 1px solid rgb(102, 17, 88);
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #ff007f;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff3399;
            }
        """)

    def open_table(self):
        table_name = self.tableComboBox.currentText()
        self.hide()
        self.crud_window = CRUDWindow(table_name)
        self.crud_window.show()


class CRUDWindow(QMainWindow):
    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name
        self.primary_key = primary_keys[table_name]
        self.setWindowTitle(f'CRUD Operations - {table_name}')
        self.resize(1000, 700)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        self.pkLineEdit = QLineEdit()
        self.pkLineEdit.setPlaceholderText(f'Enter {self.primary_key}')
        search_layout.addWidget(self.pkLineEdit)

        self.searchButton = QPushButton('Search')
        self.searchButton.setFixedWidth(100)
        self.searchButton.clicked.connect(self.search_row)
        search_layout.addWidget(self.searchButton)

        navigation_layout = QHBoxLayout()
        self.prevButton = QPushButton('<')
        self.prevButton.clicked.connect(self.previous_row)
        navigation_layout.addWidget(self.prevButton)

        self.nextButton = QPushButton('>')
        self.nextButton.clicked.connect(self.next_row)
        navigation_layout.addWidget(self.nextButton)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(navigation_layout)

        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.tableWidget)

        button_layout = QHBoxLayout()
        for label, handler in [
            ("Edit", self.edit_row),
            ("Add", self.add_row),
            ("Delete", self.delete_row),
            ("Back", self.go_back)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.current_index = 0
        self.search_index = -1
        self.load_data()
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
            }
            QComboBox, QLineEdit, QTableWidget, QPushButton {
                color: white;
                background-color: #333333;
                border: 1px solid rgb(102, 17, 71);
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #ff007f;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff3399;
            }
        """)

    def display_row(self, index):
        if index < 0 or index >= len(self.data):
            return
        row_data = self.data[index]
        self.tableWidget.setRowCount(1)
        for col, data in enumerate(row_data):
            self.tableWidget.setItem(0, col, QTableWidgetItem(str(data)))

    def search_row(self):
        pk = self.pkLineEdit.text().strip()
        if pk:
            query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?"
            cursor = conn.cursor()
            cursor.execute(query, (pk,))
            result = cursor.fetchone()
            if result:
                self.tableWidget.setRowCount(1)
                self.tableWidget.setColumnCount(len(result))
                for col, data in enumerate(result):
                    self.tableWidget.setItem(0, col, QTableWidgetItem(str(data)))
                self.search_index = self.get_row_index(result)
                self.current_index = self.search_index
            else:
                QMessageBox.information(self, "Search Result", "No row found with the given primary key.")
        else:
            QMessageBox.warning(self, "Input Error", "Primary key cannot be empty.")

    def get_row_index(self, row):
        for index, data in enumerate(self.data):
            if data == row:
                return index
        return -1

    def add_row(self):
        cursor = conn.cursor()
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.table_name}'"
        cursor.execute(query)
        columns = [column[0] for column in cursor.fetchall()]
        values = []
        for col in columns:
            value, ok = QInputDialog.getText(self, 'Input Dialog', f'Enter value for {col}:')
            if ok:
                values.append(value)
            else:
                return
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        try:
            cursor.execute(query, values)
            conn.commit()
            self.load_data()
        except pyodbc.IntegrityError as e:
            QMessageBox.critical(self, "Integrity Error", str(e))

    def delete_row(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            try:
                pk_value = self.tableWidget.item(selected_row, 0).text()
                query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
                cursor = conn.cursor()
                cursor.execute(query, (pk_value,))
                conn.commit()
                self.load_data()
                QMessageBox.information(self, "Success", f"Deleted row with {self.primary_key} = {pk_value}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "No Row Selected", "Please select a row to delete.")

    def edit_row(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            columns = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]
            column, ok = QInputDialog.getItem(self, 'Select Column', 'Select column to edit:', columns, 0, False)
            if ok and column:
                current_value = self.tableWidget.item(selected_row, columns.index(column)).text()
                new_value, ok = QInputDialog.getText(self, 'Edit Dialog', f'New value for {column}:', text=current_value)
                if ok:
                    pk_value = self.tableWidget.item(selected_row, 0).text()
                    query = f"UPDATE {self.table_name} SET {column} = ? WHERE {self.primary_key} = ?"
                    cursor = conn.cursor()
                    cursor.execute(query, (new_value, pk_value))
                    conn.commit()
                    self.load_data()
                    QMessageBox.information(self, "Success", "Row updated successfully.")
        else:
            QMessageBox.warning(self, "No Row Selected", "Please select a row to edit.")

    def previous_row(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_row(self.current_index)
        else:
            QMessageBox.warning(self, "Navigation", "You are already at the first row.")

    def next_row(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.display_row(self.current_index)
        else:
            QMessageBox.warning(self, "Navigation", "You are already at the last row.")

    def load_data(self):
        cursor = conn.cursor()
        query = f"SELECT * FROM {self.table_name}"
        cursor.execute(query)
        self.data = cursor.fetchall()
        self.headers = [column[0] for column in cursor.description]
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setRowCount(len(self.data))
        for row_idx, row_data in enumerate(self.data):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def go_back(self):
        self.hide()
        self.table_selection_window = TableSelectionWindow()
        self.table_selection_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TableSelectionWindow()
    mainWin.show()
    sys.exit(app.exec())

