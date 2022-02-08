from bs4 import BeautifulSoup
from datetime import date as dt
from schedule.utils import get_html


dict_mai_url = {
    "url_all_groups": "https://mai.ru/education/schedule/",
    "url_week": "https://mai.ru/education/schedule/detail.php?group={number_group}&week={number_week}",
    "url_count_week" : "https://mai.ru/education/schedule/detail.php?group={number_group}"
}


class MAISchedule():
    def __init__(self) -> None:
        super().__init__()

    def get_url_all_groups(self):
        """
        Возвращает ссылка на страницу, где указаны все группы
        """
        return dict_mai_url["url_all_groups"]

    def get_url_schedule_on_week(self, number_week: int):
        return (
            dict_mai_url["url_week"]
            .replace("{number_week}", str(number_week))
        )

    def get_count_week(self, number_group: str):
        """
        Вернём все номера недель и границы этой недели, где есть расписание для
            выбранной группы.

        Returns:
            List[(str, str)]: Лист пар, где первый элемент - это номер недели
                (Например, '1'), а второй элемент - граница этой недели по датам
        """
        url_count_week = dict_mai_url["url_count_week"].replace("{number_group}", number_group)
        html_count_week = get_html(url_count_week)
        soup = BeautifulSoup(html_count_week, "html.parser")
        html_all_count_week = soup.find("table", class_="table").findAll('td')

        counts_week = []
        for i in range(0, len(html_all_count_week), 2):
            number_week = html_all_count_week[i].text
            range_week = html_all_count_week[i + 1].text
            counts_week.append((number_week, range_week))

        return counts_week

    # Методы для выбора группы

    def get_courses(self, html_page_all_groups: str) -> list:
        """
        Из HTML получаем список всех курсов в МАИ.

        Args:
            html_page_all_groups (str): HTML страница со списком всех курсов
                и групп МАИ - https://mai.ru/education/schedule/.

        Returns:
            list[str]: Список всех курсов в МАИ.
        """
        soup = BeautifulSoup(html_page_all_groups, "html.parser")

        list_html_courses = soup.findAll(class_="sc-container-header")

        courses = [course.text for course in list_html_courses]

        return courses

    def get_institute(self, html_page_all_groups: str, course: str) -> list:
        """
        Из HTML получаем все институты для данного курса.

        Args:
            html_page_all_groups (str): HTML страница со списком всех курсов
                и групп МАИ - https://mai.ru/education/schedule/.

            course (str): Название курса.

        Returns:
            list[str]: Список всех институтов для данного курса в МАИ.
        """
        soup = BeautifulSoup(html_page_all_groups, "html.parser")

        html_course = soup.find(
            class_="sc-container-header", string=course
        ).find_parent()
        list_html_institute = html_course.findAll("a", class_="sc-table-col")

        institutes = [institute.text for institute in list_html_institute]

        return institutes

    def get_field(self, html_page_all_groups: str, course: str, institute: str) -> list:
        """
        Из HTML получаем все направления для данного курса и института.

        Args:
            html_page_all_groups (str): HTML страница со списком всех курсов
                и групп МАИ - https://mai.ru/education/schedule/.

            course (str): Название курса.

            institute (str): Название института.

        Returns:
            list[str]: Список всех направлений для данного курса и института в МАИ.
        """
        soup = BeautifulSoup(html_page_all_groups, "html.parser")

        html_course = soup.find(
            class_="sc-container-header", string=course
        ).find_parent()

        html_institute = html_course.find(
            "a", class_="sc-table-col", string=institute
        ).find_parent()

        html_fields = html_institute.findAll(class_="sc-program")

        fields = [field.text for field in html_fields]

        return fields

    def get_group(
        self, html_page_all_groups: str, course: str, institute: str, field: str
    ) -> list:
        """
        Из HTML получаем все группы для данного курса, института и направления.

        Args:
            html_page_all_groups (str): HTML страница со списком всех курсов
                и групп МАИ - https://mai.ru/education/schedule/.

            course (str): Название курса.

            institute (str): Название института

            field (str): Название направления

        Returns:
            list[str]: Список всех групп для данного курса, института и
                направления подготовки в МАИ.
        """
        soup = BeautifulSoup(html_page_all_groups, "html.parser")

        html_course = soup.find(
            class_="sc-container-header", string=course
        ).find_parent()

        html_institute = html_course.find(
            "a", class_="sc-table-col", string=institute
        ).find_parent()

        html_field = html_institute.find(
            class_="sc-program", string=field
        ).find_parent()

        html_groups = html_field.findAll(class_="sc-group-item")

        list_groups = [group.text for group in html_groups]

        return list_groups

    def get_all_days_on_week(self, html_schedule_on_week: str):
        """
        Из переданной HTML выбранной недели получим список пар (дата, день_недели).

        Args:
            html_schedule_on_week (str): HTML страница, которую можно получить из
                метода self.get_url_schedule_on_week.

        Returns:
            List[(str, str)]: Список пар (дата, день_недели).
        """
        soup = BeautifulSoup(html_schedule_on_week, "html.parser")
        html_all_days = soup.findAll(class_="sc-day-header")

        # Получим список пар ('дата', 'день_недели')
        all_days = []
        for day in html_all_days:
            date, html_name_day = day.contents

            # Добавим текущий год к дате
            date = date + "." + str(dt.today().year)

            name_day = html_name_day.contents[0]
            all_days.append([date, name_day])

        return all_days

    def get_all_subjects_in_day(self, html_schedule_on_week: str, name_day: str):
        """
        Из переданной HTML для выбранного дня получим расписание.

        Args:
            html_schedule_on_week (str): HTML страница
            name_day (str): Название дня недели (например, 'Вт').

        Returns:
            Dict[Dict]: Словарь, где ключами будет время пары, а значением будет
                словарь с названием занятия, местом, типом занятия и ФИО преподователя
        """
        soup = BeautifulSoup(html_schedule_on_week, "html.parser")
        html_day = soup.find(class_="sc-day", string=name_day).find_parent().find_parent()
        html_subjects_day = html_day.findAll(class_='sc-table-row')

        dict_subjects_in_day = {}
        for html_subject in html_subjects_day:
            # Время пары
            time = html_subject.find(class_="sc-item-time").contents[0]

            # Название предмета
            title = html_subject.find(class_="sc-item-title-body").find(class_="sc-title").contents[0]

            # Тип пары
            type_subject = html_subject.find(class_="sc-item-type").contents[0]

            # Преподаватели
            lecturer = html_subject.find(class_="sc-lecturer").contents
            if html_subject.find(class_="sc-lecturer").contents == []:
                lecturer = ''
            else:
                lecturer = html_subject.find(class_="sc-lecturer").contents[0]

            # Местоположение (уберём лишние символы)
            location = html_subject.findAll(class_="sc-item-location")[1].text
            location = location.replace('\t', '').replace('\n', '')[1::]

            dict_subjects_in_day[time] = {
                "Название предмета": title,
                "Преподаватели": lecturer,
                "Местоположение": location,
                "Тип пары": type_subject,
            }
        return dict_subjects_in_day

    def get_schedule_on_week(self, html_schedule_on_week: str):
        """
        Метод для получения расписания на указанную неделю.

        Args:
            html_schedule_on_week (str): HTML страница полученная из метода
                get_url_schedule_on_week

        Returns:
            Dict: Расписание для каждого дня на недели.
        """
        all_days_on_week = self.get_all_days_on_week(html_schedule_on_week)
        # Для каждого дня получим расписание
        res = {}
        for date, name_day in all_days_on_week:
            subjects_in_day = self.get_all_subjects_in_day(html_schedule_on_week, name_day)
            res[name_day + ': ' + date] = subjects_in_day
        return res

    def get_html_on_all_weeks(self, number_group: str):
        """
        Скачиваем и сохраняем все HTML страницы с расписанием на все недели для группы.

        Returns:
            [type]: [description]
        """
        dict_number_week_html_week = {}

        # Получим количество недель для данной группы
        count_week = self.get_count_week(number_group)

        for number_week, range_week in count_week:
            url_schedule_on_week = self.get_url_schedule_on_week(number_week)
            html_schedule_on_week = get_html(url_schedule_on_week)
            dict_number_week_html_week[number_week + ": " + range_week] = html_schedule_on_week

        return dict_number_week_html_week

    def get_all_schedule_from_list_html(self, dict_number_week_html_week):
        """
        Возвращает всё расписание группы на все недели.
        """

        all_schedule_for_group = {}

        for number_week, html_schedule_on_week in dict_number_week_html_week.items():
            schedule_on_week = self.get_schedule_on_week(html_schedule_on_week)
            all_schedule_for_group[number_week] = schedule_on_week

        return all_schedule_for_group

    def get_all_schedule(self, number_group: str):
        # получим словарь {"номер недели - граница недели": html этой страницы}
        dict_number_week_html_week = self.get_html_on_all_weeks(number_group)
        return self.get_all_schedule_from_list_html(dict_number_week_html_week)
