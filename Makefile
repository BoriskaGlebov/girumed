.PHONY: up

up:
	@echo "📄 Копируем .env-template → .env"
	@if [ -f .env-template ] && [ ! -f .env ]; then \
		echo "📄 Копируем .env-template → .env"; \
		cp .env-template .env; \
	else \
		echo "⚠️ Либо .env-template отсутствует, либо .env уже существует — пропускаем копирование"; \
	fi
	chmod +x init.sh

	@echo "🐳 Запускаем docker compose с пересборкой..."
	docker compose up -d --build

down:
	@echo "Сворачиваю проект"
	docker compose down -v
lint:
	@echo "🔍 Запуск линтеров через pre-commit..."
	pre-commit run --all-files

test:
	@echo "🧪 Запуск тестов..."
	ENV=local pytest tests
test-CI:
	@echo "🧪 Запуск тестов CI..."
	docker compose exec web pytest tests

# Полная проверка: линтеры + тесты
check: lint test test-CI

push:
	@echo "📦 Собираем образ через docker compose..."
	docker compose build

	@echo "🚀 Пушим образ..."
	docker push boristhebladeglebov/girumed-app:latest
