class ISchedule:
    def update_schedule(self):
        raise NotImplementedError("Виртуальный метод не переопределён")

    def get_schedule_for_group(self, url_group):
        raise NotImplementedError("Виртуальный метод не переопределён")
