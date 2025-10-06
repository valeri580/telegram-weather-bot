import asyncio
import aiohttp
import logging
import os
import io
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize, FSInputFile
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
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

# Инициализация переводчика
translator = GoogleTranslator(source='ru', target='en')

# Создаем папку для изображений если её нет
if not os.path.exists('img'):
    os.makedirs('img')

# Словарь для отслеживания состояний пользователей
user_states = {}


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


async def save_photo(message: Message):
    """
    Сохраняет фото, отправленное пользователем
    """
    try:
        # Получаем фото с наилучшим качеством
        photo = message.photo[-1]  # Берем фото с максимальным разрешением
        
        # Скачиваем файл
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path
        
        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}_{photo.file_id[:8]}.jpg"
        save_path = os.path.join('img', filename)
        
        # Скачиваем и сохраняем файл
        await bot.download_file(file_path, save_path)
        
        # Получаем размер файла
        file_size = os.path.getsize(save_path)
        
        return {
            'success': True,
            'filename': filename,
            'file_size': file_size,
            'save_path': save_path
        }
    except Exception as e:
        logger.error(f"Ошибка при сохранении фото: {e}")
        return {'success': False, 'error': str(e)}


async def create_voice_message(text: str):
    """
    Создает голосовое сообщение из текста
    """
    try:
        # Создаем временный файл для аудио в формате ogg
        temp_path = tempfile.mktemp(suffix='.ogg')
        
        # Создаем TTS объект и сохраняем в файл
        tts = gTTS(text=text, lang='ru', slow=False)
        tts.save(temp_path)
        
        # Проверяем, что файл создался
        if not os.path.exists(temp_path):
            return {'success': False, 'error': 'Файл не был создан'}
        
        # Получаем размер файла
        file_size = os.path.getsize(temp_path)
        
        if file_size == 0:
            return {'success': False, 'error': 'Файл пустой'}
        
        return {
            'success': True,
            'file_path': temp_path,
            'file_size': file_size
        }
    except Exception as e:
        logger.error(f"Ошибка при создании голосового сообщения: {e}")
        return {'success': False, 'error': str(e)}


def translate_text(text: str):
    """
    Переводит текст с русского на английский
    """
    try:
        # Переводим текст
        translated = translator.translate(text)
        return {
            'success': True,
            'original_text': text,
            'translated_text': translated
        }
    except Exception as e:
        logger.error(f"Ошибка при переводе текста: {e}")
        return {'success': False, 'error': str(e)}


async def send_random_photo(message: Message):
    """
    Отправляет случайное тестовое фото
    """
    try:
        # Список доступных тестовых фото
        test_photos = [
            'test_photos/photo1.jpg',
            'test_photos/photo2.jpg', 
            'test_photos/photo3.jpg'
        ]
        
        # Выбираем случайное фото
        random_photo = random.choice(test_photos)
        
        # Проверяем, что файл существует
        if not os.path.exists(random_photo):
            return False, f"Файл {random_photo} не найден"
        
        # Отправляем фото
        photo = FSInputFile(random_photo)
        await message.answer_photo(
            photo=photo,
            caption=f"📸 Случайное тестовое фото: {os.path.basename(random_photo)}"
        )
        
        return True, f"Отправлено фото: {os.path.basename(random_photo)}"
        
    except Exception as e:
        logger.error(f"Ошибка при отправке случайного фото: {e}")
        return False, str(e)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start
    """
    start_message = f"""
🌤️ Добро пожаловать в {BOT_NAME}!

Я помогу вам:
• Узнать погоду в Москве
• Сохранить ваши фото
• Отправить голосовые сообщения
• Перевести текст на английский

Доступные команды:
/start - Начать работу с ботом
/help - Показать справку
/weather - Получить прогноз погоды в Москве
/voice - Создать голосовое сообщение
/translate <текст> - Перевести текст на английский
/photo - Отправить случайное тестовое фото

Также вы можете:
📸 Отправить фото - я сохраню его
    """
    await message.answer(start_message)


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обработчик команды /help
    """
    help_message = """
📋 Справка по командам:

/start - Начать работу с ботом
/help - Показать эту справку
/weather - Получить текущий прогноз погоды в Москве
/voice - Создать голосовое сообщение
/translate <текст> - Перевести текст на английский
/photo - Отправить случайное тестовое фото

📸 Функции:
• Отправьте фото - бот сохранит его в папку img/
• Используйте /voice для создания голосовых сообщений
• Используйте /translate для перевода текста

Примеры:
/voice (затем напишите текст)
/translate Привет, как дела?
/photo
    """
    await message.answer(help_message)


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
        await loading_msg.edit_text(weather_message)
    else:
        await loading_msg.edit_text(MESSAGES['weather_error'])


