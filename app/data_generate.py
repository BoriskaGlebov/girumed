from random import choice, randint
from typing import Any, List

import factory  # type: ignore
import faker

from app.appointments.models import Appointment, Doctor, Patient

faker_instance = faker.Faker("ru_RU")


class PatientFactory(factory.Factory):
    """Фабрика для генерации экземпляров модели Patient."""

    class Meta:
        model = Patient

    name: str = factory.Faker("name", locale="ru_RU")
    email: str = factory.LazyAttribute(lambda o: faker_instance.unique.email())
    phone: str = factory.LazyAttribute(lambda o: faker_instance.phone_number())


class DoctorFactory(factory.Factory):
    """Фабрика для генерации экземпляров модели Doctor."""

    class Meta:
        model = Doctor

    name: str = factory.Faker("name", locale="ru_RU")
    specialization: str = factory.LazyFunction(lambda: choice(["Терапевт", "Хирург", "Кардиолог", "Невролог"]))
    experience_years: int = factory.LazyFunction(lambda: randint(1, 40))


class AppointmentFactory(factory.Factory):
    """Фабрика для генерации экземпляров модели Appointment."""

    class Meta:
        model = Appointment

    doctor_id: int = factory.LazyFunction(lambda: randint(1, 5))
    patient_id: int = factory.LazyFunction(lambda: randint(1, 10))
    start_time: Any = factory.LazyFunction(lambda: faker_instance.date_time_between(start_date="now", end_date="+10d"))


def generate_patients(num_patients: int = 10) -> List[Patient]:
    """
    Генерирует список экземпляров Patient.

    Args:
        num_patients (int): Количество пациентов.

    Returns:
        List[Patient]: Список сгенерированных пациентов.
    """
    return [PatientFactory() for _ in range(num_patients)]


def generate_doctors(num_doctors: int = 5) -> List[Doctor]:
    """
    Генерирует список экземпляров Doctor.

    Args:
        num_doctors (int): Количество врачей.

    Returns:
        List[Doctor]: Список сгенерированных врачей.
    """
    return [DoctorFactory() for _ in range(num_doctors)]


def generate_appointments(
    patients: List[Patient],
    doctors: List[Doctor],
    num_appointments: int = 20,
) -> List[Appointment]:
    """
    Генерирует список уникальных записей к врачам.

    Args:
        patients (List[Patient]): Список пациентов.
        doctors (List[Doctor]): Список врачей.
        num_appointments (int): Количество записей.

    Returns:
        List[Appointment]: Список записей на приём.
    """
    appointments: List[Appointment] = []
    used_slots: set[tuple[Any, Any]] = set()

    for _ in range(num_appointments):
        doctor = choice(doctors)
        patient = choice(patients)

        for _ in range(10):  # До 10 попыток подобрать уникальный слот
            start = faker_instance.date_time_between(start_date="now", end_date="+10d")
            key = (doctor, start)

            if key not in used_slots:
                used_slots.add(key)
                appointments.append(
                    Appointment(
                        doctor_id=doctor.id,
                        patient_id=patient.id,
                        start_time=start,
                    )
                )
                break

    return appointments


if __name__ == "__main__":
    patients = generate_patients()
    doctors = generate_doctors()
    appointments = generate_appointments(patients, doctors)

    print(f"Создано пациентов: {len(patients)}")
    print(f"Создано врачей: {len(doctors)}")
    print(f"Создано записей: {len(appointments)}")

    for app in appointments:
        print(app)
