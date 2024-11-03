import json
import os
from typing import Any
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import (calculate_cashback, filtering_transactions_by_date, filtering_transactions_by_month_and_year,
                       get_category_cash, greetings, read_excel, read_excel_dataframe, top_five, transaction_analysis)
from src.views import get_currency_rate, get_share_price

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
test_file_path_excel = os.path.join(project_root, "data", "test_transactions_excel.xlsx")
test_file_path = "test_operations.json"


@pytest.fixture
def transactions() -> list:
    return [
        {
            "Дата операции": "22.12.2021 10:19:26",
            "Дата платежа": "20.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Магнит",
            "Сумма платежа": 562.67,
            "Номер карты": "*7197",
            "Сумма операции с округлением": 34.0,
        },
        {
            "Дата операции": "21.12.2021 10:09:30",
            "Дата платежа": "20.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Озон",
            "Сумма платежа": 346.67,
            "Номер карты": "*7197",
            "Сумма операции с округлением": 172.69,
        },
        {
            "Дата операции": "19.12.2021 20:13:13",
            "Дата платежа": "20.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Колхоз",
            "Сумма платежа": -505.67,
            "Номер карты": "*5091",
            "Сумма операции с округлением": 42.92,
        },
    ]


@pytest.fixture
def transactions_2() -> list:
    return [
        {"Дата операции": "22.12.2021 10:19:26", "Категория": "Супермаркет", "Кэшбэк": 20},
        {"Дата операции": "21.12.2021 10:09:30", "Категория": "Аптеки", "Кэшбэк": 10},
        {"Дата операции": "19.12.2021 20:13:13", "Категория": "Аптеки", "Кэшбэк": 10},
    ]


@pytest.mark.parametrize(
    "data, expected",
    [
        ("2021-12-31 16:44:00", "Добрый день"),
        ("2021-12-31 18:44:00", "Добрый вечер"),
        ("2021-12-31 08:44:00", "Доброе утро"),
        ("2021-12-31 00:44:00", "Доброй ночи"),
    ],
)
def test_greetings(data: str, expected: list) -> None:
    """Тестирует работу функции"""
    assert greetings(data) == expected


def test_greetings_invalid() -> None:
    """Тестирует работу функции, если задана неправильная дата"""
    assert greetings("12345") == "Неправильная дата"


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
    file_read_excel = read_excel("../data/operations.xlsx")
    expected_result = [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    assert file_read_excel == expected_result


def test_valid_file_excel_invalid() -> None:
    """Корректная работа функции без файла."""
    assert read_excel("") == []


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            "2021-12-21 10:09:30",
            [
                {
                    "Дата операции": "21.12.2021 10:09:30",
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Озон",
                    "Сумма платежа": 346.67,
                    "Номер карты": "*7197",
                    "Сумма операции с округлением": 172.69,
                },
                {
                    "Дата операции": "19.12.2021 20:13:13",
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Колхоз",
                    "Сумма платежа": -505.67,
                    "Номер карты": "*5091",
                    "Сумма операции с округлением": 42.92,
                },
            ],
        )
    ],
)
def test_filtering_transactions_by_date(data: str, transactions: list, expected: list) -> None:
    """Тестирует работу функции"""
    assert filtering_transactions_by_date(data, transactions) == expected


def test_filtering_transactions_by_date_invalid(transactions: list) -> None:
    """Тестирует работу функции, если задана неправильная дата"""
    assert filtering_transactions_by_date("1111", transactions) == "Дата введена неверно"


def test_filtering_transactions_by_date_empty_list() -> None:
    """Тестирует работу функции, если список транзакций пуст"""
    assert filtering_transactions_by_date("2020-10-10 20:13:13", []) == []


@pytest.mark.parametrize("amount, expected", [(150, 1.50), (2068.56, 20.69), (0, 0)])
def test_calculate_cashback(amount: int, expected: int) -> None:
    """Тестирует работу функции"""
    assert calculate_cashback(amount) == expected


def test_transaction_analysis(transactions: list) -> None:
    """Тестирует работу функции"""
    assert transaction_analysis(transactions) == [
        {"last_digits": "7197", "total_spent": 206.69, "cashback": 2.07},
        {"last_digits": "5091", "total_spent": 42.92, "cashback": 0.43},
    ]


def test_transaction_analysis_not_str() -> None:
    """Тестирует работу функции, если номер карты не строка"""
    assert (
        transaction_analysis(
            [
                {
                    "Дата операции": "22.12.2021 10:19:26",
                    "Дата платежа": "20.12.2021",
                    "Номер карты": 7197,
                    "Сумма операции с округлением": 34.0,
                }
            ]
        )
        == []
    )


