import asyncio

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from app.db.database import fetch_history  # Функция для получения данных из БД


class HistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История записей")
        self.setGeometry(200, 200, 600, 400)

        # Основной Layout
        layout = QVBoxLayout()

        # Таблица для отображения данных
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "CPU Load", "RAM Load", "Disk Load", "Timestamp"]
        )

        # Добавляем таблицу в Layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Асинхронная загрузка данных
        asyncio.create_task(self.load_data())

    async def load_data(self):
        """
        Асинхронная загрузка данных из базы данных.
        """
        try:
            history = await fetch_history()  # Асинхронный вызов
            self.table.setRowCount(len(history))
            for row_index, row_data in enumerate(history):
                for col_index, value in enumerate(row_data):
                    self.table.setItem(
                        row_index, col_index, QTableWidgetItem(str(value))
                    )
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")


def show_history():
    """
    Открытие окна истории записей.
    """
    try:
        history_window = HistoryWindow()
        history_window.exec()
    except Exception as e:
        print(f"Ошибка при открытии окна истории: {e}")
