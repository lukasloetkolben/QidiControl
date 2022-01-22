import os
import socket
import subprocess
from pathlib import Path
from typing import cast
import platform



BASE =  os.path.join(os.path.dirname(os.path.abspath(__file__)))

class QidiPrinter():

    def __init__(self, ip):
        self.ip = ip
        self.port = 3000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.temp_gcode = Path(BASE, "temp.gcode")
        self.file_encoding = 'utf-8'

        if platform.system() == 'Windows':
            self.vc_compressh = Path(BASE, 'VC_compress_gcode.exe')
        elif platform.system() == 'Darwin':
            self.vc_compressh = Path(BASE, 'VC_compress_gcode_MAC')
        else:
            raise Exception('Operation System not supported!')

        self.config = self.init_printer_config()

    def socket_send(self, cmd):
        new_command = cast(str, cmd).encode(self.file_encoding, 'ignore') if type(cmd) is str else cast(bytes, cmd)
        self.socket.sendto(new_command, (self.ip, self.port))
        data, address = self.socket.recvfrom(4096)
        return data.decode('utf-8')

    def init_printer_config(self):
        msg = self.socket_send("M4001")
        msg = msg.rstrip()
        msgs = msg.split(' ')
        config = {}
        for item in msgs:
            _ = item.split(':')
            if len(_) == 2:
                id = _[0]
                value = _[1]
                if id == 'X':
                    config["x_mm_step"] = value
                elif id == 'Y':
                    config["y_mm_step"] = value
                elif id == 'Z':
                    config["z_mm_step"] = value
                elif id == 'E':
                    config["e_mm_step"] = value
                elif id == 'T':
                    _ = value.split('/')
                    if len(_) == 5:
                        config["s_machine_type"] = _[0]
                        config["s_x_max"] = _[1]
                        config["s_y_max"] = _[2]
                        config["s_z_max"] = _[3]
                elif id == 'U':
                    self.file_encoding = value.replace("'", '')
        return config

    def get_print_progress(self):
        return self.socket_send('M27')

    def pause_print(self):
        self.socket_send("M25")

    def resume_print(self):
        self.socket_send("M24")

    def cancel_print(self):
        self.socket_send("M33")

    def home_printer(self):
        self.socket_send("G28")

    def compress_gcode(self, gcode_path):
        config = self.config
        cmd = f'"{os.path.normpath(self.vc_compressh)}" "{gcode_path}" {config["x_mm_step"]} ' \
              f'{config["y_mm_step"]} {config["z_mm_step"]} {config["e_mm_step"]} "." {config["s_x_max"]}' \
              f' {config["s_y_max"]} {config["s_z_max"]} {config["s_machine_type"]}'
        _ = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        return os.path.exists(f"{self.temp_gcode}.tz")

