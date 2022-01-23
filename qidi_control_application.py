import json

from kivy.app import App
from kivy.factory import Factory
from kivymd.app import MDApp

from view.screens.main_screen import MainScreen

r = Factory.register

with open("factory_registers.json") as fd:
    custom_widgets = json.load(fd)
    for module, _classes in custom_widgets.items():
        for _class in _classes:
            r(_class, module=module)

class QidiControlApp(MDApp):

    def build(self):
        return MainScreen()





if __name__ == '__main__':
    QidiControlApp().run()