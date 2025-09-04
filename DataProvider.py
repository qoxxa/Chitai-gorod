import json
import os

# Получаем путь к директории, где находится этот файл
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'test_data.json')

# Открываем и загружаем JSON
with open(file_path, 'r', encoding='utf-8') as my_file:
    global_data = json.load(my_file)


class DataProvider:
    def __init__(self) -> None:
        self.data = global_data

    def get(self, prop: str) -> str:
        """Возвращает значение по ключу как строку"""
        return self.data.get(prop)

    def getint(self, prop: str) -> int:
        """Возвращает значение по ключу как целое число"""
        val = self.data.get(prop)
        if val is None:
            raise ValueError(f"Ключ '{prop}' не найден в test_data.json")
        try:
            return int(val)
        except (ValueError, TypeError):
            raise ValueError(f"Значение '{val}' для ключа '{prop}' нельзя преобразовать в int")