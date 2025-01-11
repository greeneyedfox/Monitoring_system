import asyncio
import os
from pathlib import Path
import psutil

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSpinBox
from PyQt6.QtCore import QTimer, QTime

from app.db.database import record_to_db
from app.services.history_window import show_history

BASE_DIR = Path(__file__).resolve().parents[2]
icon_path = os.path.join(BASE_DIR, "static", "history_icon.png")

print("Icon path:", icon_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 500, 300)

        # Устанавливаем стиль всему окну:
        self.setStyleSheet("""
            QLabel {
                font-family: "Arial";
                font-size: 24px;
                color: #0a9ba4;
            }
        """)
        self.main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        # Кнопка "history"
        self.history_button = QPushButton()
        self.history_button.setIcon(QIcon(icon_path))
        self.history_button.setFixedSize(60, 60)
        self.history_button.clicked.connect(show_history)

        # Добавляем "растяжку" слева, чтобы кнопка ушла вправо
        top_layout.addStretch()
        top_layout.addWidget(self.history_button)

        # Вкладываем горизонтальный лейаут top_layout в главный main_layout
        self.main_layout.addLayout(top_layout)

        # ========= 3. Поле для настройки интервала обновления =========
        self.interval_label = QLabel("Интервал обновления (сек):")
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 60)
        self.interval_spinbox.setValue(1)  # По умолчанию 1 секунда
        self.main_layout.addWidget(self.interval_label)
        self.main_layout.addWidget(self.interval_spinbox)

        # ========= 4. Остальные элементы (вниз, под шапкой)  =========
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("font-size: 14px; color: gray;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_time = QTime(0, 0)

        self.start_button = QPushButton("Начать запись")
        self.start_button.clicked.connect(self.start_monitoring)

        self.stop_button = QPushButton("Остановить")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setVisible(False)

        self.cpu_label = QLabel()
        self.ram_label = QLabel()
        self.disk_label = QLabel()

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_system_stats)

        # Добавляем остальные виджеты в главный лейаут
        self.main_layout.addWidget(self.cpu_label)
        self.main_layout.addWidget(self.ram_label)
        self.main_layout.addWidget(self.disk_label)
        self.main_layout.addWidget(self.timer_label)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.stop_button)

        # ========= 5. Создаём контейнер и настраиваем главное окно  =========
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def start_monitoring(self):
        """
        Запуск мониторинга.
        """
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.interval_label.setVisible(False)
        self.interval_spinbox.setVisible(False)

        self.cpu_label.setVisible(True)
        self.ram_label.setVisible(True)
        self.disk_label.setVisible(True)

        self.start_time = QTime(0, 0)
        self.timer.start(1000)  # Таймер для обновления времени

        # Устанавливаем интервал обновления данных системы
        interval = self.interval_spinbox.value() * 1000
        self.update_timer.start(interval)

    def stop_monitoring(self):
        """
        Остановка мониторинга.
        """
        self.timer.stop()
        self.update_timer.stop()
        self.timer_label.setText("00:00")

        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.interval_label.setVisible(True)
        self.interval_spinbox.setVisible(True)

        self.cpu_label.setVisible(False)
        self.ram_label.setVisible(False)
        self.disk_label.setVisible(False)

    def update_timer(self):
        """
        Обновление таймера времени записи.
        """
        self.start_time = self.start_time.addSecs(1)
        self.timer_label.setText(self.start_time.toString("mm:ss"))

    def update_system_stats(self):
        """
        Обновление значений CPU, RAM и Disk, а также запись в БД.
        """
        cpu_load = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Вычисляем занятые ресурсы
        ram_used = (ram.total - ram.available) // (1024 * 1024)  # В MB
        disk_used = (disk.total - disk.free) // (1024 * 1024)  # В MB

        # Обновление текста меток
        self.cpu_label.setText(f"ЦП: {cpu_load}%")
        self.ram_label.setText(f"ОЗУ: {ram_used}MB/{ram.total // (1024 * 1024)}MB")
        self.disk_label.setText(f"ПЗУ: {disk_used}MB/{disk.total // (1024 * 1024)}MB")

        # Сохранение данных в БД
        asyncio.create_task(record_to_db(cpu_load, ram_used, disk_used))
