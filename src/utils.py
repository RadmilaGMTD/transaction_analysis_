import datetime
import json
import logging
import math
import os
from collections import defaultdict
from json import JSONDecodeError
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")


def greetings(date_time: str) -> str:
    """Функция - приветствие"""
    try:
        logger.info("Приветствуем пользователя")
        date_string = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        if 5 <= date_string.hour < 12:
            return "Доброе утро"
        elif 12 <= date_string.hour < 18:
            return "Добрый день"
        elif 18 <= date_string.hour <= 23:
            return "Добрый вечер"
        elif 0 <= date_string.hour < 5:
            return "Доброй ночи"
    except ValueError:
        logger.error("Неправильная дата")
    return "Неправильная дата"


def read_excel(file: Any) -> list[Any]:
    """Функция, для чтения excel файла"""
    try:
        logger.info(f"Читаем файл {file} и выводим список транзакций")
        file_read_xlsx = pd.read_excel(file)
        return file_read_xlsx.to_dict(orient="records")
    except (FileNotFoundError, JSONDecodeError):
        logger.error("Файл не найден")
        return []


trans = read_excel(file_excel)


def filtering_transactions_by_date(date_time: str, transactions: list) -> Any:
    """Функция фильтрует транзакции по дате"""
    try:
        logger.info(f"Ищем месячный период транзакций заданной даты {date_time}")
        new_list = []
        date_string = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        start_month = date_string.replace(day=1)
        for i in transactions:
            data_2 = i.get("Дата операции")
            date_string_2 = datetime.datetime.strptime(data_2, "%d.%m.%Y %H:%M:%S")
            if start_month <= date_string_2 <= date_string:
                new_list.append(i)
        if not new_list:
            logger.warning("Список транзакций пуст. Возвращаем пустой список.")
            return []
        return new_list
    except ValueError:
        logger.error("Дата введена неверно")
        return "Дата введена неверно"


# print(filtering_transactions_by_date("2018-02-10 12:00:00", trans))


def calculate_cashback(amount: int) -> float:
    """Возвращает кэшбэк на основе суммы (1% от суммы)."""
    if amount:
        return round(amount / 100, 2)
    return 0


def transaction_analysis(transactions: list) -> list:
    """Функция выводит: номер карты, сумму, кэшбэк"""
    result = []
    logger.info("Ищем информацию по каждой карте(номер карты, расходы, кэшбэк)")
    my_dict: defaultdict[str, dict[str, float]] = defaultdict(lambda: {"total_spent": 0, "cashback": 0})
    for transaction in transactions:
        card_number = transaction.get("Номер карты", None)
        if not isinstance(card_number, str):
            continue
        elif isinstance(card_number, str):
            card_number = card_number.replace("*", "")
        amount = transaction.get("Сумма операции с округлением", 0)
        my_dict[card_number]["total_spent"] += amount
        my_dict[card_number]["cashback"] += calculate_cashback(amount)
    for card, value in my_dict.items():
        result.append(
            {
                "last_digits": card,
                "total_spent": round(value.get("total_spent", 0), 2),
                "cashback": round(value.get("cashback", 0), 2),
            }
        )
    return result


def top_five(transactions: list) -> list:
    """Топ-5 транзакций"""
    my_list = []
    my_dict: defaultdict = defaultdict()
    logger.info("Ищем Топ-5 транзакций по сумме платежа.")
    if not transactions:
        logger.warning("Список транзакций пуст. Возвращаем пустой список.")
        return []
    df = pd.DataFrame(transactions)
    df["Сумма платежа"] = df["Сумма платежа"].abs()
    sort_df = df.sort_values(by="Сумма платежа", ascending=False)
    top_five_df = sort_df.head()
    top_five_df_dict = top_five_df.to_dict(orient="records")
    for i in top_five_df_dict:
        my_dict["date"] = i.get("Дата операции", None)[:10]
        my_dict["amount"] = i.get("Сумма операции с округлением")
        my_dict["category"] = i.get("Категория")
        my_dict["description"] = i.get("Описание")
        my_list.append(dict(my_dict))
    return my_list


# transactions_filter_by_date = filtering_transactions_by_date("2021-10-10 12:00:00", trans)
# print(transactions_filter_by_date)
# print(top_five(transactions_filter_by_date))


