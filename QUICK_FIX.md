# Быстрое решение проблемы CORS

## ❌ Проблема
При открытии http://localhost:3000 в браузере появляются ошибки:
- `Failed to fetch`
- `CORS policy` ошибки
- `net::ERR_NAME_NOT_RESOLVED` для `backend:8000`

## ✅ Решение

### 1. Проверьте docker-compose.yml

В секции `frontend` должно быть:
```yaml
environment:
  NUXT_PUBLIC_API_BASE: http://localhost:8000  # ✅ Правильно
  # НЕ http://backend:8000                     # ❌ Неправильно
```

### 2. Перезапустите frontend

```bash
docker-compose up -d --build frontend
```

### 3. Проверьте доступность

```bash
# Backend должен отвечать
curl http://localhost:8000/

# Frontend должен быть доступен
curl http://localhost:3000/
```

## 🔍 Почему это работает?

- `backend:8000` - работает только ВНУТРИ Docker сети
- `localhost:8000` - работает из браузера на хост-машине
- Порты пробрасываются через `ports:` в docker-compose.yml

## 📝 Для production

Используйте переменные окружения:

```yaml
environment:
  NUXT_PUBLIC_API_BASE: ${API_BASE_URL:-http://localhost:8000}
```

Создайте `.env`:
```
API_BASE_URL=https://api.yourdomain.com
```

## 🆘 Если не помогло

1. Проверьте логи:
```bash
docker-compose logs backend
docker-compose logs frontend
```

2. Перезапустите все сервисы:
```bash
docker-compose down
docker-compose up -d --build
```

3. Проверьте CORS в `backend/app/main.py`:
```python
allow_origins=[
    "http://localhost:3000",  # Должно быть в списке
    ...
]
```
