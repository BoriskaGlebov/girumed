import os
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.dao import AppointmentDAO, DoctorDAO, PatientDAO
from app.config import get_settings, logger
from app.data_generate import generate_appointments, generate_doctors, generate_patients
from app.database import Base, async_test_session, test_engine
from app.dependencies import get_session
from app.main import app
from migrations_script import run_alembic_command


async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
    """
    Переопределяет зависимость FastAPI `get_session` для тестовой среды.

    :yield: Асинхронная сессия SQLAlchemy.
    """
    async with async_test_session() as session:
        yield session


# Подменяем зависимость на тестовую сессию
app.dependency_overrides[get_session] = get_session_override


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clean_database() -> None:
    """Очищает все таблицы базы данных и применяет актуальные миграции Alembic перед запуском тестов."""
    cwd = os.path.split(os.getcwd())[1]

    if cwd == "tests":
        run_alembic_command("cd ..; alembic -x db=test upgrade head; alembic -x db=test current")
    elif cwd == "girumed":
        run_alembic_command("ENV=local alembic -x db=test upgrade head; alembic -x db=test current")

    async with async_test_session() as session:
        await session.execute(text("TRUNCATE TABLE appointments RESTART IDENTITY CASCADE;"))
        await session.execute(text("TRUNCATE TABLE doctors RESTART IDENTITY CASCADE;"))
        await session.execute(text("TRUNCATE TABLE patients RESTART IDENTITY CASCADE;"))
        await session.commit()

    logger.info("🧹 База данных очищена.")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_db(async_client: AsyncClient) -> AsyncGenerator[AsyncSession, None]:
    """
    Заполняет тестовую базу данных начальными значениями.

    :param async_client: HTTP-клиент для запросов к FastAPI-приложению.
    :yield: Сессия базы данных с начальными данными.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_test_session() as session:
        doctors = [await DoctorDAO.add(session, **doc.to_dict()) for doc in generate_doctors(5)]
        patients = [await PatientDAO.add(session, **pat.to_dict()) for pat in generate_patients(5)]

        appointments = generate_appointments(patients=patients, doctors=doctors, num_appointments=20)

        for appointment in appointments:
            try:
                await AppointmentDAO.add(session, **appointment.to_dict())
            except ValueError as e:
                logger.warning(f"⚠️ Не удалось создать приём: {e}")
            except SQLAlchemyError as e:
                logger.error(f"❌ Ошибка БД при создании приёма: {e}")

        yield session


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Создаёт асинхронный клиент для тестов FastAPI.

    :yield: AsyncClient с приложением.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def config() -> Generator[Any, None, None]:
    """
    Предоставляет настройки приложения.

    :yield: Объект конфигурации.
    """
    settings = get_settings()
    yield settings


@pytest_asyncio.fixture(scope="session")
async def test_doctor() -> AsyncGenerator[Any, None]:
    """
    Фикстура для создания тестового доктора.

    :yield: Объект доктора.
    """
    async with async_test_session() as session:
        doctor = await DoctorDAO.add(
            async_session=session,
            name="Dr. House",
            specialization="Офтальмолог",
            experience_years=10,
        )
        yield doctor


@pytest_asyncio.fixture(scope="session")
async def test_patient1() -> AsyncGenerator[Any, None]:
    """
    Фикстура для создания первого тестового пациента.

    :yield: Объект пациента.
    """
    async with async_test_session() as session:
        patient = await PatientDAO.add(
            async_session=session,
            name="Больной1",
            email="test@mail.ru",
            phone="89852000338",
        )
        yield patient


@pytest_asyncio.fixture(scope="session")
async def test_patient2() -> AsyncGenerator[Any, None]:
    """
    Фикстура для создания второго тестового пациента.

    :yield: Объект пациента.
    """
    async with async_test_session() as session:
        patient = await PatientDAO.add(
            async_session=session,
            name="Больной2",
            email="test2@mail.ru",
            phone="89852000339",
        )
        yield patient


@pytest_asyncio.fixture(scope="session")
async def test_appointment(
    test_doctor: Any,
    test_patient1: Any,
) -> AsyncGenerator[Any, None]:
    """
    Создаёт приём между тестовым доктором и пациентом 1.

    :yield: Объект приёма.
    """
    async with async_test_session() as session:
        start_time = datetime.now().replace(microsecond=0) + timedelta(hours=1)
        appointment = await AppointmentDAO.add(
            async_session=session,
            doctor_id=test_doctor.id,
            patient_id=test_patient1.id,
            start_time=start_time,
        )
        yield appointment


@pytest_asyncio.fixture(scope="session")
async def test_appointment2(
    test_doctor: Any,
    test_patient2: Any,
) -> AsyncGenerator[Any, None]:
    """
    Создаёт приём между тестовым доктором и пациентом 2.

    :yield: Объект приёма.
    """
    async with async_test_session() as session:
        start_time = datetime.now().replace(microsecond=0) + timedelta(hours=1)
        appointment = await AppointmentDAO.add(
            async_session=session,
            doctor_id=test_doctor.id,
            patient_id=test_patient2.id,
            start_time=start_time,
        )
        yield appointment
