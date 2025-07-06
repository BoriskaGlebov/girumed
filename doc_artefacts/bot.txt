from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio

API_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хранилище состояний (в реальном проекте лучше использовать FSM)
user_data = {}


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Здравствуйте! Опишите, пожалуйста, свои симптомы или проблему, "
        "чтобы я мог подобрать подходящего врача."
    )
    user_data[message.from_user.id] = {}


@dp.message_handler()
async def symptoms_handler(message: types.Message):
    user_id = message.from_user.id
    symptoms = message.text
    user_data[user_id]["symptoms"] = symptoms

    # Здесь вызывается "умная" функция подбора специализации врача
    specialization = await smart_doctor_selection(symptoms)
    user_data[user_id]["specialization"] = specialization

    await message.answer(
        f"На основе вашего описания, рекомендую обратиться к врачу-специалисту: *{specialization}*.\n"
        "Если вы согласны, отправьте 'Да', или напишите другую специализацию."
    )


@dp.message_handler(lambda msg: msg.text.lower() in ["да", "yes", "ok", "согласен", "подходит"])
async def confirm_specialization_handler(message: types.Message):
    user_id = message.from_user.id
    specialization = user_data.get(user_id, {}).get("specialization")
    if not specialization:
        await message.answer("Сначала опишите ваши симптомы.")
        return

    await message.answer(
        f"Отлично! Когда вам удобно прийти? Пожалуйста, введите дату и время в формате YYYY-MM-DD HH:MM")
    user_data[user_id]["awaiting_datetime"] = True


@dp.message_handler(lambda msg: user_data.get(msg.from_user.id, {}).get("awaiting_datetime", False))
async def appointment_time_handler(message: types.Message):
    user_id = message.from_user.id
    dt_text = message.text

    # Валидация даты/времени (упрощённо)
    try:
        from datetime import datetime
        appointment_time = datetime.strptime(dt_text, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("Неверный формат даты и времени. Попробуйте ещё раз в формате YYYY-MM-DD HH:MM")
        return

    specialization = user_data[user_id]["specialization"]

    # Получаем доступных врачей и свободное время через API (заглушка)
    available_doctors = await get_available_doctors(specialization, appointment_time)
    if not available_doctors:
        await message.answer("Извините, на выбранное время нет доступных врачей. Пожалуйста, выберите другое время.")
        return

    # Для простоты берём первого доступного врача
    doctor = available_doctors[0]

    # Создаём запись через API
    success = await create_appointment_api(user_id, doctor["id"], appointment_time)
    if success:
        await message.answer(f"Запись успешно создана! Ваш врач: {doctor['name']}, время приёма: {appointment_time}")
    else:
        await message.answer("Произошла ошибка при создании записи. Попробуйте позже.")

    user_data[user_id]["awaiting_datetime"] = False


# ---- Вспомогательные асинхронные заглушки ----

async def smart_doctor_selection(symptoms_text: str) -> str:
    """
    Имитация ИИ-подбора специализации врача по тексту симптомов.
    В реальном приложении здесь может быть вызов ML-модели или API.
    """
    # Пример простого ключевого слова
    if "сердце" in symptoms_text.lower():
        return "Кардиолог"
    elif "кожа" in symptoms_text.lower():
        return "Дерматолог"
    else:
        return "Терапевт"


async def get_available_doctors(specialization: str, appointment_time):
    """
    Заглушка: имитирует запрос к API для получения списка врачей
    со свободными слотами на указанное время.
    """
    # Пример данных
    doctors = [
        {"id": 1, "name": "Иванов И.И.", "specialization": "Терапевт"},
        {"id": 2, "name": "Петров П.П.", "specialization": "Кардиолог"},
        {"id": 3, "name": "Сидоров С.С.", "specialization": "Дерматолог"},
    ]
    available = [d for d in doctors if d["specialization"] == specialization]
    # В реальности нужно проверять расписание
    return available


async def create_appointment_api(patient_id, doctor_id, appointment_time) -> bool:
    """
    Заглушка: имитирует вызов бекенд API для создания записи.
    """
    await asyncio.sleep(0.5)  # имитация сетевого вызова
    return True


if __name__ == "__main__":
    executor.start_polling(dp)
