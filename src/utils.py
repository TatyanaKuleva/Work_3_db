import json

def get_users_settings(path: str) -> dict:
    """функция принимает путь до JSON-файла и возвращает список словарей с данными о настройках пользователя"""
    with open(path, "r", encoding="utf-8") as data_file:
        data_settings = json.load(data_file)
        return data_settings

