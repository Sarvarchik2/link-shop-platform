# Архитектура Docker Deployment

## Схема подключений

```
┌─────────────────────────────────────────────────────────────┐
│                      HOST MACHINE                            │
│                                                              │
│  ┌──────────────┐                                           │
│  │   Browser    │                                           │
│  │              │                                           │
│  │  localhost:  │                                           │
│  │    3000      │ ◄─── Frontend UI                         │
│  │    8000      │ ◄─── Backend API                         │
│  │    9001      │ ◄─── MinIO Console                       │
│  └──────┬───────┘                                           │
│         │                                                    │
│         │ HTTP Requests                                     │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Docker Network (storely_network)          │   │
│  │                                                      │   │
│  │  ┌──────────────┐      ┌──────────────┐            │   │
│  │  │   Frontend   │      │   Backend    │            │   │
│  │  │  Container   │      │  Container   │            │   │
│  │  │              │      │              │            │   │
│  │  │  Port: 3000  │      │  Port: 8000  │            │   │
│  │  │              │      │              │            │   │
│  │  │  API Base:   │      │  CORS:       │            │   │
│  │  │  localhost:  │      │  localhost:  │            │   │
│  │  │    8000      │      │    3000      │            │   │
│  │  └──────────────┘      └──────┬───────┘            │   │
│  │                               │                     │   │
│  │                               │ Connects to         │   │
│  │                               ▼                     │   │
│  │  ┌──────────────┐      ┌──────────────┐            │   │
│  │  │  PostgreSQL  │      │    MinIO     │            │   │
│  │  │  Container   │      │  Container   │            │   │
│  │  │              │      │              │            │   │
│  │  │  Port: 5432  │      │  Port: 9000  │            │   │
│  │  │              │      │       9001   │            │   │
│  │  └──────────────┘      └──────────────┘            │   │
│  │                                                      │   │
│  │  ┌──────────────┐                                   │   │
│  │  │    Redis     │                                   │   │
│  │  │  Container   │                                   │   │
│  │  │              │                                   │   │
│  │  │  Port: 6379  │                                   │   │
│  │  └──────────────┘                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Port Mappings (docker-compose.yml):                        │
│  - 3000:3000  → Frontend                                    │
│  - 8000:8000  → Backend                                     │
│  - 5432:5432  → PostgreSQL                                  │
│  - 9000:9000  → MinIO API                                   │
│  - 9001:9001  → MinIO Console                               │
│  - 6379:6379  → Redis                                       │
└─────────────────────────────────────────────────────────────┘
```

## Потоки данных

### 1. Пользователь открывает Frontend (localhost:3000)

```
Browser → localhost:3000 → Docker Port Mapping → Frontend Container
```

### 2. Frontend делает API запрос

```
Browser → localhost:8000/api/... → Docker Port Mapping → Backend Container
```

### 3. Backend обращается к базе данных

```
Backend Container → postgres:5432 → PostgreSQL Container
(внутри Docker сети, используется hostname)
```

### 4. Backend работает с файлами

```
Backend Container → minio:9000 → MinIO Container
(внутри Docker сети, используется hostname)
```

## Важные моменты

### ✅ Правильно

**Из браузера (хост-машина):**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- MinIO Console: `http://localhost:9001`

**Внутри Docker сети (между контейнерами):**
- Backend → PostgreSQL: `postgres:5432`
- Backend → MinIO: `minio:9000`
- Backend → Redis: `redis:6379`

### ❌ Неправильно

**Из браузера:**
- ❌ `http://backend:8000` - не работает
- ❌ `http://frontend:3000` - не работает
- ❌ `http://postgres:5432` - не работает

**Внутри контейнера:**
- ❌ `http://localhost:5432` - может не работать
- ✅ `postgres:5432` - правильно

## Environment Variables

### Frontend (docker-compose.yml)

```yaml
environment:
  # Для браузера - используем localhost
  NUXT_PUBLIC_API_BASE: http://localhost:8000
```

### Backend (docker-compose.yml)

```yaml
environment:
  # Для контейнера - используем Docker hostnames
  DATABASE_URL: postgresql://postgres:postgres@postgres:5432/link_shop_platform
  MINIO_ENDPOINT: minio:9000
  REDIS_URL: redis://redis:6379
```

## Volumes

```yaml
volumes:
  postgres_data:     # Данные PostgreSQL
  minio_data:        # Файлы MinIO
  redis_data:        # Данные Redis
  backend_uploads:   # Загруженные файлы
```

Данные сохраняются между перезапусками контейнеров.

## Networks

```yaml
networks:
  storely_network:
    driver: bridge
```

Все контейнеры находятся в одной сети и могут общаться друг с другом по именам.
