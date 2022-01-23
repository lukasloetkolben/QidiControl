from threading import Thread

from kivy.lang import Builder
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
            pos_hint:{'center_y':.8}
        
        MDBoxLayout:
            orientation: "horizontal"
            pos_hint: {'center_x':0.5, 'center_y':.5}
            size_hint: (0.5, 0.1)
            spacing: 10
            
            MDTextField:
                id: printer_ip_field
                size_hint: (0.5, None)
                hint_text: "IP address"
                helper_text: "Enter ip of your printer."
                helper_text_mode: "on_focus"
            
            MDIconButton:
                id: search_printer_ip_button
                icon: "cloud-search"
                on_release: root.search_printer_ip()
            
            MDSpinner:
                id: spinner
                size_hint: None, None
                pos_hint:{'center_y':.44}
                padding: 5
                size: dp(20), dp(20)
                active: False
           
        MDFillRoundFlatIconButton:
            id: connect_button
            pos_hint:{'center_x':.5,'center_y':.3}
            text: "Connect"
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

    def search_printer_ip(self):
        t = Thread(target=search_printer, args=(self,))
        t.start()
        self.ids.search_printer_ip_button.disabled = True
        self.ids.printer_ip_field.disabled = True
        self.ids.connect_button.disabled = True
        self.ids.spinner.active = True

    def printer_ip_found(self, ip):
        self.ids.spinner.active = False
        self.ids.search_printer_ip_button.disabled = False
        self.ids.connect_button.disabled = False
        self.ids.printer_ip_field.text = ip
        self.connect_clicked()

    def printer_ip_not_found(self):
        toast("Could not find printer!")
        self.ids.printer_ip_field.disabled = False
        self.ids.search_printer_ip_button.disabled = False
        self.ids.connect_button.disabled = False
        self.ids.spinner.active = False

    def connect_clicked(self):

        if self.printer.connect(self.ids.printer_ip_field.text):
            toast("Printer connected!")
            self.manager.get_screen("main_screen").printer = self.printer
            self.goto_main_screen()
        else:
            toast("Printer connection failed!")
