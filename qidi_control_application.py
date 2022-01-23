import json

from kivy.factory import Factory
from kivymd.app import MDApp

from screen_manger import QidiControlScreenManger

r = Factory.register

with open("factory_registers.json") as fd:
    custom_widgets = json.load(fd)
    for module, _classes in custom_widgets.items():
        for _class in _classes:
            r(_class, module=module)


class QidiControlApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        return QidiControlScreenManger()


if __name__ == '__main__':
    QidiControlApp().run()
