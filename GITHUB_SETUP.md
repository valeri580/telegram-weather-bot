# 🚀 Инструкция по загрузке на GitHub

## 📋 Пошаговая инструкция

### 1. Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните данные:
   - **Repository name**: `telegram-weather-bot`
   - **Description**: `Telegram bot for weather forecast in Moscow using aiogram and OpenWeatherMap API`
   - Выберите **Public** или **Private**
   - **НЕ** добавляйте README, .gitignore или лицензию (они уже есть)
4. Нажмите **"Create repository"**

### 2. Инициализация Git в проекте

Откройте терминал в папке проекта и выполните:

```bash
# Инициализация Git репозитория
git init

# Добавление всех файлов (кроме исключенных в .gitignore)
git add .

# Первый коммит
git commit -m "Initial commit: Telegram weather bot for Moscow"

# Добавление удаленного репозитория (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telegram-weather-bot.git

# Переименование основной ветки в main
git branch -M main

# Отправка кода на GitHub
git push -u origin main
```

### 3. Проверка безопасности

⚠️ **ВАЖНО**: Убедитесь, что файлы с секретами НЕ попали в репозиторий:

```bash
# Проверьте, что .env файл не добавлен
git status

# Если .env файл есть в списке, удалите его:
git rm --cached .env
git commit -m "Remove .env file from tracking"
```

### 4. Создание .env файла для пользователей

Создайте файл `env_example.txt` (уже создан) с примером:

```env
# Токен Telegram-бота (получить у @BotFather)
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# API ключ для OpenWeatherMap (получить на https://openweathermap.org/api)
WEATHER_API_KEY=YOUR_WEATHER_API_KEY_HERE
```

## 🔧 Дополнительные настройки

### Настройка GitHub Actions (опционально)

Создайте папку `.github/workflows/` и файл `ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Настройка Issues и Projects

1. В репозитории перейдите в **Issues**
2. Включите Issues в настройках
3. Создайте шаблоны для Issues и Pull Requests

## 📝 Финальная проверка

После загрузки проверьте:

- [ ] Все файлы загружены корректно
- [ ] README.md отображается правильно
- [ ] .gitignore работает (секретные файлы не видны)
- [ ] Структура проекта понятна
- [ ] Инструкции по установке работают

## 🎉 Готово!

Ваш проект теперь доступен на GitHub! Поделитесь ссылкой с другими разработчиками.

## 🔗 Полезные ссылки

- [GitHub Docs](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Markdown Guide](https://www.markdownguide.org/)
