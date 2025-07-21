from abc import ABC, abstractmethod
import requests
import json
import time

from mypy.strconv import indent


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса вакансий"""

    @abstractmethod
    def connect_api(self, keyword):
        """Абстрактный метод для подключения к API"""
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter и получения вакансий по ключевому слову"""

    def  connect_api(self, keyword):
        url = 'https://api.hh.ru/vacancies'
        params = {'text': keyword, 'per_page':100}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f'Произoшла ошибка: {response.status_code}')
            return None
        data_response = response.json()['items']

        return data_response

    def get_employer_data(self, list_employers):
        """Получает данные работодателя по ID по заданному списку"""

        emlpoyers_data = []
        result_list_employer = []

        for employer_id in list_employers:
            url = f"https://api.hh.ru/employers/{employer_id}"
            response = requests.get(url)
            emlpoyers_data.append(response.json())
            time.sleep(0.5)

        for employer in emlpoyers_data:
            data_employer = {
                'id': employer['id'],
                'name': employer['name'],
                'url_hh_employer': employer['alternate_url']
            }
            result_list_employer.append(data_employer)

        return result_list_employer

    def get_employer_vacancies(self, list_employers):
        """Получает все вакансии радотодателя из  заданного списка"""

        vacancies_data = []

        for employer_id in list_employers:
            url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
            vacancies = []
            page = 0
            pages = 1

            while page < pages:
                params = {
                    'page': page,
                    'per_page': 100  # Максимальное количество на странице
                }
                response = requests.get(url, params=params)
                data = response.json()
                vacancies.extend(data['items'])
                pages = data['pages']
                page += 1

            vacancies_data.append(vacancies)

        return vacancies_data

    def create_data_dict_vacancies(self, vacancies_data):
        result_list = []
        for list in vacancies_data:
            for vacancy in list:
                id = vacancy.get('id', '')
                name = vacancy.get('name', '')
                url_vacancy = vacancy.get('alternate_url', '')
                employer_id = vacancy.get('employer', {}).get('id', '')
                employer_name = vacancy.get('employer', {}).get('name', '')
                salary = vacancy.get('salary', '')
                if salary is not None:
                    salary_from = salary['from']
                    if salary_from is None:
                        salary_from = 0
                    salary_to = salary['to']
                    if salary_to is None:
                        salary_to = salary_from
                    currency_salary = salary['currency']
                else:
                    salary_from = 0
                    salary_to = 0
                    currency_salary = 'нет данных'
                requirement = vacancy.get('snippet', {}).get('requirement', '')
                responsibility = vacancy.get('snippet', {}).get('responsibility', '')
                vacancy_data = {
                    'id': id,
                    'name':name,
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'salary_currency': currency_salary,
                    'url_vacancy':url_vacancy,
                    'employer_id': employer_id,
                    'employer_name': employer_name,
                    'requirement':requirement,
                    'responsibility':responsibility
                    }
                result_list.append(vacancy_data)

        return result_list








if __name__ == '__main__':
    emp =HeadHunterAPI()
    list = emp.get_employer_data(557534)
    print(list)
