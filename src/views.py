from src.utils import greetings, read_excel, filtering_transactions_by_date, transaction_analysis, top_five
import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")
file_json = os.path.join(project_root, 'user_settings.json')


def get_currency_rate(file):
    """Функция выводит в файл курс валют"""
    url = f"https://www.cbr-xml-daily.ru//daily_json.js"
    response = requests.get(url)
    my_list = list()
    if response.status_code != 200:
        raise ValueError(f"Failed to get currency rate")
    data = response.json().get("Valute")
    for key, value in data.items():
        my_list.append({"currency": key, "rate": value.get("Value")})
    with open(file, 'a') as f:
        json.dump(my_list, f, indent=4)
    return my_list


def get_share_price(file):
    """Функция выводит в файл стоимость акций из S&P500"""
    my_list = list()
    load_dotenv()
    apikey = os.getenv('apikey')
    response = requests.get(f"https://financialmodelingprep.com/api/v3/quote/AAPL,AMZN,GOOGL,MSFT,TSLA?apikey={apikey}")
    data =  response.json()
    for i in data:
        my_list.append({"stock": i.get("symbol"), "price": i.get("price")})
    with open(file, 'a') as f:
        json.dump(my_list, f, indent=4)
    return my_list



def users(user_data, file, file_xlx):
    """Функция для взаимодействия с пользователем"""
    greetings_result = greetings(user_data)
    transactions_excel = read_excel(file_xlx)
    transactions_filter_by_date = filtering_transactions_by_date(user_data, transactions_excel)
    result_transaction_analysis = transaction_analysis(transactions_filter_by_date)
    json_string = top_five(transactions_filter_by_date)
    json_data = json.loads(json_string)

    result = {"greeting" : greetings_result,
              "cards" : result_transaction_analysis,
              "top_transactions" : json_data,
              "currency_rates" : get_currency_rate(file),
              "stock_prices" : get_share_price(file)}

    result_json = json.dumps(result, ensure_ascii=False)
    return result_json


users('20.12.2021 16:44:00', file_json, file_excel)
