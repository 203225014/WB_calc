# WB Unit Calculator

Много пользовательский веб-сайт для расчёта юнит-экономики товаров на маркетплейсе Wildberries.

## Технологии

- **Frontend:** React, TailwindCSS
- **Backend:** Python (FastAPI)
- **База данных:** SQLite (локально), PostgreSQL (через Supabase/Neon в продакшене)
- **Аутентификация:** JWT
- **Хостинг:** Render / Railway

## Запуск локально (для разработки)

### Требования

- Python 3.11+
- Node.js / npm
- Docker (опционально)

### Установка и запуск

1.  **Склонируйте репозиторий:**

    ```bash
    git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
    cd wb-unit-calculator
    ```

2.  **Запуск Backend (Python - FastAPI):**

    *   Перейдите в папку `backend`:
        ```bash
        cd backend
        ```
    *   Создайте и активируйте виртуальное окружение (рекомендуется):
        *   **Windows:**
            ```bash
            python -m venv venv
            venv\Scripts\Activate.ps1 # Для PowerShell
            # venv\Scripts\activate.bat # Для Command Prompt
            ```
        *   **Linux/macOS:**
            ```bash
            python -m venv venv
            source venv/bin/activate
            ```
    *   Установите зависимости:
        ```bash
        pip install -r requirements.txt
        # Также установите python-multipart, если он не в requirements.txt
        pip install python-multipart
        ```
    *   (Опционально) Создайте файл `.env` в папке `backend` на основе `.env.example` и укажите свои настройки (например, `SECRET_KEY`, `DATABASE_URL`).
    *   Запустите сервер разработки:
        ```bash
        python -m uvicorn main:app --reload
        ```
        Сервер будет доступен по адресу `http://127.0.0.1:8000`. Документация API по адресу `http://127.0.0.1:8000/docs`.

    *   **Вернитесь в корень проекта:**
        ```bash
        cd ..
        ```

3.  **Запуск Frontend (React):**

    *   Убедитесь, что вы в корне проекта (`wb-unit-calculator`).
    *   Перейдите в папку `frontend`:
        ```bash
        cd frontend
        ```
    *   Установите зависимости:
        ```bash
        npm install
        ```
    *   Запустите сервер разработки:
        ```bash
        npm start
        ```
        Приложение будет доступно в браузере по адресу `http://localhost:3000`. Оно будет автоматически перезапускаться при изменениях в коде.

### Структура проекта

- `frontend/` - исходный код React-приложения.
- `backend/` - исходный код FastAPI-приложения.
- `.env.example` - шаблон файла переменных окружения.
- `Dockerfile` - инструкции для сборки бэкенда в Docker.
- `README.md` - этот файл.

## Запуск с помощью Docker

1.  Убедитесь, что у вас установлены `Docker` и `Docker Compose`.
2.  (Опционально) Создайте файл `.env` в корне проекта на основе `.env.example` и укажите свои настройки.
3.  Выполните команду из корня проекта:
    ```bash
    docker-compose up --build
    ```
    Это соберёт образы и запустит контейнеры `db` и `backend`.
    Бэкенд будет доступен по адресу `http://127.0.0.1:8000`.
    Документация API по адресу `http://127.0.0.1:8000/docs`.

## API Endpoints (основные)

- `POST /token` - Получение JWT токена.
- `POST /users/` - Создание пользователя.
- `GET /users/me` - Получение информации о текущем пользователе.
- `POST /calculations/` - Создание расчёта.
- `GET /calculations/` - Получение списка расчётов пользователя.