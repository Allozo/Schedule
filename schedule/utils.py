import json
import requests


def get_html(url: str):
    """
    По переданному url получаем html. Если код ответа не 200, то вернём ошибку.

    Args:
        url (str): Ссылка на страницу, html которой хотим получить.

    Returns:
        str: HTML страницы.
    """
    page = requests.get(url)

    assert (
        page.status_code == 200
    ), f"Не удалось получить страницу. Код ошибки: {page.status_code}"

    return page.text


def save_html(name: str, html_page: str):
    """
    Сохраняет html страницы в файл.

    Args:
        name (str): Имя (вместе с путём), под которым сохранится файл.

        html_page (str): HTML страница, которую надо сохранить ф файл.
    """
    with open(f"{name}", "w", encoding="utf-8") as file:
        file.write(html_page)


def load_html(path: str) -> str:
    """
    Загружает HTML файл с указанным путём.

    Args:
        path (str): Путь HTML файла, из которого будут загружаться данные.

    Returns:
        str: HTML страница.
    """
    data = None
    with open(f"{path}", "r", encoding="utf-8") as file:
        data = file.read()
    return data


def load_json(path: str):
    """
    Загружает json файл с указанным путём.

    Args:
        path (str): Путь json файла, из которого будут загружаться данные.

    Returns:
        dict: Данные из json файла.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json(name: str, data):
    """
    Сохраняет переданный объект в файл под указанным именем.

    Args:
        name (str): Имя (вместе с путём), под которым сохранится файл.

        data (dict): Данные, которые надо сохранить в файл.
    """
    with open(f"{name}", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
