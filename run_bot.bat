@echo off
echo Запуск Telegram-бота "Погодный Бот"...
echo.

REM Проверяем наличие .env файла
if not exist .env (
    echo ОШИБКА: Файл .env не найден!
    echo Скопируйте env_example.txt в .env и настройте API ключи
    pause
    exit /b 1
)

REM Устанавливаем зависимости если нужно
if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Запуск бота...
python main.py

pause
