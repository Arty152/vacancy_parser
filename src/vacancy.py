import re
from src.api_manager import SuperJobAPI, HeadHunterAPI


class Vacancy:
    vacancies_list = []

    def __init__(self, name, vacancy_id, area, company, url, salary_min,
                 salary_max, currency, description, responsibility, platform):
        self.name = name
        self.vacancy_id = vacancy_id
        self.area = area
        self.company = company
        self.url = url
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.__avr_salary = self.calc_salary(self.salary_min, self.salary_max)
        self.description = self.remove_html_tags(description)
        self.responsibility = self.remove_html_tags(responsibility)
        self.platform = platform
        Vacancy.vacancies_list.append(self)

    @property
    def avr_salary(self):
        return self.__avr_salary

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.platform}, {self.name}, ' \
               f'{self.vacancy_id}, {self.area}, {self.company}, {self.avr_salary}, {self.url})\n'

    def __str__(self):
        return f'{"_" * 80}\n' \
               f'Платформа: {self.platform}\n' \
               f'vacancy_id: {self.vacancy_id}\n' \
               f'Вакансия: {self.name}\n' \
               f'Ссылка: {self.url}\n' \
               f'Населенный пункт: {self.area}\n' \
               f'Компания: {self.company}\n' \
               f'Зарплата: {self.avr_salary} {self.currency}\n' \
               f'Описание:\n{self.description}\n' \
               f'Обязанности:\n{self.responsibility}'

    def __ge__(self, other):
        if isinstance(other, int):
            return int(self.avr_salary) >= other
        raise AttributeError(f'{other} не является экземпляром класса Integer')

    @staticmethod
    def calc_salary(salary_min: int, salary_max: int) -> int:
        if salary_min == 0 or salary_min is None:
            return salary_max
        elif salary_max == 0 or salary_max is None:
            return salary_min
        else:
            avr_salary = (salary_min + salary_max) // 2
            return avr_salary

    @staticmethod
    def remove_html_tags(value: str) -> str:
        """remove html <tags> from string"""
        if value:
            return re.compile(r'<[^>]+>').sub('', value)


class SJVacancy(Vacancy):

    @classmethod
    def initialize_vac(cls, search_query: str) -> None:
        for item in SuperJobAPI().get_api(search_query):
            cls(
                item['profession'],
                item['id'],
                item['town']['title'],
                item['firm_name'],
                item['link'],
                item['payment_from'],
                item['payment_to'],
                item['currency'],
                item['candidat'],
                item['work'] if item['work'] is not None else 'Данные отсутствуют или находятся в другом описании.',
                'SuberJob'  # platform
            )


class HHVacancy(Vacancy):

    @classmethod
    def initialize_vac(cls, search_query: str) -> None:
        for item in HeadHunterAPI().get_api(search_query):
            cls(
                item['name'],
                item['id'],
                item['area']['name'],
                item['employer']['name'],
                item['alternate_url'],
                item['salary']['from'],
                item['salary']['to'],
                item['salary']['currency'],
                item['snippet']['requirement'],
                item['snippet']['responsibility'],
                'HeadHunter'  # platform
            )
