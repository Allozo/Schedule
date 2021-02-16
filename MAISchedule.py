from bs4 import BeautifulSoup
from ISchedule import ISchedule
import requests


class MAISchedule(ISchedule):
    def __init__(self):
        # Сайт откуда будем брать расписание
        self.official_website = "https://mai.ru/education/schedule/"
        self.courses = dict()

    def update_schedule(self):
        f"""
        Данный метод получает html с сайта {self.official_website} и парсит его.
        :return: Возвращает словари курсов, институтов, направлений 
            подготовки, групп и ссылки на их расписание в виде словаря.
        """
        start_page_html = self.__get_html_page(self.official_website)

        soup = BeautifulSoup(start_page_html, "html.parser")
        html_courses = soup.findAll(class_='sc-container')

        self.courses = self.__get_courses(html_courses)

    @staticmethod
    def __get_html_page(url):
        """ проверим есть ли подключение """
        page = requests.get(url)
        try:
            assert page.status_code == 200
            return page.text
        except AssertionError:
            print(f"Не удалось получить. Код ошибки {page.status_code}")
            print("Завершение работы.")
            exit(1)

    def __get_courses(self, html_courses):
        """
        Получает на вход html блок, где находятся все курсы. Вытаскиваем курс
            (его имя), а потом получаем для него институты.
        :param html_courses: блок html страницы, где находятся все курсы.
        :return: возвращает словари всех курсов.
        """
        courses = dict()
        for html_course in html_courses:
            '''получаем название курса'''
            html_name_course = html_course.findAll(class_='sc-container-header')
            name_course = html_name_course[0].contents[0]

            '''получим институты внутри курса'''
            html_institutes = html_course.findAll('div', class_='sc-table-row')
            courses[name_course] = self.__get_institutes(html_institutes)

        return courses

    def __get_institutes(self, html_institutes):
        """
        Получает на вход html блок, где находятся все институты для опрделенного
            курса. Вытаскиваем название института, а потом получаем для него все
            направления подготовки.
        :param html_institutes: блок html страницы, где находятся все
            институты.
        :return: возвращает словари всех институтов для конкретного курса.
        """
        all_institute = dict()
        for html_institute in html_institutes:
            '''получаем название институтов для каждого курса'''
            html_name = html_institute.findAll('a', class_='sc-table-col')
            name_institute = html_name[0].contents[0]

            '''получим направления подготовки внутри института'''
            html_fields = html_institute.findAll(class_='sc-groups')
            all_institute[name_institute] = self.__get_fields(html_fields)

        return all_institute

    def __get_fields(self, html_fields):
        """
        Получает на вход html блок, где находятся все направления подготовки для
            определённого института. Вытаскиваем названиянаправлений подготовки,
            а потом для них получаем все группы.
        :param html_fields: блок html страницы, где находятся все направления
            подготовки.
        :return: возвращает все направления подготовки для конкретного
            института.
        """
        all_field = dict()
        for html_field in html_fields:
            '''получаем название направления подготовки'''
            name_field = html_field.findAll(class_='sc-program')[0].contents[0]

            ''' получим все группы внутри направления подготовки'''
            html_groups = html_field.findAll('a', class_='sc-group-item')

            groups = self.__get_groups(html_groups)
            all_field[name_field] = groups

        return all_field

    def __get_groups(self, html_groups):
        """
        Получает на вход html блок, где находятся все группы для определённого
            направления подготовки. Вытаскиваем названия группы, а потом для неё
            получаем ссылку на её расписание.
        :param html_groups: блок html страницы, где находятся все группы.
        :return: возвращает все группы и ссылки на их расписание для конкретного
            направления подготовки.
        """
        groups = dict()
        for html_group in html_groups:
            ''' получим название группы'''
            name_group = html_group.contents[0]

            ''' получи url группы'''
            url_group = html_group['href']
            groups[name_group] = self.official_website + url_group

        return groups

    def get_schedule_for_group(self, url_group):
        """
        Получает на вход ссылку на расписание конкретной группы.
        :param url_group:
        :return: Возвращает словарь состоящий из недель, дней недели и занятий.
        """

        start_page = self.__get_html_page(url_group)

        soup = BeautifulSoup(start_page, "html.parser")
        html_weeks = soup.find('table', class_='table')

        schedule = self.__get_all_week(html_weeks)
        return schedule

    def __get_all_week(self, html_weeks):
        number_name_url_week = dict()

        html_list_weeks = html_weeks.findAll('td')
        flag = -1

        html_number = html_list_weeks[0::2]
        html_name_url = html_list_weeks[1::2]
        for (number, name_and_url) in zip(html_number, html_name_url):
            number_week = number.contents[0]

            name_and_url = name_and_url.contents[0]

            if ('<' or '>') not in str(name_and_url):
                name_week = name_and_url
                url_week = ''
                flag = str(number_week)
            else:
                name_week = name_and_url.contents[0]
                url_week = self.official_website + 'detail.php' + name_and_url['href']

            number_name_url_week[number_week] = [name_week, url_week]

        '''эта штука нужна из-за того, что для текущей недели нет ссылки, а 
            значит её нужно ставить отдельно ручками'''
        if flag == '1':
            new_name = number_name_url_week[flag][0]
            new_url = number_name_url_week[str(2)][1][:-1] + flag
            number_name_url_week[flag] = [new_name, new_url]
        else:
            new_name = number_name_url_week[flag][0]
            new_url = number_name_url_week[str(1)][1][:-1] + flag
            number_name_url_week[flag] = [new_name, new_url]

        return number_name_url_week

    def get_schedule_on_week(self, url_week):
        # откроем html из файла
        # with open('html_site.html', 'r', encoding='utf-8') as file:
        #     start_page = file.read()

        start_page = self.__get_html_page(url_week)

        # with open('html_site.html', 'w', encoding='utf-8') as file:
        #     file.write(start_page)

        soup = BeautifulSoup(start_page, "html.parser")

        # получим html дни
        html_weeks = soup.findAll('div', class_='sc-container')

        schedule_on_week = self.__get_days(html_weeks)
        return schedule_on_week

    def __get_days(self, html_weeks):
        days_on_week = dict()
        # обрабытываем день
        for html_day in html_weeks:
            # получаем все предметы за день
            day = dict()
            date = str(html_day.find(class_='sc-day-header').contents[0])
            day_of_week = html_day.find(class_='sc-day').contents[0]

            # обработаем предметы в день
            today_item = self.___get_items(html_day)
            day['item'] = today_item
            day['date'] = date
            days_on_week[day_of_week] = day
        return days_on_week

    @staticmethod
    def ___get_items(html_day):
        now_day = html_day.find(class_='sc-table-detail').findAll(class_='sc-table-row')
        one_day = dict()
        list_items = []
        for item in now_day:
            name_item = item.findAll(class_='sc-title')[0].contents[0]
            time_item = item.findAll(class_='sc-item-time')[0].contents[0]
            type_time = item.findAll(class_='sc-item-type')[0].contents[0]
            map_item = str(item.findAll('div', class_='sc-item-location')[1].contents[2]).replace('\t', '').replace('\n', '')
            lecture_item = item.findAll('span', class_='sc-lecturer')[0].contents

            one_day['name_item'] = name_item
            one_day['time_item'] = time_item
            one_day['type_item'] = type_time
            one_day['map_item'] = map_item
            one_day['lecture_item'] = lecture_item

            list_items.append(one_day.copy())

        return list_items

    def print_schedule_all(self, list_all_url_weeks):
        for i in list_all_url_weeks:
            print(list_all_url_weeks[i][0])
            m = self.get_schedule_on_week(list_all_url_weeks[i][1])
            self.print_schedule_on_week(m)


    def print_schedule_on_week(self, dict_schedule):
        for name_date in dict_schedule:
            date = dict_schedule[name_date]['date']
            items = dict_schedule[name_date]['item']
            print(f"    {date} -- {name_date}")
            for i in enumerate(items):
                number_item = i[0] 
                item = i[1]
                time_item = item['time_item']
                type_item = item['type_item']
                map_item = item['map_item']
                lecture_item = item['lecture_item']
                print(f"        {int(i[0]) + 1}: {item['name_item']} -- {time_item} -- {lecture_item} -- {type_item} -- {map_item}")
                

