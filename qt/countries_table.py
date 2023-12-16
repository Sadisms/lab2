from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout
)


class CountriesTable(QMainWindow):
    def __init__(
            self,
            countries: list[dict],
            headers: list[str],
            onDelete=None,
            onEdit=None,
            onCreate=None,
            read_only_values=None
    ):
        super().__init__()

        self.onEdit = onEdit
        self.onCreate = onCreate
        self.onDelete = onDelete
        self.headers = headers
        self.read_only_values = read_only_values

        self.setWindowTitle('Countries table')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.table_widget = QTableWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.table_widget)

        len_countries = len(countries)

        if len_countries > 0:
            self.table_widget.setColumnCount(len(countries[0]) + 1)

        self.table_widget.setRowCount(len_countries)

        self.table_widget.setHorizontalHeaderLabels([
            header.capitalize().replace('_', ' ')
            for header in headers
        ] + ['Actions'])

        for row_idx, row_data in enumerate(countries):
            for col_idx, key in enumerate(headers):
                item = QTableWidgetItem(str(row_data[key]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable & Qt.ItemFlag.ItemIsEnabled)
                self.table_widget.setItem(row_idx, col_idx, item)

                self.create_action_buttons(row_idx, row_data)

        self.add_button = QPushButton('Add country', self)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        self.central_layout.addLayout(button_layout)
        self.add_button.clicked.connect(self.add_row)

        self.table_widget.resizeColumnsToContents()

    def create_action_buttons(self, row_idx, row_data):
        actions_widget = QWidget(self)
        actions_layout = QHBoxLayout(actions_widget)

        delete_button = QPushButton('Delete', actions_widget)
        delete_button.setFixedSize(50, 20)
        delete_button.clicked.connect(lambda state, row=row_idx, row_data=row_data: self.delete_row(row, row_data))
        actions_layout.addWidget(delete_button)

        edit_button = QPushButton('Edit', actions_widget)
        edit_button.setFixedSize(50, 20)
        edit_button.clicked.connect(lambda state, row=row_idx: self.edit_row(row))
        actions_layout.addWidget(edit_button)

        self.table_widget.setCellWidget(row_idx, self.table_widget.columnCount() - 1, actions_widget)

    def add_row(self):
        current_row_count = self.table_widget.rowCount()

        self.table_widget.insertRow(current_row_count)

        for col_idx in range(self.table_widget.columnCount() - 1):
            item = QTableWidgetItem('')
            self.table_widget.setItem(current_row_count, col_idx, item)

        self.create_save_button(current_row_count, True)

    def delete_row(self, row: int, row_data: dict) -> None:
        self.table_widget.removeRow(row)

        if callable(self.onDelete):
            self.onDelete(**row_data)

    def create_save_button(self, row, is_create=False):
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(lambda state, row=row, is_create=is_create: self.save_row(row, is_create))
        self.table_widget.setCellWidget(row, self.table_widget.columnCount() - 1, save_button)

    def edit_row(self, row):
        for col_idx in range(self.table_widget.columnCount() - 1):
            if self.read_only_values:
                if self.headers[col_idx] in self.read_only_values:
                    continue

            item = self.table_widget.item(row, col_idx)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

        self.create_save_button(row)

    def save_row(self, row_idx, is_create=False):
        row_data = {}

        for col_idx in range(self.table_widget.columnCount() - 1):
            item = self.table_widget.item(row_idx, col_idx)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable & Qt.ItemFlag.ItemIsEnabled)
            row_data[self.headers[col_idx]] = item.text()

        self.create_action_buttons(row_idx, row_data)

        try:
            if is_create:
                if callable(self.onCreate):
                    self.onCreate(**row_data)

            else:
                if callable(self.onEdit):
                    self.onEdit(**row_data)

        except Exception as e:
            print(e)
