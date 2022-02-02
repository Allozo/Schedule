from bs4 import BeautifulSoup
from schedule.ISchedule import ISchedule
import requests


dict_mai_url = {
    "url_all_groups": "https://mai.ru/education/schedule/",
    "url_week": "https://mai.ru/education/schedule/detail.php?group={number_group}&week={number_week}",
}


def get_html(url: str):
    """
    По переданному url получаем html.
    Если код ответа не 200, то вернём ошибку.
    """
    page = requests.get(url)

    assert (
        page.status_code == 200
    ), f"Не удалось получить страницу. Код ошибки: {page.status_code}"

    return page.text


def save_html(html_page: str):
    """
    Сохраняет html страницы в файл.
    """
    with open("test\\dir_html\\all_groups.html", "w", encoding="utf-8") as file:
        file.write(html_page)


def load_html(path: str) -> str:
    data = None
    with open(f"{path}", "r", encoding="utf-8") as file:
        data = file.read()
    return data


class MAISchedule(ISchedule):
    def __init__(self) -> None:
        super().__init__()
        self._number_group = "М3О-326Б-19"

    def get_url_all_groups(self):
        """
        Возвращает ссылка на страницу, где указаны все группы
        """
        return dict_mai_url["url_all_groups"]

    def get_url_schedule_on_week(self, number_week: int):

        return (
            dict_mai_url["url_week"]
            .replace("{number_group}", str(self.number_group))
            .replace("{number_week}", str(number_week))
        )

    @property
    def number_group(self):
        """
        Свойство для получения номера группы
        """
        return self._number_group

    def __get_courses(self, html_page_all_groups: str) -> list:
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

    def __get_institute(self, html_page_all_groups: str, course: str) -> list:
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

    def __get_field(
        self, html_page_all_groups: str, course: str, institute: str
    ) -> list:
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

        html_course = soup.find(class_="sc-container-header", string=course)
        html_institute = (
            html_course.find_parent()
            .find("a", class_="sc-table-col", string=institute)
            .find_parent()
        )
        html_fields = html_institute.findAll(class_="sc-program")

        fields = [field.text for field in html_fields]

        return fields

    def __get_group(
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

        html_course = soup.find(class_="sc-container-header", string=course)
        html_institute = (
            html_course.find_parent()
            .find("a", class_="sc-table-col", string=institute)
            .find_parent()
        )
        html_field = html_institute.find(
            class_="sc-program", string=field
        ).find_parent()
        html_groups = html_field.findAll(class_="sc-group-item")

        list_groups = [group.text for group in html_groups]

        return list_groups

    def select_group(self):
        """
        Метод для выбора номера группы.
        """
        html_page_all_group = get_html(self.get_url_all_groups())

        # Получим список курсов
        list_courses = self.__get_courses(html_page_all_group)
        print(list_courses)

        # Выберем курс
        course = list_courses[2]

        # Получим список институтов
        list_institute = self.__get_institute(html_page_all_group, course)
        print(list_institute)

        # Выбираем институт
        institute = list_institute[2]

        # Получим список направлений подготовки
        list_fields = self.__get_field(html_page_all_group, course, institute)
        print(list_fields)

        # Выбираем направление
        field = list_fields[1]

        # Получим список групп
        list_group = self.__get_group(html_page_all_group, course, institute, field)
        print(list_group)

        print("\n")

        return

    def update_schedule(self):
        """
        Метод для обновления расписания.
        """
        pass

    def get_schedule_on_week(self, number_week):
        """
        Метод для получения расписания на указанную неделю.

        number_week {int} - Номер недели для которой будем возвращать
            расписание.
        """
        pass

    def get_schedule_on_day(self, data):
        """
        Метод для получения расписания на указанный день.

        data {str} - Дата для которой будем возвращать расписание.
        """
        pass

    def get_all_schedule(self):
        """
        Возвращает всё расписание группы.
        """
        pass


if __name__ == "__main__":
    print("\n")
    m = MAISchedule()
    tmp = m.select_group()
    print(tmp)
