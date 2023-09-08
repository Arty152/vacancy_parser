import os
import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class API(ABC):
    @abstractmethod
    def get_api(self, search_query: str) -> list:
        pass


class HeadHunterAPI(API):

    def get_api(self, search_query: str):
        data = []
        page_count = 0
        while True:
            params = {'text': search_query,
                      'page': page_count,
                      'area': 113,
                      'per_page': 100,
                      'only_with_salary': True,
                      'period': 30}
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.ok:
                page_count += 1
                data.extend(response.json()['items'])
                continue
            return data


class SuperJobAPI(API):

    def get_api(self, search_query: str):
        data = []
        page_count = 0
        while page_count != 20:
            period_date = datetime.now() - timedelta(days=30)
            unix_date = period_date.timestamp()
            headers = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}
            params = {'keyword': search_query,
                      'page': page_count,
                      'count': 100,
                      'no_agreement': 1,
                      'date_published_from': unix_date}
            response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=headers, params=params)
            if response.ok:
                page_count += 1
                data.extend(response.json()['objects'])
                continue
            return data
        return data
