# Docker Deployment Guide

## Быстрый старт

### Запуск всего проекта

```bash
# Запустить все сервисы (PostgreSQL, MinIO, Redis, Backend, Frontend)
docker-compose up -d

# Посмотреть логи
docker-compose logs -f

# Посмотреть логи конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Остановка проекта

```bash
# Остановить все сервисы
docker-compose down

# Остановить и удалить volumes (БД будет очищена!)
docker-compose down -v
```

### Пересборка после изменений

```bash
# Пересобрать и перезапустить все сервисы
docker-compose up -d --build

# Пересобрать только backend
docker-compose up -d --build backend

# Пересобрать только frontend
docker-compose up -d --build frontend
```

## Доступ к сервисам

После запуска сервисы будут доступны по следующим адресам:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
  - User: `postgres`
  - Password: `postgres`
  - Database: `link_shop_platform`
- **MinIO Console**: http://localhost:9001
  - User: `minioadmin`
  - Password: `minioadmin`
- **MinIO API**: http://localhost:9000
- **Redis**: localhost:6379

## Полезные команды

### Просмотр статуса контейнеров

```bash
docker-compose ps
```

### Выполнение команд внутри контейнера

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# PostgreSQL shell
docker-compose exec postgres psql -U postgres -d link_shop_platform
```

### Миграции базы данных

```bash
# Выполнить миграции
docker-compose exec backend python -c "from app.database import init_db; init_db()"

# Создать тестовые данные
docker-compose exec backend python init_test_data.py
```

### Очистка и перезапуск

```bash
# Остановить все контейнеры
docker-compose down

# Удалить все volumes (очистить БД)
docker-compose down -v

# Удалить все образы
docker-compose down --rmi all

# Полная очистка (контейнеры, volumes, образы, сети)
docker-compose down -v --rmi all --remove-orphans

# Запустить заново
docker-compose up -d --build
```

## Troubleshooting

### Проблемы с портами

Если порты уже заняты, можно изменить их в `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Изменить 3000 на 3001 для frontend
  - "8001:8000"  # Изменить 8000 на 8001 для backend
```

### Проблемы с подключением к БД

Убедитесь, что PostgreSQL полностью запустился:

```bash
docker-compose logs postgres
```

### Проблемы с MinIO

Создайте bucket вручную:

```bash
docker-compose exec backend python verify_minio.py
```

### Очистка Docker системы

Если возникают проблемы с дисковым пространством:

```bash
# Удалить неиспользуемые образы
docker image prune -a

# Удалить неиспользуемые volumes
docker volume prune

# Полная очистка системы
docker system prune -a --volumes
```

## Режим разработки

Для разработки можно запустить только инфраструктурные сервисы:

```bash
# Запустить только PostgreSQL, MinIO, Redis
docker-compose up -d postgres minio redis

# Backend запустить локально
cd backend
python main.py

# Frontend запустить локально
cd frontend
npm run dev
```

## Production режим

Для production рекомендуется:

1. Изменить `SECRET_KEY` в docker-compose.yml
2. Использовать environment файлы для секретов
3. Настроить reverse proxy (nginx)
4. Включить SSL/TLS
5. Настроить backup для volumes

## Структура volumes

- `postgres_data` - данные PostgreSQL
- `minio_data` - файлы MinIO
- `redis_data` - данные Redis
- `backend_uploads` - загруженные файлы backend

## Backup и восстановление

### Backup PostgreSQL

```bash
docker-compose exec postgres pg_dump -U postgres link_shop_platform > backup.sql
```

### Восстановление PostgreSQL

```bash
docker-compose exec -T postgres psql -U postgres link_shop_platform < backup.sql
```

### Backup MinIO

```bash
docker-compose exec minio mc mirror /data ./minio-backup
```
