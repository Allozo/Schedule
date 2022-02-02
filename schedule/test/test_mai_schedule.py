import pytest
import json
from schedule.MAISchedule import MAISchedule, load_html

dict_file_name = {
    "all_groups_html": "schedule\\test\\file_for_test\\all_groups.html",
    "all_groups_json": "schedule\\test\\file_for_test\\all_groups.json",
}


def test_get_courses():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    list_courses = schedule._MAISchedule__get_courses(html_page_all_group)

    with open(dict_file_name["all_groups_json"], "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    list_json_courses = list(loads_json.keys())

    assert list_courses == list_json_courses


def test_get_institute():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    name_course = "3 курс"
    list_institutes = schedule._MAISchedule__get_institute(
        html_page_all_group, name_course
    )

    with open(dict_file_name["all_groups_json"], "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    list_json_institute = list(loads_json[name_course].keys())

    assert list_institutes == list_json_institute


def test_get_field():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    name_course = "3 курс"
    name_institute = "Институт №3"
    list_fields = schedule._MAISchedule__get_field(
        html_page_all_group, name_course, name_institute
    )

    with open(dict_file_name["all_groups_json"], "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    list_json_fields = list(loads_json[name_course][name_institute].keys())

    assert list_fields == list_json_fields


def test_get_group():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    name_course = "3 курс"
    name_institute = "Институт №3"
    name_field = "Бакалавриат"
    list_groups = schedule._MAISchedule__get_group(
        html_page_all_group, name_course, name_institute, name_field
    )

    with open(dict_file_name["all_groups_json"], "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    list_json_group = loads_json[name_course][name_institute][name_field]

    assert list_groups == list_json_group


def test_parsing_html_with_all_groups():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])

    # Получим словарь со всеми курсами, институтами, направлениями и группами
    dict_all_courses = {}

    list_courses = schedule._MAISchedule__get_courses(html_page_all_group)
    for course in list_courses:
        dict_all_institutes = {}
        list_institute = schedule._MAISchedule__get_institute(
            html_page_all_group, course
        )
        for institute in list_institute:
            dict_all_fields = {}
            list_fields = schedule._MAISchedule__get_field(
                html_page_all_group, course, institute
            )
            for field in list_fields:
                dict_all_group = []
                list_group = schedule._MAISchedule__get_group(
                    html_page_all_group, course, institute, field
                )
                for group in list_group:
                    dict_all_group.append(group)
                dict_all_fields[field] = dict_all_group
            dict_all_institutes[institute] = dict_all_fields
        dict_all_courses[course] = dict_all_institutes

    with open(dict_file_name["all_groups_json"], "r", encoding="utf-8") as file:
        loads_json = json.load(file)

    # Получим конкретное значения из загруженного json
    course = list(loads_json.keys())[0]
    institute = list(loads_json[course].keys())[0]
    field = list(loads_json[course][institute].keys())[0]
    group = loads_json[course][institute][field][0]

    # Проверка конкретных значений
    assert loads_json.keys() == dict_all_courses.keys()
    assert loads_json[course].keys() == dict_all_courses[course].keys()
    assert (
        loads_json[course][institute].keys()
        == dict_all_courses[course][institute].keys()
    )
    assert (
        loads_json[course][institute][field]
        == dict_all_courses[course][institute][field]
    )

    # Проверка всего json
    assert loads_json == dict_all_courses
