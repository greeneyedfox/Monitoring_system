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
   ![image](https://github.com/user-attachments/assets/b858be7e-54a0-4615-97d3-3e1937754252)
   ![image](https://github.com/user-attachments/assets/d9cc62dc-e09c-4e52-93fe-c2e2fa3a33f5)
   ![image](https://github.com/user-attachments/assets/1fa19916-429c-4506-bc06-784bfda86519)
   ![image](https://github.com/user-attachments/assets/6bdf9815-1f41-447f-9914-2d2a926abac6)
   ![image](https://github.com/user-attachments/assets/13e51abb-e869-4923-9260-ea00a6a59a1a)
   ![image](https://github.com/user-attachments/assets/3f7ae549-c629-4b8b-869d-df43fb042424)

2) Тесты:
   ![image](https://github.com/user-attachments/assets/b892ecfa-7baa-434d-a7d0-18ef7303d5b6)
   ![image](https://github.com/user-attachments/assets/32d75361-62e5-40a3-924e-ab1a3b417681)


