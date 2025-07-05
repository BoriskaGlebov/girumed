from typing import Type

from app.appointments.models import Appointment, Doctor, Patient
from app.dao.base import BaseDAO


class PatientDAO(BaseDAO[Patient]):
    """
    Класс для доступа к данным в БД.

    Работает с таблицей Patient
    """

    model: Type[Patient] = Patient


class DoctorDAO(BaseDAO[Doctor]):
    """
    Класс для доступа к данным в БД.

    Работает с таблицей Doctor
    """

    model: Type[Doctor] = Doctor


class AppointmentDAO(BaseDAO[Appointment]):
    """
    Класс для доступа к данным в БД.

    Работает с таблицей Appointment
    """

    model: Type[Appointment] = Appointment
