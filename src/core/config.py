import os

# Загрузка из переменных окружения (создайте .env файл)
model = os.getenv("MISTRAL_MODEL", "mistral-tiny")
key = os.getenv("MISTRAL_API_KEY", "")

# Проверка наличия ключа
if not key:
    raise ValueError("API ключ не найден. Создайте файл .env с MISTRAL_API_KEY=ваш_ключ")