.PHONY: preprod

preprod:
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

	@echo "✅ Контейнеры запущены. Выполняем следующую команду..."
	# Здесь укажи нужную команду, например:
	# docker compose exec backend python manage.py migrate
# Проверка кода линтерами и типами
lint:
	@echo "🔍 Запуск линтеров через pre-commit..."
	pre-commit run --all-files

# Запуск тестов (можно заменить на docker compose exec, если тесты в контейнере)
test:
	@echo "🧪 Запуск тестов..."
	ENV=local pytest tests

# Полная проверка: линтеры + тесты
check: lint test
