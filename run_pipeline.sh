#!/bin/bash

# Запуск тестів Pytest
echo "Запуск тестів..."
pytest --maxfail=1 --disable-warnings -q
pytest_exit_code=$?
echo "Код завершення тестів: $pytest_exit_code"

# Запуск перевірки стилю за допомогою Flake8 із зазначенням файлу конфігурації .flake8
echo "Запуск перевірки стилю коду..."
flake8 --config="$(dirname "$0")/.flake8" .
flake8_exit_code=$?
echo "Код завершення Flake8: $flake8_exit_code"

# Якщо хоча б один крок завершився з помилкою – вийти з помилковим кодом
if [ $pytest_exit_code -ne 0 ] || [ $flake8_exit_code -ne 0 ]; then
    echo "Pipeline завершився з помилкою."
    exit 1
fi

echo "Всі перевірки пройдено успішно!"
exit 0