import json
import os

from src.utils import filtering_transactions_by_month_and_year, get_category_cash

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")


def users_cash(year: str, month: str, transactions_: list) -> str:
    """Функция выводит категории с кэшбэком по убыванию"""
    filter_transactions = filtering_transactions_by_month_and_year(year, month, transactions_)
    result_category_cash = get_category_cash(filter_transactions)
    result_json = json.dumps(result_category_cash, ensure_ascii=False)
    return result_json
