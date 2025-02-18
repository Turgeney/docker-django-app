#!/bin/sh

# Прекращаем выполнение при ошибке любой команды
set -e

# Выполняем миграции базы данных
echo "Выполнение миграций..."
python manage.py migrate

# Создаем суперпользователя (если его нет)
echo "from django.contrib.auth.models import User; \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin'); \
print('Суперпользователь создан')" | python manage.py shell

# Собираем статику
echo "Сбор статики..."
python manage.py collectstatic --noinput

# Запускаем сервер
echo "Запуск приложения: $@"
exec "$@"
