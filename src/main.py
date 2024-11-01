import os
from typing import Any

from src.reports import spending_by_category
from src.services import users_cash
from src.views import users_analysis

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_excel = os.path.join(project_root, "data", "operations.xlsx")
file_json = os.path.join(project_root, "data", "user_settings.json")


def main(user_date: str, file_j: str, file_e: str, user_year: str, user_mont: str, user_category: str) -> Any:
    print(users_analysis(user_date, file_j, file_e))
    print(users_cash(user_year, user_mont))
    print(spending_by_category(user_category, user_date))


main("20.12.2021 16:44:00", file_json, file_excel, "2021", "12", "Супермаркеты")
