import json
import os

from src.utils import (filtering_transactions_by_date, get_currency_rate, get_share_price, greetings, read_excel,
                       top_five, transaction_analysis)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")
file_json = os.path.join(project_root, "data", "user_settings.json")


def users_analysis(user_date: str) -> str:
    """Функция для взаимодействия с пользователем"""
    greetings_result = greetings(user_date)
    transactions_excel = read_excel(file_excel)
    transactions_filter_by_date = filtering_transactions_by_date(user_date, transactions_excel)
    result_transaction_analysis = transaction_analysis(transactions_filter_by_date)
    json_string = top_five(transactions_filter_by_date)
    result_get_currency_rate = get_currency_rate(file_json)
    result_get_share_price = get_share_price(file_json)

    result = {
        "greeting": greetings_result,
        "cards": result_transaction_analysis,
        "top_transactions": json_string,
        "currency_rates": result_get_currency_rate,
        "stock_prices": result_get_share_price,
    }
    result_json = json.dumps(result, ensure_ascii=False, indent=4)
    return result_json


# print(users_analysis("2021-10-10 12:00:00"))
