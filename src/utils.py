from src.vacancy import Vacancy, SJVacancy, HHVacancy


def platform_choice(search_query, user_input=True):
    while user_input:
        user_input = input('На какой платформе ищем?\n'
                           '1 -> HH\n'
                           '2 -> SJ\n'
                           '3 -> HH & SJ\n'
                           '4 -> Выход\n-> ')
        if user_input == '1':
            HHVacancy.initialize_vac(search_query)
            return Vacancy.vacancies_list
        elif user_input == '2':
            SJVacancy.initialize_vac(search_query)
            return Vacancy.vacancies_list
        elif user_input == '3':
            SJVacancy.initialize_vac(search_query)
            HHVacancy.initialize_vac(search_query)
            return Vacancy.vacancies_list
        elif user_input == '4':
            exit('Работа программы завершена!')
        else:
            print('Введенные данные не соответствую меню! Пожалуйста, повторите попытку ввода.')


def display_to_console(list_class_instances) -> None:
    for vacancy in list_class_instances:
        print(vacancy)


def filter_by_salary(list_class_instances, salary_query) -> list:
    filtered_vacancies = []
    for vacancy in list_class_instances:
        if vacancy >= salary_query:
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_by_salary(list_class_instances) -> list:
    sorted_vacancies = sorted(list_class_instances, reverse=True)
    return sorted_vacancies


def display_top(sort_func, value: int):
    sorted_list = sort_func
    return sorted_list[:value]




