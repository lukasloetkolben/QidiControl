import json

from kivy.clock import Clock
from kivy.factory import Factory  # NOQA: F401
from kivy.uix.screenmanager import ScreenManager


class QidiControlScreenManger(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_screens)

    def add_screens(self, interval):
        with open("screens.json") as f:
            screens = json.load(f)
            for import_screen, screen_details in screens.items():
                exec(import_screen)
                screen_object = eval(screen_details["factory"])
                screen_object.name = screen_details["screen_name"]
                self.add_widget(screen_object)
