import datetime
from typing import Any
import os
import pandas as pd
from collections import defaultdict
import json
import logging
from json import JSONDecodeError


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def greetings(date_time: str) -> str:
    """Функция - приветствие"""
    try:
        logger.info("Приветствуем пользователя")
        date_string = datetime.datetime.strptime(date_time, "%d.%m.%Y %H:%M:%S")
        if 5 <= date_string.hour < 12:
            return 'Доброе утро'
        elif 12 <= date_string.hour < 18:
            return 'Добрый день'
        elif 18 <= date_string.hour <= 23:
            return 'Добрый вечер'
        elif 0 <= date_string.hour < 5:
            return 'Доброй ночи'
    except ValueError:
        logger.error("Неправильная дата")
        return "Неправильная дата"


def read_excel(file: Any = None) -> list:
    """Функция, для чтения excel файла"""
    try:
        logger.info(f"Читаем файл {file} и выводим список транзакций")
        file_read_xlsx = pd.read_excel(file)
        return file_read_xlsx.to_dict(orient="records")
    except (FileNotFoundError, JSONDecodeError):
        logger.error("Файл не найден")
        return []


def filtering_transactions_by_date(date_time: str, transactions: list) -> Any:
    """Функция фильтрует транзакции по дате"""
    try:
        logger.info(f"Ищем месячный период транзакций заданной даты {date_time}")
        new_list = []
        date_string = datetime.datetime.strptime(date_time, "%d.%m.%Y %H:%M:%S")
        start_month = date_string.replace(day=1)
        for i in transactions:
            data_2 = i.get('Дата операции')
            date_string_2 = datetime.datetime.strptime(data_2, "%d.%m.%Y %H:%M:%S")
            if start_month <= date_string_2 <= date_string:
                new_list.append(i)
        return new_list
    except ValueError:
        logger.error("Нет транзакций за этот месяц или дата введена неверна")
        return "Нет транзакций за этот месяц или дата введена неверна"


def calculate_cashback(amount: int) -> float:
    """Возвращает кэшбэк на основе суммы (1% от суммы)."""
    if amount:
        return round(amount / 100, 2)
    return 0


def transaction_analysis(transactions: list) -> list:
    """Функция выводит: номер карты, сумму, кэшбэк"""
    result = []
    logger.info("Ищем информацию по каждой карте(номер карты, расходы, кэшбэк)")
    my_dict = defaultdict(lambda: {"total_spent": 0, "cashback": 0})
    for transaction in transactions:
        card_number = transaction.get('Номер карты', None)
        if not isinstance(card_number, str):
            continue
        elif isinstance(card_number, str):
            card_number = card_number.replace('*', '')
        amount = transaction.get('Сумма операции с округлением',0)
        my_dict[card_number]["total_spent"] += amount
        my_dict[card_number]["cashback"] += calculate_cashback(amount)
    for card, value in my_dict.items():
        result.append({"last_digits" : card, "total_spent" : round(value.get("total_spent"),2), "cashback" : round(value.get("cashback"),2)})
    return result


def top_five(transactions: list) -> json:
    """Топ-5 транзакций"""
    logger.info("Ищем Топ-5 транзакций по сумме платежа.")
    df = pd.DataFrame(transactions)
    df['Сумма платежа'] = df['Сумма платежа'].abs()
    sort_df = df.sort_values(by='Сумма платежа', ascending=False)
    top_five_df = sort_df.head()
    return top_five_df.to_json(orient='records', force_ascii=False)



def filtering_transactions_by_month_and_year(year: str, month: str, transactions: list) -> Any:
    try:
        logger.info(f"Ищем транзакции за {month} месяц, {year} год.")
        new_list = []
        for i in transactions:
            data_2 = i.get('Дата операции')
            date_string_2 = datetime.datetime.strptime(data_2, "%d.%m.%Y %H:%M:%S")
            if int(year) == date_string_2.year and int(month) == date_string_2.month:
                new_list.append(i)
        return new_list
    except ValueError:
        logger.error("Нет транзакций за этот месяц и год или дата введена неверна")
        return "Нет транзакций за этот месяц и год или дата введена неверна"


def read_excel_dataframe(file: Any = None) -> pd.DataFrame:
    try:
        logger.info(f"Читаем файл {file} и выводим данные в формате DataFrame")
        """Функция, для чтения excel файла с выводов DataFrame"""
        file_read_xlsx = pd.read_excel(file)
        return file_read_xlsx
    except (FileNotFoundError, JSONDecodeError):
        logger.error("Файл не найден")
        return []
