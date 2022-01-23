from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<ControlPanel>:
    orientation: "vertical"
    GridLayout:
        cols: 5
        rows: 4
        spacing:10
    
    
        Label:
    
        MDIconButton:
            icon: "arrow-up"
            on_release: root.printer.move_back()
    
        Label:
    
        MDIconButton:
            icon: "arrow-up"
            on_release: root.printer.move_up()
    
        MDFillRoundFlatIconButton:
            icon: "home"
            text: "XYZ"
            on_release: root.printer.home_all()
    
        MDIconButton:
            icon: "arrow-left"
            on_release: root.printer.move_left()
    
        MDFillRoundFlatIconButton:
            icon: "home"
            text: "XY"
            on_release: root.printer.home_xy()
    
        MDIconButton:
            icon: "arrow-right"
            on_release: root.printer.move_right()
    
        MDFillRoundFlatIconButton:
            icon: "home"
            text: "Z"
            on_release: root.printer.home_z()
    
        MDFillRoundFlatIconButton:
            icon: "home"
            text: "X"
            on_release: root.printer.home_x()
    
        Label:
    
        MDIconButton:
            icon: "arrow-down"
            on_release: root.printer.move_front()
    
        Label:
    
        MDIconButton:
            icon: "arrow-down"
            on_release: root.printer.move_down()
    
        MDFillRoundFlatIconButton:
            icon: "home"
            text: "Y"
            on_release: root.printer.home_y()
            
    Widget:

''')


class ControlPanel(BoxLayout):
    printer = ObjectProperty()
