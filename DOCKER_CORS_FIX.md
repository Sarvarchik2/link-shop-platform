# Решение проблемы CORS и подключения к API

## Проблема

При запуске проекта в Docker возникали следующие ошибки:
- CORS ошибки при запросах к backend API
- Ошибки подключения (Failed to fetch)
- Frontend не мог обратиться к backend из браузера

## Причина

В `docker-compose.yml` для frontend была установлена переменная окружения:
```yaml
NUXT_PUBLIC_API_BASE: http://backend:8000
```

Это внутренний Docker hostname, который работает только внутри Docker сети между контейнерами. Из браузера пользователя (который работает на хост-машине) этот адрес недоступен.

## Решение

Изменена переменная окружения на:
```yaml
NUXT_PUBLIC_API_BASE: http://localhost:8000
```

Теперь браузер обращается к backend через `localhost:8000`, который проброшен из Docker контейнера на хост-машину через порты.

## Как это работает

### Внутри Docker сети:
- Backend контейнер доступен по имени `backend:8000`
- Frontend контейнер доступен по имени `frontend:3000`
- Контейнеры могут общаться друг с другом

### Из браузера (хост-машина):
- Backend доступен по `localhost:8000` (проброшен порт)
- Frontend доступен по `localhost:3000` (проброшен порт)
- Браузер делает запросы к `localhost:8000`

### CORS настройки

Backend уже имеет правильные CORS настройки в `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # ... другие origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Проверка

После изменений:

1. Frontend перезапущен:
```bash
docker-compose up -d --build frontend
```

2. Проверка доступности:
- Backend API: http://localhost:8000 ✅
- Frontend: http://localhost:3000 ✅
- API Docs: http://localhost:8000/docs ✅

## Для production

Для production окружения нужно:

1. Использовать реальный домен вместо localhost
2. Настроить HTTPS
3. Добавить домен в CORS origins
4. Использовать переменные окружения:

```yaml
environment:
  NUXT_PUBLIC_API_BASE: ${API_BASE_URL:-http://localhost:8000}
```

Затем в `.env` файле:
```
API_BASE_URL=https://api.yourdomain.com
```
