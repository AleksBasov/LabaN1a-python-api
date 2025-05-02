# Используем официальный образ Python на базе Alpine
FROM python:3.13-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (если нужны для некоторых Python-пакетов)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Копируем файлы с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем необходимые зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое текущей директории в контейнер
COPY . .

# Открываем порт для доступа к FastAPI
EXPOSE 8000

# Команда для запуска FastAPI с использованием uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]