import json

from src.vacancy import Vacancy
from abc import ABC, abstractmethod


class Saver(ABC):

    @abstractmethod
    def save_file(self) -> None:
        pass

    @abstractmethod
    def load_file(self) -> list:
        pass


class JSONSaver(Saver):

    def __init__(self, filename: str):
        self.filename = filename

    def save_file(self) -> None:
        vacancies_data = []
        for vacancy in Vacancy.vacancies_list:
            vacancies_data.append(vacancy.__dict__)
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_data, f, indent=2, ensure_ascii=False)

    def load_file(self) -> list:
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def delete_vacancy(self) -> None:
        vacancies_data = self.load_file()
        vacancies_data.clear()
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def merge_json_files(first_file_path, second_file_path, output_file_path):
        with open(first_file_path, 'r', encoding="utf-8") as file1:
            data1 = json.load(file1)

        with open(second_file_path, 'r', encoding="utf-8") as file2:
            data2 = json.load(file2)

        result = data1 + data2
        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            return json.dump(result, output_file, ensure_ascii=False, indent=4)
