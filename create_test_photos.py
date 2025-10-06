"""
Скрипт для создания тестовых фото
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_photo(text, filename, color):
    """Создает тестовое фото с текстом"""
    # Создаем изображение 400x300
    img = Image.new('RGB', (400, 300), color=color)
    draw = ImageDraw.Draw(img)
    
    # Пытаемся использовать системный шрифт
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
        except:
            font = ImageFont.load_default()
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Центрируем текст
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    # Рисуем текст
    draw.text((x, y), text, fill='white', font=font)
    
    # Сохраняем изображение
    img.save(filename)
    print(f"Создано фото: {filename}")

def main():
    """Создает 3 тестовых фото"""
    # Создаем папку если её нет
    if not os.path.exists('test_photos'):
        os.makedirs('test_photos')
    
    # Создаем 3 тестовых фото
    photos = [
        ("Тестовое фото 1", "test_photos/photo1.jpg", (255, 100, 100)),  # Красный
        ("Тестовое фото 2", "test_photos/photo2.jpg", (100, 255, 100)),  # Зеленый
        ("Тестовое фото 3", "test_photos/photo3.jpg", (100, 100, 255)),  # Синий
    ]
    
    for text, filename, color in photos:
        create_test_photo(text, filename, color)
    
    print("Все тестовые фото созданы!")

if __name__ == "__main__":
    main()
