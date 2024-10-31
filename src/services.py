import json
import os
from collections import defaultdict
import math
from src.utils import filtering_transactions_by_month_and_year, read_excel


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")


def cashback_by_category(data: list, year: str, month: str) -> json:
    """Функция выводит категории с кэшбэком по убыванию"""
    filter_transactions = filtering_transactions_by_month_and_year(year, month, data)
    my_dict = defaultdict(float)
    for transaction in filter_transactions:
        cash = transaction.get('Кэшбэк', None)
        if isinstance(cash, (int,float)) and not math.isnan(cash):
            category = transaction.get('Категория')
            round_cash = round(cash)
            if isinstance(category, str) and category.strip():
                my_dict[category] += round_cash
    if not dict(my_dict):
        return "За этот период кэшбэка не было"
    sorted_result = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
    result_json = json.dumps(sorted_result, ensure_ascii=False)
    return result_json


transactions = read_excel(file_excel)
print(cashback_by_category(transactions, '2021', '05'))
