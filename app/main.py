from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from app.gui.main_window import MainWindow
import asyncio


async def main():
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Инициализация основного окна
    window = MainWindow()
    window.show()

    # Запуск событийного цикла
    loop.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
