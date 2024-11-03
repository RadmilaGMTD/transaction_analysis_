import os
import tempfile

from src.decorators import log

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_reports = os.path.join(project_root, "data", "reports.txt")


def test_log_good() -> None:
    """Тестирует выполнение тестовой декорированной функции"""

    def my_function() -> str:
        return "test"

    result = my_function()
    assert result == "test"


def test_log_txt() -> None:
    """Тестирует запись в файл после успешного выполнения"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        log_file_path = tmp_file.name

    @log(file=log_file_path)
    def my_function() -> str:
        return "test"

    my_function()
    with open(log_file_path, "r", encoding="utf-8") as file:
        text = file.read()
        assert "test" in text


def test_log_caps_without_filename() -> None:
    """Тестирует вывод в файл, если путь не задан"""

    @log(file="")
    def my_function() -> str:
        return "test"

    my_function()
    with open(file_reports, "r", encoding="utf-8") as file:
        text = file.read()
        assert "test" in text
