import datetime
import json
import os
from typing import Any

import pandas as pd

from src.utils import read_excel_dataframe

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")


def spending_by_category(category: str, date: Any) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца"""
    transactions = read_excel_dataframe(file_excel)
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    three_months_ago = date - pd.DateOffset(months=3)
    filter_category = transactions[transactions["Категория"] == category].copy()
    df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filter_category = transactions[(three_months_ago <= df_date) & (df_date <= date)]

    # filter_category.loc[:, "Дата операции"] = pd.to_datetime(
    #     filter_category["Дата операции"], format="%d.%m.%Y %H:%M:%S"
    # )
    # filtered_dates = filter_category[
    #     (filter_category["Дата операции"] >= three_months_ago) & (filter_category["Дата операции"] <= date)
    # ]

    result_dict = {
        "Категория": category,
        "Траты": round(filter_category["Сумма операции"].sum(), 2),
        "Начало": three_months_ago.strftime("%Y-%m-%d"),
        "Конец": date.strftime("%Y-%m-%d"),
    }
    if not result_dict.get("Траты"):
        return "За этот период не было трат."
    return json.dumps(result_dict, ensure_ascii=False, indent=4)


# df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
# transactions = transactions[(start_date <= df_date) & (df_date <= end_date)]
# print(spending_by_category("Супермаркеты", "12-05-2020 12:00:00"))
