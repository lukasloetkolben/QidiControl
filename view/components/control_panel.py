from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

Builder.load_string('''
<ControlPanel>:
    cols: 5
    rows: 3
    spacing:20
    row_default_height: 80
    row_default_width: 80
    row_force_default: True
    col_default_height: 80
    col_default_width: 80
    col_force_default: True

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

''')


class ControlPanel(GridLayout):
    printer = ObjectProperty()
