# Monitoring_system
(Решение тестового задания)

## Как запустить приложение?
1. Клонируйте и откройте репозиторий
2. Добавьте виртуальное окружение
3. В терминале данного окружения:
```pip install -r requirements.txt```
4. Запуск контейнера с бд postgres (должен быть установллен docker):
`docker run --name monitoring_system_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -d --restart always \
  postgres`
5. Запуск миграций (создание таблиц в бд):
```alembic upgrade head```
6. Можно запускать приложение из точки входа app/main.py
7. Тесты запускаются командой `pytest` или напрямую из папки app/tests


## Пример работы приложения
1) Работа приложения

2) Тесты