def test_top_five(transactions: list) -> None:
    """Тестирует работу функции"""
    assert top_five(transactions) == [
        {"amount": 562.67, "category": "Супермаркеты", "date": "20.12.2021", "description": "Магнит"},
        {"amount": 505.67, "category": "Супермаркеты", "date": "20.12.2021", "description": "Колхоз"},
        {"amount": 346.67, "category": "Супермаркеты", "date": "20.12.2021", "description": "Озон"},
    ]


def test_top_five_empty_list() -> None:
    """Тестирует работу функции, если список транзакций пустой"""
    assert top_five([]) == []


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (
            "2021",
            "12",
            [
                {
                    "Дата операции": "22.12.2021 10:19:26",
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Магнит",
                    "Сумма платежа": 562.67,
                    "Номер карты": "*7197",
                    "Сумма операции с округлением": 34.0,
                },
                {
                    "Дата операции": "21.12.2021 10:09:30",
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Озон",
                    "Сумма платежа": 346.67,
                    "Номер карты": "*7197",
                    "Сумма операции с округлением": 172.69,
                },
                {
                    "Дата операции": "19.12.2021 20:13:13",
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Колхоз",
                    "Сумма платежа": -505.67,
                    "Номер карты": "*5091",
                    "Сумма операции с округлением": 42.92,
                },
            ],
        ),
        ("2021", "05", []),
        ("2020", "12", []),
        ("2", "0", []),
    ],
)
def test_filtering_transactions_by_month_and_year(year: str, month: str, transactions: list, expected: list) -> None:
    """Тестирует корректную работу функции и если дата введена неправильно"""
    assert filtering_transactions_by_month_and_year(year, month, transactions) == expected


def test_read_excel_dataframe() -> None:
    """Тест на проверку работы функции с excel файлом"""
    rows = [{"id": 650703, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    df = pd.DataFrame(rows)
    df.to_excel(test_file_path_excel, index=False)
    result = read_excel_dataframe(test_file_path_excel)
    rows_dataframe = pd.DataFrame([{"id": 650703, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}])
    assert result.equals(rows_dataframe)
    os.remove(test_file_path_excel)


@patch("pandas.read_excel")
def test_valid_file_excel_dataframe(mock_read_excel: Any) -> None:
    """Корректная работа функции с файлом excel с моком."""
    mock_read_excel.return_value = pd.DataFrame(
        [{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}]
    )
    file_read_excel = read_excel_dataframe("../data/operations.xlsx")
    expected_result = pd.DataFrame([{"id": 650703.0, "state": "EXECUTED", "date": "2023-09-05T11:30:32Z"}])
    assert file_read_excel.equals(expected_result)


def test_get_category_cash(transactions_2: list) -> None:
    """Тестирует корректную работу функции"""
    assert get_category_cash(transactions_2) == {"Супермаркет": 20.0, "Аптеки": 20.0}
    assert get_category_cash([]) == "За этот период кэшбэка не было"


@patch("src.utils.requests.get")
def test_get_currency_rate(mock_get: Mock) -> None:
    """Проверка корректной работы функции"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Value": 73.5}}}
    assert get_currency_rate(test_file_path) == [{"currency": "USD", "rate": 73.5}]
    os.remove(test_file_path)


@patch("src.utils.requests.get")
def test_get_currency_rate_invalid(mock_get: Mock) -> None:
    """Проверка корректной работы функции"""
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {}
    with pytest.raises(ValueError, match="Не удалось получить курс валюты"):
        get_currency_rate(test_file_path)
        os.remove(test_file_path)


@patch("src.utils.requests.get")
def test_get_currency_rate_file(mock_get: Mock) -> None:
    """Функция проверяет как записывает файл"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Value": 73.5}}}
    valid_data = [{"currency": "USD", "rate": 73.5}]
    with open(test_file_path, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)
    assert get_currency_rate(test_file_path) == [{"currency": "USD", "rate": 73.5}]
    os.remove(test_file_path)


@patch("src.utils.requests.get")
def test_get_share_price(mock_get: Mock) -> None:
    """Проверка корректной работы функции"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"symbol": "AAPL", "name": "Apple Inc.", "price": 225.91}]
    assert get_share_price(test_file_path) == [{"stock": "AAPL", "price": 225.91}]
    os.remove(test_file_path)


@patch("src.utils.requests.get")
def test_get_share_price_invalid(mock_get: Mock) -> None:
    """Проверка корректной работы функции"""
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {}
    with pytest.raises(ValueError, match="Не удалось получить основные акции"):
        get_share_price(test_file_path)
        os.remove(test_file_path)


@patch("src.utils.requests.get")
def test_get_share_price_file(mock_get: Mock) -> None:
    """Функция проверяет как записывает файл"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"symbol": "AAPL", "name": "Apple Inc.", "price": 225.91}]
    valid_data = [{"stock": "AAPL", "price": 225.91}]
    with open(test_file_path, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)
    assert get_share_price(test_file_path) == [{"stock": "AAPL", "price": 225.91}]
    os.remove(test_file_path)
