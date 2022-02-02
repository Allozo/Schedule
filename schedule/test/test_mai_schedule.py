import pytest
import json
from schedule.MAISchedule import MAISchedule, load_html

def test_parsing_html_with_all_groups():
    schedule = MAISchedule()

    html_page_all_group = load_html("all_groups.html", "schedule\\test\\file_for_test")

    # Получим словарь со всеми курсами, институтами, направлениями и группами
    dict_all_courses = {}
    for course in schedule._MAISchedule__get_courses(html_page_all_group):
        dict_all_institutes = {}
        for institute in schedule._MAISchedule__get_institute(html_page_all_group, course):
            dict_all_fields = {}
            for field in schedule._MAISchedule__get_field(html_page_all_group, course, institute):
                dict_all_group = []
                for group in schedule._MAISchedule__get_group(html_page_all_group, course, institute, field):
                    dict_all_group.append(group)
                dict_all_fields[field] = dict_all_group
            dict_all_institutes[institute] = dict_all_fields
        dict_all_courses[course] = dict_all_institutes

    with open("schedule\\test\\file_for_test\\all_groups.json", "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    # Получим конкретное значения из загруженного json
    course = list(loads_json.keys())[0]
    institute = list(loads_json[course].keys())[0]
    field = list(loads_json[course][institute].keys())[0]
    group = loads_json[course][institute][field][0]

    # Проверка конкретных значений
    assert loads_json.keys() == dict_all_courses.keys()
    assert loads_json[course].keys() == dict_all_courses[course].keys()
    assert loads_json[course][institute].keys() == dict_all_courses[course][institute].keys()
    assert loads_json[course][institute][field] == dict_all_courses[course][institute][field]

    # Проверка всего json
    assert loads_json == dict_all_courses