import sys
import csv
from typing import Any

from loguru import logger

# Конфиг loguru
logger.add(sys.stderr, format="{level} {message}",
           filter="my_module", level="INFO")


def read_file(file_name: Any) -> list:
    """
    Считывает данные из файла CSV и возвращает список словарей.
    """
    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return data
    except FileNotFoundError:
        logger.exception(f'Файл {file_name} не найден!')


transaction_file = 'transaction.csv'
transaction_data = read_file(transaction_file)
