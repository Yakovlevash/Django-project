import re
import requests

class API:

    def __init__(self, search_text: str):
        self.search_text = search_text

    def __get_full_vacancies__(self, date: str, count_vacancies: int) -> list:
        base_url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.search_text,
            'specialization': 1,
            'date_from': f"{date}T00:00:00",
            'date_to': f"{date}T23:00:00",
            'per_page': count_vacancies,
            'page': 1
        }
        response = requests.get(base_url, params=params).json()
        return response.get("items", [])

    def get_data_vacancies(self, date: str, count_vacancies: int):
        full_vacancies = self.__get_full_vacancies__(date, count_vacancies)
        response = []

        for vacancy in full_vacancies:
            vacancy_url = f'https://api.hh.ru/vacancies/{vacancy["id"]}'
            vacancy_info = requests.get(vacancy_url).json()

            if vacancy_info['salary']:
                description = ' '.join(re.sub(re.compile('<.*?>'), '', vacancy_info['description'])
                                       .strip()
                                       .split())
                description = description[:100] + '...' if len(description) >= 100 else description

                response.append({
                    'name': vacancy_info['name'],
                    'description': description,
                    'key_skills': [skill['name'] for skill in vacancy_info['key_skills']],
                    'employer': vacancy_info['employer']['name'],
                    'salary': f"{vacancy_info['salary']['from']} - {vacancy_info['salary']['to']} {vacancy_info['salary']['currency']}",
                    'area': vacancy_info['area']['name'],
                    'published_at': vacancy_info['published_at'][:10],
                    'alternate_url': vacancy_info['alternate_url']
                })

        return response
