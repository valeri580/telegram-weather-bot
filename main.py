import asyncio
import aiohttp
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import (
    BOT_TOKEN, 
    WEATHER_API_URL, 
    MESSAGES, 
    BOT_NAME
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_weather_data():
    """
    Получает данные о погоде из OpenWeatherMap API
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Ошибка API: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Ошибка при получении данных о погоде: {e}")
        return None


def format_weather_message(weather_data):
    """
    Форматирует данные о погоде в читаемое сообщение
    """
    try:
        # Основные данные
        temp = round(weather_data['main']['temp'])
        feels_like = round(weather_data['main']['feels_like'])
        description = weather_data['weather'][0]['description'].title()
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']
        pressure = round(weather_data['main']['pressure'] * 0.750062)  # Конвертация в мм рт.ст.
        visibility = round(weather_data['visibility'] / 1000)  # Конвертация в км
        
        # Время обновления
        current_time = datetime.now().strftime("%H:%M %d.%m.%Y")
        
        return MESSAGES['weather_format'].format(
            temp=temp,
            feels_like=feels_like,
            description=description,
            wind_speed=wind_speed,
            humidity=humidity,
            pressure=pressure,
            visibility=visibility,
            time=current_time
        )
    except Exception as e:
        logger.error(f"Ошибка при форматировании данных о погоде: {e}")
        return MESSAGES['weather_error']


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start
    """
    await message.answer(
        MESSAGES['start'].format(bot_name=BOT_NAME),
        parse_mode="HTML"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обработчик команды /help
    """
    await message.answer(
        MESSAGES['help'],
        parse_mode="HTML"
    )


@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    """
    Обработчик команды /weather
    """
    # Отправляем сообщение о загрузке
    loading_msg = await message.answer("🌤️ Получаю данные о погоде...")
    
    # Получаем данные о погоде
    weather_data = await get_weather_data()
    
    if weather_data:
        weather_message = format_weather_message(weather_data)
        await loading_msg.edit_text(weather_message, parse_mode="HTML")
    else:
        await loading_msg.edit_text(MESSAGES['weather_error'], parse_mode="HTML")


@dp.message()
async def handle_other_messages(message: Message):
    """
    Обработчик всех остальных сообщений
    """
    await message.answer(
        "🤔 Не понимаю эту команду. Используйте /help для просмотра доступных команд.",
        parse_mode="HTML"
    )


async def main():
    """
    Основная функция для запуска бота
    """
    logger.info("Запуск бота...")
    
    # Проверяем наличие токена
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("Не установлен BOT_TOKEN! Создайте .env файл с токеном бота.")
        return
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