@dp.message(Command("voice"))
async def cmd_voice(message: Message):
    """
    Обработчик команды /voice - запрашивает текст для голосового сообщения
    """
    user_id = message.from_user.id
    user_states[user_id] = 'waiting_for_voice_text'
    
    await message.answer(
        "🎤 Напишите текст, который нужно озвучить:\n"
        "Просто отправьте сообщение с текстом, и я создам голосовое сообщение!"
    )


@dp.message(Command("translate"))
async def cmd_translate(message: Message):
    """
    Обработчик команды /translate
    """
    # Получаем текст после команды
    text = message.text.replace('/translate', '').strip()
    
    if not text:
        await message.answer("❌ Укажите текст для перевода.\nПример: /translate Привет, как дела?")
        return
    
    # Отправляем сообщение о переводе
    loading_msg = await message.answer("🌍 Перевожу на английский...")
    
    # Переводим текст
    translation_result = translate_text(text)
    
    if translation_result['success']:
        await loading_msg.edit_text(
            MESSAGES['translation'].format(
                original_text=translation_result['original_text'],
                translated_text=translation_result['translated_text']
            )
        )
    else:
        await loading_msg.edit_text(MESSAGES['translation_error'])


@dp.message(Command("photo"))
async def cmd_photo(message: Message):
    """
    Обработчик команды /photo - отправляет случайное тестовое фото
    """
    # Отправляем сообщение о загрузке
    loading_msg = await message.answer("📸 Отправляю случайное фото...")
    
    # Отправляем случайное фото
    success, result = await send_random_photo(message)
    
    if success:
        await loading_msg.edit_text(f"✅ {result}")
    else:
        await loading_msg.edit_text(f"❌ Ошибка: {result}")


@dp.message(lambda message: message.photo is not None)
async def handle_photo(message: Message):
    """
    Обработчик фото
    """
    # Отправляем сообщение о сохранении
    loading_msg = await message.answer("📸 Сохраняю фото...")
    
    # Сохраняем фото
    save_result = await save_photo(message)
    
    if save_result['success']:
        current_time = datetime.now().strftime("%H:%M %d.%m.%Y")
        await loading_msg.edit_text(
            MESSAGES['photo_saved'].format(
                filename=save_result['filename'],
                file_size=save_result['file_size'],
                time=current_time
            ),
        )
    else:
        await loading_msg.edit_text(MESSAGES['photo_error'])


@dp.message()
async def handle_other_messages(message: Message):
    """
    Обработчик всех остальных сообщений
    """
    text = message.text.strip()
    user_id = message.from_user.id
    
    # Проверяем, что это не команда
    if text.startswith('/'):
        await message.answer(
            "🤔 Не понимаю эту команду. Используйте /help для просмотра доступных команд."
        )
        return
    
    # Проверяем состояние пользователя
    if user_id in user_states and user_states[user_id] == 'waiting_for_voice_text':
        # Пользователь ждет создания голосового сообщения
        user_states[user_id] = None  # Сбрасываем состояние
        
        # Отправляем сообщение о создании
        loading_msg = await message.answer("🎤 Создаю голосовое сообщение...")
        
        # Создаем голосовое сообщение
        voice_result = await create_voice_message(text)
        
        if voice_result['success']:
            try:
                # Отправляем голосовое сообщение
                voice_file = FSInputFile(voice_result['file_path'])
                await message.answer_voice(
                    voice=voice_file,
                    caption=f"🎤 Голосовое сообщение: {text}"
                )
                
                # Отправляем подтверждение
                current_time = datetime.now().strftime("%H:%M %d.%m.%Y")
                await loading_msg.edit_text(
                    MESSAGES['voice_sent'].format(
                        text=text,
                        duration=len(text) // 10 + 1  # Примерная длительность
                    ) + f"\n🕐 Время: {current_time}"
                )
                
            except Exception as e:
                logger.error(f"Ошибка при отправке голосового сообщения: {e}")
                await loading_msg.edit_text(MESSAGES['voice_error'])
            finally:
                # Удаляем временный файл
                try:
                    os.unlink(voice_result['file_path'])
                except:
                    pass
        else:
            await loading_msg.edit_text(MESSAGES['voice_error'])
        
        return
    
    # Для обычного текста просто отвечаем подсказкой
    await message.answer(
        "💬 Для перевода текста используйте команду /translate\n"
        "Для создания голосового сообщения используйте /voice\n"
        "Примеры:\n/translate Привет, как дела?\n/voice"
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
