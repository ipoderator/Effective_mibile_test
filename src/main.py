import csv
import time
import sys
from typing import Any

from loguru import logger
import click

from add_data import transaction_data
from constants import (
    MAX, MIN, MY_DATE, ENTER_FIELD_EDIT,
    SEACH_CATEGORY, LIST_OF_CRITERIA
)

# Конфиг loguru
logger.add(sys.stderr, format='{time} {level} {message}',
           filter='my_module', level='INFO')
logger.add('logs/logs.log', level='DEBUG')


def write_data(file_name: Any, data: list, writer_type: str):
    """
    Записывает данные в файл CSV.
    file_name: имя файла для записи.
    Если падает в ошибку то перехватывает и логирует ее.:
    raise ValueError: если указанный режим не «w» или «a».
    """
    with open(file_name, writer_type, newline='', encoding='utf-8') as csvfile:
        columns = LIST_OF_CRITERIA
        file_writer = csv.DictWriter(
            csvfile, lineterminator='\r', fieldnames=columns
            )
        if writer_type == 'w':
            file_writer.writeheader()
        if data:
            file_writer.writerows(data)
    logger.info('Данные добвлены!')


@click.group()
def wallet():
    pass


@wallet.command()
def view_balance():
    """
    Просмотр баланса, доходов и расходов
    """
    try:
        total_income = sum(
            int(record['Сумма']) for record in transaction_data
            if record['Категория'] == 'Доход'
        )
        total_expense = sum(
            int(record['Сумма']) for record in transaction_data
            if record['Категория'] == 'Расход'
        )
        balance = total_income - total_expense
        click.echo(f'Текущий баланс: {balance}\n'
                   f'Доходы: {total_income}\n'
                   f'Расходы: {total_expense}')
        logger.info('Все хорошо, функция отработала успешно!')
    except Exception as e:
        logger.exception(f'Неизвестная ошибка: {e}, повторите попытку!')


@wallet.command()
def search_record():
    """
    Поиск записей по категориям
    """
    criterion_choice = click.prompt(
        SEACH_CATEGORY, type=click.Choice(LIST_OF_CRITERIA)
    )
    category = click.prompt(
        f'Введите категорию для поиска {criterion_choice}: '
        )
    found_records = [record for record in transaction_data
                     if record[criterion_choice] == category]
    if found_records:
        click.echo('Найденные записи:')
        for record in found_records:
            click.echo(record)
        logger.info('Все прошло успешно, запись найдена!')
    else:
        click.echo('Записи не найдены.')
        logger.debug('Что-то пошло не так, записи не найдены!')


@wallet.command()
@click.argument('file_name', default='transaction.csv')
def add_record(file_name: Any):
    """
    Принимает данные от пользователя:

    - Дату высталяет автоматически
    - Выбор Доход или Расход
    - Сумма Дохода или Расхода
    - Краткое описание
    И далее вывод какие данные были внесены.
    """
    formatted_date = MY_DATE.strftime('%Y-%m-%d')
    category_choice = click.prompt(
        'Введите категорию: ', type=click.Choice(['Доход', 'Расход'])
    )
    while MIN < MAX:
        MIN_1 = 0
        try:
            amount = int(input('Введите число: '))
            break
        except ValueError:
            MIN_1 += 1
            if MIN_1 == MAX:
                raise
            logger.error('Произошла ошибка. Введите число!')
            time.sleep(1)
    description = input('Краткое описание: ').strip()
    new_record = {
        'Дата': formatted_date, 'Категория': category_choice.title(),
        'Сумма': amount, 'Описание': description
    }
    transaction_data.append(new_record)
    write_data(file_name, [new_record], writer_type='a')
    print()
    print(f'Дата: {formatted_date}\n'
          f'Категория: {category_choice}\n'
          f'Сумма: {amount}\n'
          f'Описание: {description}')
    logger.info('Данные внесены успешно!')


@wallet.command()
@click.argument('file_name', default='transaction.csv')
def edit_record(file_name: Any):
    """
    Отредактировать существующую запись по индексу.
    """
    try:
        index = click.prompt(
            'Введите индекс записи для редактирования: ', type=int
        )
        if 0 <= index < len(transaction_data):
            click.echo(f'Текущая запись: {transaction_data[index]}')
            field_choice = click.prompt(
                ENTER_FIELD_EDIT, type=click.Choice(LIST_OF_CRITERIA)
            )
            if field_choice in transaction_data[index]:
                value = click.prompt(
                    f'Введите новое значение для {field_choice}: '
                )
                transaction_data[index][field_choice] = value
                write_data(file_name, transaction_data, writer_type='w')
                click.echo('Запись успешно изменена!')
                logger.info('Функция изменение записи отработала успешно')
        else:
            click.echo('Такой записи нет!')
            logger.debug('Записи не найдены!')
            time.sleep(1)
    except click.Abort:
        logger.exception('Не правильный ввод. Введите число!')


if __name__ == '__main__':
    wallet()
