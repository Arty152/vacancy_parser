import json
from abc import ABC, abstractmethod


class Saver(ABC):

    @abstractmethod
    def save_vacancy(self, filename, vacancies_list) -> None:
        pass

    @abstractmethod
    def get_vacancy(self, file, *keywords) -> list:
        pass

    @abstractmethod
    def del_vacancy(self) -> list:
        pass


class JSONSaver(Saver):

    def save_vacancy(self, filename, vacancies_list) -> None:
        vacancies_data = []
        for vacancy in vacancies_list:
            data = {'Платформа': vacancy.platform,
                    'ID': vacancy.vacancy_id,
                    'Вакансия': vacancy.name,
                    'Ссылка': vacancy.url,
                    'Населенный пункт': vacancy.area,
                    'Компания': vacancy.company,
                    'Зарплата': vacancy.avr_salary,
                    'Описание': vacancy.description,
                    'Обязанности': vacancy.responsibility}
            vacancies_data.append(data)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies_data, f, indent=2, ensure_ascii=False)

    def get_vacancy(self, file, *keywords) -> list:
        pass

    def del_vacancy(self) -> list:
        pass
