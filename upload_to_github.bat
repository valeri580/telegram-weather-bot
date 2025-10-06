@echo off
echo ========================================
echo   Загрузка Telegram-бота на GitHub
echo ========================================
echo.

REM Проверяем, что мы в Git репозитории
if not exist .git (
    echo ОШИБКА: Не найден Git репозиторий!
    echo Сначала выполните: git init
    pause
    exit /b 1
)

echo 1. Проверка статуса Git...
git status

echo.
echo 2. Добавление всех файлов...
git add .

echo.
echo 3. Создание коммита...
git commit -m "Update: Telegram weather bot improvements"

echo.
echo 4. Проверка удаленного репозитория...
git remote -v

echo.
echo ========================================
echo   ВАЖНО: Настройте удаленный репозиторий!
echo ========================================
echo.
echo Если это первый раз, выполните:
echo git remote add origin https://github.com/YOUR_USERNAME/telegram-weather-bot.git
echo.
echo Затем запустите этот скрипт снова.
echo.

set /p choice="Продолжить загрузку? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 5. Отправка на GitHub...
    git push -u origin main
    echo.
    echo ✅ Проект успешно загружен на GitHub!
) else (
    echo Отмена загрузки.
)

echo.
pause
