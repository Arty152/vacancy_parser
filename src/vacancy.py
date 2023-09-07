import re
from src.api_manager import SuperJobAPI, HeadHunterAPI


class Vacancy:
    vacancies_list = []

    def __init__(self, name, area, company, url, salary_min, salary_max,
                 currency, description, responsibility, platform):
        self.name = name
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
        return f'{self.__class__.__name__} ' \
               f'({self.name}, {self.area}, {self.company}, ' \
               f'{self.avr_salary}, {self.url})\n'

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            return int(self.avr_salary) < int(other.avr_salary)
        raise AttributeError(f'{other.avr_salary} не является экземпляром класса Vacancy')

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


class SJVac(Vacancy):

    @classmethod
    def initialize_vac(cls, search_query: str) -> list:

        for item in SuperJobAPI().get_vacancies(search_query):
            cls(
                item['profession'],
                item['town']['title'],
                item['firm_name'],
                item['link'],
                item['payment_from'],
                item['payment_to'],
                item['currency'],
                item['candidat'],
                item['work'] if item['work'] is not None else 'Данные отсутствуют или находятся в другом разделе.',
                'SuberJob'  # platform
            )


class HHVac(Vacancy):

    @classmethod
    def initialize_vac(cls, search_query: str) -> None:
        for item in HeadHunterAPI().get_vacancies(search_query):
            cls(
                item['name'],
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
