import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.dao import PatientDAO
from app.appointments.models import Patient


@pytest.mark.asyncio(scope="session")
async def test_patient_add_find_one(async_client, test_db: AsyncSession) -> None:
    """Тест добавления пациента и поиска его по ID и email."""
    patient_data = {
        "name": "Test Patient",
        "email": "testpatient@example.com",
        "phone": "1234567890",
    }

    # Добавляем пациента
    patient: Patient = await PatientDAO.add(test_db, **patient_data)

    assert patient.id is not None
    assert patient.name == patient_data["name"]
    assert patient.email == patient_data["email"]

    # Поиск по ID
    found: Patient | None = await PatientDAO.find_one_or_none_by_id(test_db, patient.id)
    assert found is not None
    assert found.email == patient_data["email"]

    # Поиск по email
    found2: Patient | None = await PatientDAO.find_one_or_none(test_db, email=patient_data["email"])
    assert found2 is not None
    assert found2.name == patient_data["name"]


@pytest.mark.asyncio(scope="session")
async def test_patient_find_all_and_update_and_delete(async_client, test_db: AsyncSession) -> None:
    """Тест поиска всех пациентов, обновления и удаления одного из них."""
    # Получаем всех пациентов (предполагается, что база уже наполнена)
    patients: list[Patient] = await PatientDAO.find_all(test_db)  # type: ignore
    assert len(patients) > 0

    patient: Patient = patients[0]

    # Обновляем телефон пациента
    updated_list: list[Patient] = await PatientDAO.update(test_db, filter_by={"id": patient.id}, phone="9876543210")
    assert any(p.phone == "9876543210" for p in updated_list)

    # Удаляем пациента
    deleted_count: int = await PatientDAO.delete(test_db, id=patient.id)
    assert deleted_count == 1

    # Проверяем, что пациент действительно удалён
    deleted_patient: Patient | None = await PatientDAO.find_one_or_none_by_id(test_db, patient.id)
    assert deleted_patient is None
