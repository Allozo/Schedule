from abc import ABC, abstractmethod

class ISchedule(ABC):
    @abstractmethod
    def select_group(self):
        """
        Метод для выбора номера группы.
        """
        pass

    @abstractmethod
    def update_schedule(self):
        """
        Метод для обновления расписания.
        """
        pass

    @abstractmethod
    def get_schedule_on_week(self, number_week):
        """
        Метод для получения расписания на указанную неделю.

        number_week {int} - Номер недели для которой будем возвращать расписание
        """
        pass

    @abstractmethod
    def get_schedule_on_day(self, data):
        """
        Метод для получения расписания на указанный день.

        data {str} - Дата для которой будем возвращать расписание
        """
        pass
