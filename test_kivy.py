from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button


class MainApp(App):
    def build(self):
        pl = PageLayout()
        l1 = Button(text='text1', size=[100, 100])
        pl.add_widget(l1)
        pl.add_widget(Button(text='text2'))
        pl.add_widget(Button(text='text3'))
        pl.border = 10
        return pl


if __name__ == '__main__':
    app = MainApp()
    app.run()