def filtering_transactions_by_month_and_year(year: str, month: str, transactions: list) -> list:
    """Функция ищет транзакции за указанный месяц и год"""
    logger.info(f"Ищем транзакции за {month} месяц, {year} год.")
    new_list = []
    for i in transactions:
        data_2 = i.get("Дата операции")
        date_string_2 = datetime.datetime.strptime(data_2, "%d.%m.%Y %H:%M:%S")
        if int(year) == date_string_2.year and int(month) == date_string_2.month:
            new_list.append(i)
    if not new_list:
        logger.error(f"Отсутствуют транзакции за {month} месяц, {year} год. Возвращаем пустой список.")
        return []
    return new_list


def read_excel_dataframe(file: Any = None) -> pd.DataFrame:
    """Функция, для чтения excel файла с выводов DataFrame"""
    logger.info(f"Читаем файл {file} и выводим данные в формате DataFrame")
    file_read_xlsx = pd.read_excel(file)
    return file_read_xlsx


def get_category_cash(transactions: list) -> Any:
    """Функция выводит категории с кэшбэком"""
    logger.info("Ищем категории с кэшбэком и сортируем по убыванию.")
    my_dict: defaultdict[str, int] = defaultdict(int)
    for transaction in transactions:
        cash = transaction.get("Кэшбэк", None)
        if isinstance(cash, (int, float)) and not math.isnan(cash):
            category = transaction.get("Категория")
            round_cash = round(cash)
            if isinstance(category, str) and category.strip():
                my_dict[category] += round_cash
    if not dict(my_dict):
        logger.error("За этот период кэшбэка не было")
        return "За этот период кэшбэка не было"
    sorted_result = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_result


file_json = os.path.join(project_root, "data", "user_settings.json")


def get_currency_rate(file: str) -> list:
    """Функция выводит в файл курс валют"""
    logger.info("Поиска курс валют")
    url = "https://www.cbr-xml-daily.ru//daily_json.js"
    response = requests.get(url)
    my_list = list()
    if response.status_code != 200:
        logger.error("Не удалось получить курс валюты")
        raise ValueError("Не удалось получить курс валюты")
    data = response.json().get("Valute", None)
    my_list = [{"currency": key, "rate": value.get("Value")} for key, value in data.items()]
    logger.error(f"Записываем курс валют в файл {file}")
    with open(file, "w") as f:
        json.dump(my_list, f, indent=4)
    return my_list


def get_share_price(file: str) -> list:
    """Функция выводит в файл стоимость акций из S&P500"""
    logger.info("Поиск основных акций из S&P500")
    my_list = list()
    load_dotenv()
    apikey = os.getenv("apikey")
    response_ = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/AAPL,AMZN,GOOGL,MSFT,TSLA?apikey={apikey}"
    )
    if response_.status_code != 200:
        logger.error("Не удалось получить основные акции")
        raise ValueError("Не удалось получить основные акции")
    data = response_.json()
    for i in data:
        my_list.append({"stock": i.get("symbol"), "price": i.get("price")})
    logger.error(f"Записываем акции в файл {file}")
    with open(file, "w") as f:
        json.dump(my_list, f)
    return my_list


# transactions = read_excel(file_excel)

# def filter_date_events(date: str, transactions_: list, range_: str = "M") -> list:
#     """Функция, которая выодит транзакции в заданный промежуток времени"""
#     logger.info(f"Ищем {range_} период транзакций заданной даты {date}")
#     new_list = []
#     date_string = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
#     if range_ == "W":
#         start = date_string - datetime.timedelta(weeks=1)
#     elif range_ == "Y":
#         start = date_string - relativedelta(years=1)
#     elif range_ == "M":
#         start = date_string - relativedelta(months=1)
#     elif range_ == "ALL":
#         return [i for i in transactions_]
#     for i in transactions_:
#         data_2 = i.get("Дата операции")
#         date_string_2 = datetime.datetime.strptime(data_2, "%d.%m.%Y %H:%M:%S")
#         if start <= date_string_2 <= date_string:
#             new_list.append(i)
#     return new_list
#
#
# print(filter_date_events("20.12.2021 14:22:12", transactions, "W"))
