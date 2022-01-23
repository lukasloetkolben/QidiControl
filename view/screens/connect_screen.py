from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

from model.qidi_printer import QidiPrinter
from model.utils import search_printer

Builder.load_string('''
<ConnectScreen>:
    MDFloatLayout:
        MDLabel:
            text: "Printer"
            font_style: "H4"
            halign: "center"
            pos_hint:{'center_x':.5,'center_y':.8}
        
        MDBoxLayout:
            orientation: "horizontal"
            pos_hint: {'center_x':0.5, 'center_y':.5}
            size_hint: (0.5, 0.1)
            MDTextField:
                id: printer_ip_field
                size_hint: (0.5, None)
                hint_text: "Printers ip"
                helper_text: "Input ip of your printer."
                helper_text_mode: "on_focus"
                on_text: root.ip_changed()
            
            MDIconButton:
                icon: "cloud-search"
                on_release: root.refresh_clicked()
    
        MDFillRoundFlatIconButton:
            id: connect_button
            pos_hint:{'center_x':.5,'center_y':.3}
            text: "connect"
            icon: "connection"      
            on_release: root.connect_clicked()
''')


class ConnectScreen(MDScreen):
    printer = QidiPrinter()

    def on_pre_enter(self):
        print("projects pre_enter")

    def goto_main_screen(self):
        self.manager.transition.direction = "down"
        self.manager.current = "main_screen"

    def refresh_clicked(self):
        ip = search_printer()
        if ip is not None:
            self.ids.printer_ip_field.text = ip
            self.connect_clicked()

    def connect_clicked(self):

        if self.printer.connect(self.ids.printer_ip_field.text):
            toast("Printer connected!")
            self.ids.connect_button.disabled = True
            self.manager.get_screen("main_screen").printer = self.printer
            self.goto_main_screen()
        else:
            toast("Printer connection failed!")
            self.ids.connect_button.disabled = False

    def ip_changed(self):
        self.ids.connect_button.disabled = False
