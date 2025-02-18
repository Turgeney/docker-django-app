FROM python:3.13.0-bookworm

# Устанавливаем переменные среды для корректной работы Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем систему и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию для приложения
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . /app/

# Копируем скрипт entrypoint.sh и делаем его исполняемым
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Устанавливаем скрипт entrypoint.sh как точку входа
ENTRYPOINT ["/app/entrypoint.sh"]

# Указываем дефолтную команду, которая будет выполняться через скрипт
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
