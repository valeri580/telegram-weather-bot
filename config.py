"""
Конфигурационный файл для Telegram-бота с прогнозом погоды
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Также пытаемся загрузить из env_example.txt если .env недоступен
try:
    load_dotenv('env_example.txt')
except:
    pass

# Токен Telegram-бота (получить у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# API ключ для OpenWeatherMap (получить на https://openweathermap.org/api)
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'YOUR_WEATHER_API_KEY_HERE')

# ID города Москва для OpenWeatherMap
MOSCOW_CITY_ID = 524901

# URL для API OpenWeatherMap
WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?id={MOSCOW_CITY_ID}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

# Настройки бота
BOT_NAME = "Погодный Бот"
BOT_DESCRIPTION = "Бот для получения прогноза погоды в Москве"

# Сообщения бота
MESSAGES = {
    'start': """
🌤️ Добро пожаловать в {bot_name}!

Я помогу вам узнать текущую погоду в Москве.

Доступные команды:
/start - Начать работу с ботом
/help - Показать справку
/weather - Получить прогноз погоды в Москве
    """,
    
    'help': """
📋 Справка по командам:

/start - Начать работу с ботом
/help - Показать эту справку
/weather - Получить текущий прогноз погоды в Москве

Просто отправьте команду /weather, и я покажу вам актуальную информацию о погоде в столице России!
    """,
    
    'weather_error': """
❌ Извините, не удалось получить данные о погоде.
Попробуйте позже или обратитесь к администратору.
    """,
    
    'weather_format': """
🌤️ Погода в Москве:

🌡️ Температура: {temp}°C
🌡️ Ощущается как: {feels_like}°C
☁️ Описание: {description}
💨 Ветер: {wind_speed} м/с
💧 Влажность: {humidity}%
🌫️ Давление: {pressure} мм рт.ст.
👁️ Видимость: {visibility} км

🕐 Обновлено: {time}
    """,
    
    'photo_saved': """
📸 Фото сохранено!

Файл: {filename}
Размер: {file_size} байт
Время: {time}
    """,
    
    'voice_sent': """
🎤 Голосовое сообщение отправлено!

Текст: "{text}"
Длительность: {duration} сек
    """,
    
    'translation': """
🌍 Перевод на английский:

🇷🇺 Русский: {original_text}
🇺🇸 English: {translated_text}
    """,
    
    'translation_error': """
❌ Ошибка перевода. Попробуйте еще раз.
    """,
    
    'photo_error': """
❌ Ошибка при сохранении фото.
    """,
    
    'voice_error': """
❌ Ошибка при создании голосового сообщения.
    """
}
