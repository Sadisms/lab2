import sys

from PyQt6.QtWidgets import QApplication

from db import db_worker
from qt.countries_table import CountriesTable


def main():
    db_worker.init_tables()

    app = QApplication(sys.argv)

    window = CountriesTable(
        countries=db_worker.get_countries(),
        headers=db_worker.get_countries_header_table(),
        onDelete=db_worker.delete_country,
        onEdit=db_worker.edit_country,
        onCreate=db_worker.create_country,
        read_only_values=['code']
    )

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
