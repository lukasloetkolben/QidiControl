from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from model.qidi_printer import QidiPrinter
from model.utils import search_printer

Builder.load_string('''
<MainScreen>    
    ControlPanel:
        id: control_panel

        
    ''')

# Button:
# text: "Upload File"
# on_release: root.upload_file_btn_clicked()

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.printer = QidiPrinter(search_printer())

        self.ids.control_panel.printer = self.printer

    def on_pre_enter(self):
        print("MainScreen entered!")


    def upload_file_btn_clicked(self):
        print("upload file")


    def goto_main_screen(self):
        self.manager.transition.direction = "down"
        self.manager.current = "main_screen"
