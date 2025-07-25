import json

from mypyc.transform.exceptions import primitive_call

from src.parser import HeadHunterAPI, Parser
from src.utils import get_users_settings
from src.config import config
from src.postrges_db import PostgresDB
from src.manager_db import DBManager

def main():
    """Главная фунцкия для работы программы"""
    user_platform = input('Выберите платформу. "HH.ru - введите \'H\', другая - введите \'Other\' ').lower()
    if user_platform == 'h':
        hh = HeadHunterAPI()
    user_input_list_emp = input('Подтвердите ранее заданный список работодателей. "Подтверждаю" введите \'Y\', другой список - введите \'Other\' ').lower()
    if user_input_list_emp == 'y':
        list = get_users_settings('data/user_settings.json')
        user_list_employer = list['user_employer_id']
    list_employer = hh.get_employer_data(user_list_employer)
    data_vacancies = hh.get_employer_vacancies(user_list_employer)
    list_vacancies = hh.create_data_dict_vacancies(data_vacancies)

    name_search = input('введите имя для сохдания база данных поиска ').lower()

    params = config()

    connect_db= PostgresDB.created_postgres_conn(params)
    create_db = connect_db.create_database(name_search)
    table_vacancies = connect_db.create_table_vacancies(name_search)
    insert_vacancies = connect_db.insert_data_vacancies(name_search, list_vacancies)
    table_emlpoyers = connect_db.create_table_emloyers(name_search)
    insert_employers = connect_db.insert_data_empoloyers(name_search, list_employer)

    manager = DBManager(**params, name_base=name_search)


    while True:
        user_input_choose_action = int(input("выберитe, что нужно сделать:\n"
                                         "1. Получить список компаний и кол-во вакансий у каждой компании\n"
                                         "2. Получить список всех вакансий\n"
                                         "3. Получить среднюю зарплату по вакансии\n"
                                         "4. Получить список вакансий, у которых зарплата выше средней\n"
                                         "5. получить список всех вакансий по фразе\n"
                                            "6. Завершить "))

        if user_input_choose_action == 1:
            count_vacancies = manager.get_companies_and_vacancies_count()
            print(count_vacancies)
            # with open('result/count_vacancies.json', 'w', encoding='utf-8') as f:
            # json.dump(count_vacancies, f, indent=4, ensure_ascii=False)
        elif user_input_choose_action == 2:
            all_vacancies = manager.get_all_vacancies()
            print(all_vacancies)
            # with open('result/all_vacancies.json', 'w', encoding='utf-8') as f:
            # json.dump(all_vacancies, f, indent=4, ensure_ascii=False)
        elif user_input_choose_action == 3:
            avg_salary = manager.get_avg_salary()
            print(avg_salary)
            # with open('result/avg_salary.json', 'w', encoding='utf-8') as f:
            # json.dump(avg_salary, f, indent=4, ensure_ascii=False)
        elif user_input_choose_action == 4:
            higher_salary = manager.get_vacancies_with_higher_salary()
            print(higher_salary)
            # with open('result/higher_salary.json', 'w', encoding='utf-8') as f:
            # json.dump(higher_salary, f, indent=4, ensure_ascii=False)
        elif user_input_choose_action == 5:
            key_word = input('введите ключевый слова для поиска вакансий ').lower().split()
            search_word = manager.get_vacancies_with_keyword(key_word)
            # with open('result/key_word.json', 'w', encoding='utf-8') as f:
            # json.dump(key_word, f, indent=4, ensure_ascii=False)
            print(search_word)
        elif user_input_choose_action == 6:
            break
        else:
            print('Вы выбрали неверный вариант')



if __name__ == '__main__':
    print(main())
