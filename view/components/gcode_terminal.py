from kivy.lang import Builder

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.list import OneLineListItem

Builder.load_string('''
<GcodeTerminal>:
    orientation: "vertical"
    ScrollView:
        id: scroll_view
        size_hint: (1,1)
        canvas.before:
        Color:
            rgba: app.theme_cls.bg_dark
        Rectangle:
            pos: self.pos
            size: self.size
        MDList:
            id: gcode_list
            pos_hint: {'top':1}
    
    BoxLayout:
        orientation: "horizontal"
        pos_hint: {'bottom':0.99}
        size_hint: (1, 0.2)
        MDTextField:
            id: gcode_input
            hint_text: "GCode"
            multiline: False
            on_text_validate: root.send_gcode()
    
        MDIconButton:
            icon: "send"
            on_release: root.send_gcode()
''')

class GcodeTerminal(BoxLayout):
    printer = ObjectProperty()

    def append_gcode_list(self, gcode):
        self.ids.gcode_list.add_widget(
                OneLineListItem(
                    text=f"> {gcode}"
                )
        )

    def send_gcode(self):
        text = self.ids.gcode_input.text.strip()
        if text:
            self.printer.send_gcode_command(text)  #
            self.ids.gcode_input.text = ""
            self.append_gcode_list(text)

    def add_message(self, message):
        message = f"[size=12]# {message}[/size]"
        self.ids.gcode_list.add_widget(
            OneLineListItem(
                text=message,
            )
        )
        self.ids.scroll_view.scroll_y = 0

