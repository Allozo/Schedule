import pytest
import json
from schedule.MAISchedule import MAISchedule, load_html, save_html, load_json, save_json

dict_file_name = {
    "all_groups_html": "schedule\\test\\file_for_test\\all_groups.html",
    "all_groups_json": "schedule\\test\\file_for_test\\all_groups.json",
    "days_on_week_html": "schedule\\test\\file_for_test\\days_on_week.html",
    "days_on_week_json": "schedule\\test\\file_for_test\\days_on_week.json",
    "all_subjects_in_day_json": "schedule\\test\\file_for_test\\all_subjects_in_day.json",
    "list_html_files_json": "schedule\\test\\file_for_test\\list_html_files.json",
    "all_schedule_for_group_json": "schedule\\test\\file_for_test\\all_schedule_for_group.json",
}

const_name = {
    "name_course": "3 курс",
    "name_institute": "Институт №3",
    "name_field": "Бакалавриат",
    "name_day": "Вт",
}


def test_get_courses():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    list_courses = schedule.get_courses(html_page_all_group)

    all_groups = load_json(dict_file_name["all_groups_json"])
    list_json_courses = list(all_groups.keys())

    assert list_courses == list_json_courses


def test_get_institute():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    list_institutes = schedule.get_institute(
        html_page_all_group, const_name["name_course"]
    )

    all_groups = load_json(dict_file_name["all_groups_json"])
    list_json_institute = list(all_groups[const_name["name_course"]].keys())

    assert list_institutes == list_json_institute


def test_get_field():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])
    list_fields = schedule.get_field(
        html_page_all_group, const_name["name_course"], const_name["name_institute"]
    )
    all_groups = load_json(dict_file_name["all_groups_json"])

    list_json_fields = list(
        all_groups[const_name["name_course"]][const_name["name_institute"]].keys()
    )

    assert list_fields == list_json_fields


def test_get_group():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])

    list_groups = schedule.get_group(
        html_page_all_group,
        const_name["name_course"],
        const_name["name_institute"],
        const_name["name_field"],
    )

    all_groups = load_json(dict_file_name["all_groups_json"])

    list_json_group = all_groups[const_name["name_course"]][
        const_name["name_institute"]
    ][const_name["name_field"]]

    assert list_groups == list_json_group


def test_parsing_html_with_all_groups():
    schedule = MAISchedule()

    html_page_all_group = load_html(dict_file_name["all_groups_html"])

    # Получим словарь со всеми курсами, институтами, направлениями и группами
    dict_all_courses = {}

    list_courses = schedule.get_courses(html_page_all_group)
    for course in list_courses:
        dict_all_institutes = {}
        list_institute = schedule.get_institute(html_page_all_group, course)
        for institute in list_institute:
            dict_all_fields = {}
            list_fields = schedule.get_field(html_page_all_group, course, institute)
            for field in list_fields:
                dict_all_group = []
                list_group = schedule.get_group(
                    html_page_all_group, course, institute, field
                )
                for group in list_group:
                    dict_all_group.append(group)
                dict_all_fields[field] = dict_all_group
            dict_all_institutes[institute] = dict_all_fields
        dict_all_courses[course] = dict_all_institutes

    loads_json = load_json(dict_file_name["all_groups_json"])

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


def test_all_days_on_week():
    schedule = MAISchedule()

    html_days_on_week = load_html(dict_file_name["days_on_week_html"])

    list_days_on_week = schedule.get_all_days_on_week(html_days_on_week)

    list_json = load_json(dict_file_name["days_on_week_json"])

    assert list_days_on_week == list_json


def test_get_all_subjects_in_day():
    schedule = MAISchedule()

    html_days_on_week = load_html(dict_file_name["days_on_week_html"])

    list_subjects_in_day = schedule.get_all_subjects_in_day(html_days_on_week, "Вт")

    list_json_all_subjects_in_day = load_json(dict_file_name["all_subjects_in_day_json"])

    assert list_subjects_in_day == list_json_all_subjects_in_day

def test_get_all_schedule_from_list_html():
    schedule = MAISchedule()

    dict_number_week_html_week = load_json(dict_file_name["list_html_files_json"])

    tmp = schedule.get_all_schedule_from_list_html(dict_number_week_html_week)

    right_schedule_for_group = load_json(dict_file_name["all_schedule_for_group_json"])

    assert tmp == right_schedule_for_group