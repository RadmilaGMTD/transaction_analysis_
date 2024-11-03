import json
from unittest.mock import Mock, patch

from src.views import users_analysis


@patch("src.views.get_share_price")
@patch("src.views.get_currency_rate")
@patch("src.views.top_five")
@patch("src.views.transaction_analysis")
@patch("src.views.filtering_transactions_by_date")
@patch("src.views.read_excel")
@patch("src.views.greetings")
def test_users_analysis(
    mock_greetings: Mock,
    mock_read_excel: Mock,
    mock_filtering_transactions_by_date: Mock,
    mock_transaction_analysis: Mock,
    mock_top_five: Mock,
    mock_get_currency_rate: Mock,
    mock_get_share_price: Mock,
) -> None:
    mock_greetings.return_value = "Добро пожаловать!"
    mock_read_excel.return_value = [{"Дата операции": "01.01.2021 12:00:00", "Сумма платежа": 100}]
    mock_filtering_transactions_by_date.return_value = [{"Дата операции": "01.01.2021 12:00:00", "Сумма платежа": 100}]
    mock_transaction_analysis.return_value = [{"last_digits": "7197", "total_spent": 2395.52, "cashback": 23.96}]
    mock_top_five.return_value = json.dumps([{"Дата операции": "01.01.2021 12:00:00", "Сумма платежа": 100}])
    mock_get_currency_rate.return_value = {"USD": 73.4, "EUR": 86.5}
    mock_get_share_price.return_value = {"AAPL": 150, "TSLA": 750}
    user_date = "01-01-2021 12:00:00"
    file = "currency_stock"
    file_xlx = "transactions.xlsx"
    result = users_analysis(user_date, file, file_xlx)
    expected_result = {
        "greeting": "Добро пожаловать!",
        "cards": [{"last_digits": "7197", "total_spent": 2395.52, "cashback": 23.96}],
        "top_transactions": [{"Дата операции": "01.01.2021 12:00:00", "Сумма платежа": 100}],
        "currency_rates": {"USD": 73.4, "EUR": 86.5},
        "stock_prices": {"AAPL": 150, "TSLA": 750},
    }

    expected_json_result = json.dumps(expected_result, ensure_ascii=False, indent=4)
    assert result == expected_json_result
