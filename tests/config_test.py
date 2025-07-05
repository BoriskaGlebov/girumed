import os
from unittest.mock import patch

import pytest

from app.config import get_settings, logger

# def test_config(config):
#     """Проверка правильности настроек для работы приложения локально."""
#     assert config.get_test_db_url() == "postgresql+asyncpg://some_user:some_password@localhost:5432/test_girumed_db"
#     assert config.get_db_url() == "postgresql+asyncpg://some_user:some_password@localhost:5432/girumed_db"
#     logger.info("ОК")


# Тест на некорректные значения в .env
def test_invalid_settings():
    """# Тест на некорректные значения в .env."""
    with patch.dict(
        os.environ,
        {
            "DB_USER": "",
            "DB_PASSWORD": "",  # Пустой SecretStr
            "DB_HOST": "localhost",
            "DB_PORT": "invalid_port",  # Некорректный порт (должен быть int)
            "DB_NAME": "test_db",
            "DB_TEST": "test_db_test",
            "UPLOAD_DIRECTORY": "/uploads",
            "PYTHONPATH": "/app",
        },
    ):
        with pytest.raises(RuntimeError):
            get_settings()  # Вызов функции для получения настроек
    logger.info("ОК")
