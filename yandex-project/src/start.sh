#!/bin/sh

# 1. Переходим в корень проекта, чтобы Alembic увидел alembic.ini
cd /yandex-project

# 2. Выполняем миграции, явно указывая путь к конфигу
alembic -c alembic.ini upgrade head

# 3. Запускаем приложение, используя python3 и указывая путь к main.py
python3 src/main.py
