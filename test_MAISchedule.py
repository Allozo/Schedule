import time
from MAISchedule import MAISchedule


def full_test():
    d = MAISchedule()
    d.update_schedule()

    for course in d.courses:
        for institute in d.courses[course]:
            for fields in d.courses[course][institute]:
                for group in d.courses[course][institute][fields]:
                    url_group = d.courses[course][institute][fields][group]
                    print('url --' + url_group)
                    schedule = d.get_schedule_for_group(url_group)

                    for i in schedule:
                        time.sleep(5)
                        print(schedule[i][0] + ' -- ' + schedule[i][1])
                        print(d.get_schedule_on_week(schedule[i][1]))


def test_print_all_schedule(d):
    url_my_group = 'https://mai.ru/education/schedule/detail.php?group=М3О-226Б-19'
    my_schedule = d.get_schedule_for_group(url_my_group)
    d.print_schedule_all(my_schedule)


def test_print_schedule_on_week(d):
    url_week = 'https://mai.ru/education/schedule/detail.php?group=М3О-226Б-19&week=2'
    my_schedule_two_week = d.get_schedule_on_week(url_week)
    d.print_schedule_on_week(my_schedule_two_week)


def test():
    d = MAISchedule()
    d.update_schedule()

    # вывести все расписание для группы
    test_print_all_schedule(d)

    # вывести расписание для второй недели
    # test_print_schedule_on_week(d)


def main():
    test()


if __name__ == '__main__':
    main()
