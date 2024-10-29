import pytest
from src.utils import greetings, read_excel, filtering_transactions_by_date, calculate_cashback, transaction_analysis, top_five
import os
import pandas as pd
from unittest.mock import mock_open, patch
from typing import Any


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_file_path_excel = os.path.join(project_root, "data", "test_transactions_excel.xlsx")

@pytest.fixture
def transactions():
    return [{'Дата операции': '22.12.2021 10:19:26', 'Дата платежа': '20.12.2021', 'Сумма платежа': 562.67, 'Номер карты': '*7197', 'Сумма операции с округлением': 34.0},
            {'Дата операции': '21.12.2021 10:09:30', 'Дата платежа': '20.12.2021', 'Сумма платежа': 346.67, 'Номер карты': '*7197', 'Сумма операции с округлением': 172.69},
            {'Дата операции': '19.12.2021 20:13:13', 'Дата платежа': '20.12.2021', 'Сумма платежа': -505.67, 'Номер карты': '*5091', 'Сумма операции с округлением': 42.92}]


@pytest.mark.parametrize("data, expected", [('31.12.2021 16:44:00', 'Добрый день'),
                                            ('31.12.2021 18:44:00', 'Добрый вечер'),
                                            ('31.12.2021 08:44:00', 'Доброе утро'),
                                            ('31.12.2021 00:44:00', 'Доброй ночи')])
def test_greetings(data, expected):
    assert greetings(data) == expected


def test_greetings_invalid():
    assert greetings("12345") == 'Неправильная дата'


def test_read_xlsx_valid() -> None:
    """Тест на проверку работы функции с excel файлом"""
    rows = [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    df = pd.DataFrame(rows)
    df.to_excel(test_file_path_excel, index=False)
    result = read_excel(test_file_path_excel)
    assert result == [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    os.remove(test_file_path_excel)


@patch("pandas.read_excel")
def test_valid_file_excel(mock_read_excel: Any) -> None:
    """Корректная работа функции с файлом excel с моком."""
    mock_read_excel.return_value = pd.DataFrame(
        [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    )
    file_read_excel = read_excel("../data/transactions.xlsx")
    expected_result = [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    assert file_read_excel == expected_result


@pytest.mark.parametrize("data, expected",[('21.12.2021 10:09:30', [{'Дата операции': '21.12.2021 10:09:30', 'Дата платежа': '20.12.2021', 'Сумма платежа': 346.67, 'Номер карты': '*7197', 'Сумма операции с округлением': 172.69},
            {'Дата операции': '19.12.2021 20:13:13', 'Дата платежа': '20.12.2021', 'Сумма платежа': -505.67, 'Номер карты': '*5091', 'Сумма операции с округлением': 42.92}])])
def test_filtering_transactions_by_date(data, transactions, expected):
    assert filtering_transactions_by_date(data, transactions) == expected


def test_filtering_transactions_by_date_invalid(transactions):
    assert filtering_transactions_by_date('1111', transactions) == "Нет транзакций за этот месяц или дата введена неверна"


@pytest.mark.parametrize('amount, expected', [(150, 1.50), (2068.56, 20.69), (0,0)])
def test_calculate_cashback(amount, expected):
    assert calculate_cashback(amount) == expected


def test_transaction_analysis(transactions):
    assert transaction_analysis(transactions) == [{'last_digits': '7197', 'total_spent': 206.69, 'cashback': 2.07}, {'last_digits': '5091', 'total_spent': 42.92, 'cashback': 0.43}]


def test_transaction_analysis_not_str():
    assert transaction_analysis([{'Дата операции': '22.12.2021 10:19:26', 'Дата платежа': '20.12.2021', 'Номер карты': 7197, 'Сумма операции с округлением': 34.0}]) == []


def test_top_five(transactions):
    assert top_five(transactions) == ('[{"Дата операции":"22.12.2021 10:19:26","Дата платежа":"20.12.2021","Сумма платежа":562.67,"Номер карты":"*7197","Сумма операции с округлением":34.0},{"Дата операции":"19.12.2021 20:13:13","Дата платежа":"20.12.2021","Сумма платежа":505.67,"Номер карты":"*5091","Сумма операции с округлением":42.92},{"Дата операции":"21.12.2021 10:09:30","Дата платежа":"20.12.2021","Сумма платежа":346.67,"Номер карты":"*7197","Сумма операции с округлением":172.69}]')