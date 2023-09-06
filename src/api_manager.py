import os
import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class GetAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> list:
        pass


class HeadHunterAPI(GetAPI):

    def get_vacancies(self, search_query: str):
        params = {'text': search_query,
                  'area': 113,
                  'per_page': 100,
                  'only_with_salary': True,
                  'period': 30}
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        if response.ok:
            data = response.json()['items']
            return data


class SuperJobAPI(GetAPI):

    def get_vacancies(self, search_query: str):
        period_date = datetime.now() - timedelta(days=30)
        unix_date = period_date.timestamp()
        headers = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}
        params = {'keyword': search_query,
                  'count': 100,
                  'date_published_from': unix_date}
        response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=headers, params=params)
        if response.ok:
            data = response.json()['objects']
            return data
