from typing import Any, Optional
import os
import pandas as pd
from src.utils import read_excel_dataframe
import datetime



project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")



def spending_by_category(transactions_: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца"""
    if date is None:
        date = datetime.date.today().strftime("%d.%m.%Y")
    date_string = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_month = (date_string - pd.DateOffset(months=3))
    filter_category = transactions_[transactions_['Категория'] == category]
    filter_category.loc[:,'Дата операции'] = pd.to_datetime(filter_category['Дата операции'], format="%d.%m.%Y %H:%M:%S")
    filtered_dates = filter_category[(filter_category['Дата операции'] >= start_month) &
                                     (filter_category['Дата операции'] <= date_string)]

    return filtered_dates


transactions = read_excel_dataframe(file_excel)
spending_by_category(transactions, 'Супермаркеты', '20.12.2021')


def spending_by_weekday(transactions_: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.date.today().strftime("%d.%m.%Y")
    date_string = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_month = date_string - pd.DateOffset(months=3)
    transactions_['Дата операции'] = pd.to_datetime(transactions_['Дата операции'], format="%d.%m.%Y %H:%M:%S", errors='coerce')
    filtered_dates = transactions_[(transactions_['Дата операции'] >= start_month) &
                                     (transactions_['Дата операции'] <= date_string)].copy()
    # Добавляем столбец с днем недели (0 = понедельник, 6 = воскресенье)
    filtered_dates.loc[:,'День недели'] = filtered_dates['Дата операции'].dt.dayofweek

    # Группируем данные по дню недели и вычисляем средние траты
    average_spending = filtered_dates.groupby('День недели')['Сумма операции'].mean().abs()

    # Настройка индекса для более удобного отображения
    average_spending.index = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    return average_spending


transactions = read_excel_dataframe(file_excel)
spending_by_weekday(transactions, '20.12.2021')
