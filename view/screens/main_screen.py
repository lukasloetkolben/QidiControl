from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from plyer import filechooser

Builder.load_string('''
<MainScreen>    
    GridLayout:
        cols:2
        rows: 2
        size_hint: (1, 0.6)
        pos_hint: {'top':0.99}
        spacing: 50
        AnchorLayout:          
            anchor_x: 'left'
            anchor_y: 'top'
            size_hint: (0.5, 0.5)

            ControlPanel:
                id: control_panel
                
        AnchorLayout:          
            anchor_x: 'right'
            anchor_y: 'top'
            size_hint: (0.5, 0.5)
  
            GcodeTerminal:
                id: gcode_terminal
        
    MDFloatLayout:        
        MDFillRoundFlatIconButton:
            icon: "power"
            text: "Shutdown"
            pos_hint: {'left':0.99}
            on_release: root.printer.printer_shutdown()
        
        MDFloatingActionButton:
            pos_hint: {'right':0.99, 'top':0.99}
            icon: "power-cycle"
            md_bg_color: app.theme_cls.error_color
            root_button_anim: True
            on_release: root.printer.printer_emergency_stop()
        
        MDFloatingActionButton:
            pos_hint: {'right':0.99}
            icon: "file-upload"
            root_button_anim: True
            on_release: root.upload_file_btn_clicked()
                  
    ''')



class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.printer = None

    def on_pre_enter(self):
        self.printer.main_screen = self
        self.ids.control_panel.printer = self.printer
        self.ids.gcode_terminal.printer = self.printer

    def upload_file_btn_clicked(self):
        raw_path = filechooser.open_file(title="Carica il file tempi in formato .xlsx",
                                         filters=[("Gcode", "*.gcode")])
        if raw_path:
            self.printer.upload_gcode(raw_path[0], start_print=True)

    def goto_main_screen(self):
        self.manager.transition.direction = "down"
        self.manager.current = "main_screen"

    def add_terminal_message(self, message):
        self.ids.gcode_terminal.add_message(message)

