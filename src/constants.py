from datetime import datetime

MAX: int = 5
MIN: int = 0
MY_DATE = datetime.now()
ENTER_FIELD_EDIT: str = (
    'Введите поле для редактирования(Дата/Категория/Сумма/Описание): '
)
SEACH_CATEGORY: str = (
    'Введите критерий для поиска (Дата/Категория/Сумма/Описание): '
)
LIST_OF_CRITERIA: tuple = ['Дата', 'Категория', 'Сумма', 'Описание']

TESTING = [
    {'Дата': '2023-05-01', 'Категория': 'Доход', 'Сумма': 1000,
     'Описание': 'Зарплата'},
    {'Дата': '2023-05-02', 'Категория': 'Расход', 'Сумма': 500,
     'Описание': 'Продукты'},
    {'Дата': '2023-05-03', 'Категория': 'Доход', 'Сумма': 2000,
     'Описание': 'Фриланс'}
]
RECORDS = [
    {'Дата': '2023-05-01', 'Категория': 'Доход', 'Сумма': 1000,
     'Описание': 'Зарплата'},
    {'Дата': '2023-05-03', 'Категория': 'Доход', 'Сумма': 2000,
     'Описание': 'Фриланс'}
]
