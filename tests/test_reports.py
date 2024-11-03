import json
from typing import Any
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture()
def transactions() -> pd.DataFrame:
    transactions_data = [
        {"Дата операции": "20.09.2021 12:00:00", "Категория": "Супермаркеты", "Сумма операции": -200.00},
        {"Дата операции": "15.11.2021 13:30:00", "Категория": "Супермаркеты", "Сумма операции": -150.00},
        {"Дата операции": "10.12.2021 16:45:00", "Категория": "Супермаркеты", "Сумма операции": -100.00},
        {"Дата операции": "22.12.2021 18:00:00", "Категория": "Другие", "Сумма операции": -50.00},
        {"Дата операции": "01.10.2021 09:00:00", "Категория": "Супермаркеты", "Сумма операции": -100.00},
    ]
    transactions_df = pd.DataFrame(transactions_data)
    return transactions_df


@pytest.mark.parametrize(
    "category, date, expected_result",
    [
        (
            "Супермаркеты",
            "2021-12-22 16:45:00",
            {"Категория": "Супермаркеты", "Траты": -350.00, "Начало": "2021-09-22", "Конец": "2021-12-22"},
        )
    ],
)
@patch("src.reports.read_excel_dataframe")
def test_spending_by_category(
    mock_read_excel_dataframe: Mock, category: str, date: str, expected_result: list, transactions: pd.DataFrame
) -> Any:
    """Корректная работа функции"""
    mock_read_excel_dataframe.return_value = transactions
    result_json = spending_by_category(category, date)
    result = json.loads(result_json)
    assert result == expected_result


@patch("src.reports.read_excel_dataframe")
def test_spending_by_category_not_date(mock_read_excel_dataframe: Mock, transactions: pd.DataFrame) -> Any:
    """Корректная работа функции, если дата не задана"""
    mock_read_excel_dataframe.return_value = transactions
    result_json = spending_by_category("Супермаркеты", None)
    assert result_json == "За этот период не было трат."
