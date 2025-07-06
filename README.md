# girumed
Тестовое задание «Clinic Appointments»
# Clinic Appointments Microservice

Минимальный микросервис для записи пациентов к врачу на приём.

---

## Оглавление

- [Описание](#описание)
- [Требования](#требования)
- [Запуск](#запуск)
- [Пример `.env`](#пример)
- [API](#api)
- [Тестирование](#тестирование)
- [Makefile](#makefile)
- [CI/CD](#cicd)

---

## Описание

Это сервис на FastAPI с моделью `Appointment` и двумя эндпойнтами:

- `POST /appointments` — создание записи;
- `GET /appointments/{id}` — получение записи по ID.

Уникальность записи гарантируется по паре `doctor_id + start_time`, чтобы врач не мог принять двух пациентов одновременно.

---

## Требования

- Docker и Docker Compose
- Python 3.12 (используется в Dockerfile)
- PostgreSQL (или MySQL — на выбор в `docker-compose.yml`)

---

## Запуск

1. Клонируйте репозиторий:

```bash

git clone https://github.com/BoriskaGlebov/girumed.git
cd girumed
```
2. Создайте ваш .env на основе примера и удалите **пример!**:

```bash

cp .env.example .env
```
3. Запустите сервис :

```bash

docker compose up -d
```
Либо воспользуйтесь командой

```bash

make up
```
4. Проверьте, что сервис работает:

```bash
    curl http://localhost:8000/health
```

## Пример
```dotenv
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
DB_NAME=clinic_db
DB_TEST=clinic_test_db

```
## API
### Создание записи
### POST /appointments

Тело запроса (JSON):
```json
{
  "patient_name": "Иван Иванов",
  "doctor_id": 1,
  "start_time": "2025-07-06T14:30:00"
}

```
Ответ: JSON с созданной записью и её уникальным ID.

## Тестирование
### Запуск тестов:
```bash

make test
```

### Makefile
```bach
make lint
```
— запуск форматирования и проверки кода (black, isort, flake8)
```bash

make test
```
 — запуск тестов через pytest
```bash

make check
```
 — запуск линтеров, а потом тестов


## CI/CD
Настроен GitHub Actions workflow с двумя шагами:

Линтинг кода (make lint)

Запуск тестов (make test)

Пушит на docker hub репозиторий

Все шаги должны успешно пройти для принятия изменений.
