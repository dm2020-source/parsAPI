from bs4 import BeautifulSoup as Bs
import requests
import re
import pandas as pd
from pprint import pprint

main_link = 'https://hh.ru' #/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true'
params = {'L_save_area': 'true', 'clusters': 'true', 'enable_snippets': 'true', 'text': 'python', 'showClusters': 'true'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; rv:86.0) Gecko/20100101 Firefox/86.0'}
link = f'{main_link}/search/vacancy/'

response = requests.get(link, params=params, headers=headers)

#soup = Bs(response, 'lxml')
soup = Bs(response.text, 'html.parser')

if response.ok:

    vacancy_list = soup.findAll('div',{'class': 'vacancy-serp-item HH-VacancySidebarTrigger-Vacancy'})

    page_list = soup.findAll('div', {'data-qa': 'pager-block'})

    vacansys = []
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a').text
        vacancy_link = vacancy.find('span', {'class': 'resume-search-item__name'}).find('a')['href']

        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not vacancy_salary:
            vacancy_salary_min = None
            vacancy_salary_max = None
            vacancy_salary_currency = None
        else:
            vacancy_salary = vacancy_salary.getText().replace(u'\xa0', u'')
            salaries = vacancy_salary.split('-')
            salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
            vacancy_salary_min = int(salaries[0])
            if len(salaries) > 1:
                salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                vacancy_salary_max = int(salaries[1])
            else:
                vacancy_salary_max = None

        vacancy_data['vacancy_name'] = vacancy_name
        vacancy_data['vacancy_salary'] = vacancy_salary
        vacancy_data['vacancy_salary_min'] = vacancy_salary_min
        vacancy_data['vacancy_salary_max'] = vacancy_salary_max
        vacancy_data['vacancy_link'] = vacancy_link

        vacansys.append(vacancy_data)
        pprint(vacansys)
