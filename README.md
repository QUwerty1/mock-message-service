# Mock Message Service

FastAPI-заглушка сервиса уведомлений `MESSAGE_SERVICE`.

## Настройка

```bash
cp .env.example .env
```

`MESSAGE_OUTPUT_FILE` задаёт JSONL-файл. При отсутствии переменной сообщения выводятся в stdout.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

`POST /` принимает JSON с полями `token`, `body`, `mira_id` и `type`. Успешный ответ имеет статус `200` и тело `{"status":"ok"}`. Неверный токен возвращает `401`.

Проверка доступности выполняется через `GET /health`.

## Docker Image

Образ доступен на DockerHub: quwerty0/mock-message-service:21.11.2026
