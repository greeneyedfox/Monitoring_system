import pytest
from PyQt6.QtCore import Qt
from app.gui.main_window import MainWindow

@pytest.fixture
def main_window(qtbot):
    """Фикстура для создания окна MainWindow и добавления его в qtbot."""
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window

def test_main_window_is_visible(main_window):
    """Проверяем, что окно вообще показывается."""
    assert main_window.isVisible()

def test_history_button_is_present(main_window):
    """Проверяем, что кнопка history присутствует."""
    assert main_window.history_button is not None
    assert main_window.history_button.isVisible()

def test_default_interval_value(main_window):
    """Проверяем, что QSpinBox для интервала по умолчанию = 1."""
    assert main_window.interval_spinbox.value() == 1

def test_start_stop_monitoring(qtbot, main_window):
    """
    Проверяем логику кнопок:
    - 'Начать запись' скрывает её и показывает 'Остановить'
    - 'Остановить' скрывает её и показывает 'Начать запись'
    """
    start_button = main_window.start_button
    stop_button = main_window.stop_button

    # Изначально кнопка "Начать запись" видна, "Остановить" - нет
    assert start_button.isVisible()
    assert not stop_button.isVisible()

    # Кликаем на "Начать запись"
    qtbot.mouseClick(start_button, Qt.MouseButton.LeftButton)

    # Теперь "Начать запись" должна скрыться, "Остановить" - появиться
    assert not start_button.isVisible()
    assert stop_button.isVisible()

    # Кликаем на "Остановить"
    qtbot.mouseClick(stop_button, Qt.MouseButton.LeftButton)

    # Теперь наоборот
    assert start_button.isVisible()
    assert not stop_button.isVisible()
