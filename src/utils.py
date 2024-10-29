import datetime
from typing import Any
import os
import pandas as pd
from collections import defaultdict
import json


def greetings(date_time: str) -> str:
    """Функция - приветствие"""
    try:
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
        return "Неправильная дата"

greetings('31.12.2021 16:44:00')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")


def read_excel(file: Any = None) -> list:
    """Функция, для чтения excel файла"""
    file_read_xlsx = pd.read_excel(file)
    return file_read_xlsx.to_dict(orient="records")

transactions_excel = read_excel(file_excel)


def filtering_transactions_by_date(date_time: str, transactions: list) -> Any:
    """Функция фильтрует транзакции по дате"""
    try:
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
        return "Нет транзакций за этот месяц или дата введена неверна"


data = '20.12.2021 16:44:00'
transactions_filter_by_date = filtering_transactions_by_date(data, transactions_excel)


def calculate_cashback(amount: int) -> float:
    """Возвращает кэшбэк на основе суммы (1% от суммы)."""
    if amount:
        return round(amount / 100, 2)
    return 0

def transaction_analysis(transactions: list) -> list:
    """Функция выводит: номер карты, сумму, кэшбэк"""
    result = []
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

transaction_analysis(transactions_filter_by_date)

def top_five(transactions: list) -> json:
    """Топ-5 транзакций"""
    df = pd.DataFrame(transactions)
    df['Сумма платежа'] = df['Сумма платежа'].abs()
    sort_df = df.sort_values(by='Сумма платежа', ascending=False)
    top_five_df = sort_df.head()
    return top_five_df.to_json(orient='records', force_ascii=False)

top_five(transactions_filter_by_date)


