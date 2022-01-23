from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from model.qidi_printer import QidiPrinter
from model.utils import search_printer
from plyer import filechooser
from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser

Builder.load_string('''
<MainScreen>    
    MDFloatLayout:

        ControlPanel:
            id: control_panel
            pos_hint: {'left':0.1, 'top':1}

        MDRaisedButton:
            size_hint: (0.5, None)
            pos_hint: {'right':1, 'bottom': 0}
            text: "Upload"
            on_release: root.upload_file_btn_clicked()
    ''')

# Button:
# text: "Upload File"
# on_release: root.upload_file_btn_clicked()

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.printer = None


    def on_pre_enter(self):
        self.ids.control_panel.printer = self.printer


    def upload_file_btn_clicked(self):
        raw_path = filechooser.open_file(title="Carica il file tempi in formato .xlsx",
                                         filters=[("Gcode", "*.gcode")])
        self.printer.upload_gcode(raw_path[0], start_print=True)


    def goto_main_screen(self):
        self.manager.transition.direction = "down"
        self.manager.current = "main_screen"
