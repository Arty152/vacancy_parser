import json

from src.file_manager import JSONSaver
from src.utils import platform_choice, display_to_console, filter_by_salary, sort_by_salary, display_top

FILE_DEFAULT = 'vacancies.json'
FILE_FILTERED_SALARY = 'filtered_vacancies_by_salary.json'
FILE_SORTED_SALARY = 'sorted_vacancies_by_salary.json'
FILE_FILTERED_KEYWORDS = 'vacancies_by_keywords.json'
FILE_TOP_VACANCIES = 'top_by_salary.json'

if __name__ == '__main__':
    print('Данная программа выполняет поиск вакансии по России по Вашему запросу на платформах HeadHunter и SuperJob.\n'
          'Внимание: поиск осуществляется по всем разделам вакансий!')
    search_query = input('Введите поисковый запрос: ')
    while True:
        query_results = platform_choice(search_query)
        JSONSaver().save_vacancy(FILE_DEFAULT, query_results)
        print(f'По запросу {search_query} найдено вакансий: {len(query_results)}.\n'
              f'Данные сохранены в файл {FILE_DEFAULT}')

        choice_method = input('Варианты работы с полученными данными:\n'
                              '1 -> Отобразить в консоли.\n'
                              '2 -> Отфильтровать по указанной з/п.\n'
                              '3 -> Выполнить сортировку по з/п.\n'
                              '4 -> Вывести топ по з/п.\n'
                              '5 -> Получить вакансии по ключевым словам.\n'
                              '6 -> Удалить вакансию по ID.\n'
                              '0 -> Завершение работы программы.\n')

        if choice_method == '1':
            display_to_console(query_results)
            break

        elif choice_method == '2':
            count_error = 0
            while count_error <= 2:
                salary_query = input('Введите желаемую зарплату для фильтрации: ')
                try:
                    salary_query = int(salary_query)
                    break
                except ValueError:
                    count_error += 1
                    print(f'"{salary_query}" не является типом данных int. Пожалуйста, введите целое число.')
            if count_error <= 2:
                filtered_salaries = filter_by_salary(query_results, salary_query)
                JSONSaver().save_vacancy(FILE_FILTERED_SALARY, filtered_salaries)
                print(f'По запросу {search_query} от {salary_query} руб. найдено вакансий: {len(filtered_salaries)}.\n'
                      f'Данные сохранены в файл {FILE_FILTERED_SALARY}')
            else:
                exit("Превышено количество попыток ввода. Программа завершена.\nПовторите запуск программы!")
            break

        elif choice_method == '3':
            sorted_salary = sort_by_salary(query_results)
            JSONSaver().save_vacancy(FILE_SORTED_SALARY, sorted_salary)
            display_to_console(sorted_salary)
            break

        elif choice_method == '4':
            user_int = int(input('Введите количество вакансий для вывода в ТОП: '))
            sorted_salary = sort_by_salary(query_results)
            top = display_top(sorted_salary, user_int)
            display_to_console(top)
            break

        elif choice_method == '5':
            keywords_input = input('Введите ключевые слова\n-> ')
            filtered = JSONSaver().get_vacancy(FILE_DEFAULT, keywords_input)
            with open(FILE_FILTERED_KEYWORDS, 'w', encoding='utf-8') as f:
                json.dump(filtered, f, indent=2, ensure_ascii=False)
            break

        elif choice_method == '6':
            print('ID вакансий можно найти в файле vacancies.json')
            id_vacancy = int(input(f'Введите ID вакансии для удаления из файла {FILE_DEFAULT}: '))
            JSONSaver().del_vacancy(FILE_DEFAULT, id_vacancy)
            print(f'Файл {FILE_DEFAULT} обновлен!')
            break

        elif choice_method == '0':
            exit('Работа программы завершена!')

        else:
            print('Введенные данные не соответствую меню! Пожалуйста, повторите попытку ввода.')
