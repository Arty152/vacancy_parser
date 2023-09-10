import json
from abc import ABC, abstractmethod


class Saver(ABC):

    @abstractmethod
    def save_vacancy(self, filename, vacancies_list) -> None:
        pass

    @abstractmethod
    def get_vacancy(self, filename, *keywords) -> list:
        pass

    @abstractmethod
    def del_vacancy(self, filename, id_vacancy) -> None:
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

    def get_vacancy(self, filename, *keywords) -> list:
        filtered_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            for data in file_data:
                for word in keywords:
                    values = []
                    for i in data.values():
                        values.append(str(i))
                    values_str = ' '.join(values).lower()
                    if word.lower() in values_str:
                        filtered_list.append(data)
            return filtered_list

    def del_vacancy(self, filename, id_vacancy) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
        vacancy_deleted = False
        for data in file_data:
            if id_vacancy in data.values():
                file_data.remove(data)
                print(f'Вакансия с ID {id_vacancy} успешно удалена!')
                vacancy_deleted = True
        if not vacancy_deleted:
            print(f'Вакансии с ID {id_vacancy} не существует')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(file_data, f, indent=2, ensure_ascii=False)
