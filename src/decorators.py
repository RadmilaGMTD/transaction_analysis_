import os
from functools import wraps
from typing import Any

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_reports = os.path.join(project_root, "data", "reports.txt")


def log(file: str) -> Any:
    """Декоратор, который выводит результаты отчётов в файл"""

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: int, **kwargs: int) -> Any:
            result = func(*args, **kwargs)
            if file:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(result)
            if not file:
                with open(file_reports, "w", encoding="utf-8") as f:
                    f.write(result)
            return result

        return wrapper

    return decorator
