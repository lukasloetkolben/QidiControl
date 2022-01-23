import os
import platform
import socket
import struct
import subprocess
from pathlib import Path
from socket import *
from typing import cast

import config

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class QidiPrinter():

    def __init__(self):
        self.ip = ""
        self.port = 3000
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.socket.setblocking(1)
        self.socket.settimeout(5)

        self.temp_gcode = Path(BASE, "temp.gcode")
        self.file_encoding = 'utf-8'

        if platform.system() == 'Windows':
            self.vc_compress = config.GCODE_COMPRESSOR_WIN
        elif platform.system() == 'Darwin':
            self.vc_compress = config.GCODE_COMPRESSOR_MAC
        else:
            raise Exception('Operation System not supported!')

        self.config = {}

    def connect(self, ip):
        try:
            self.ip = ip
            self.config = self.init_printer_config()
            return True
        except Exception:
            return False


    def socket_send(self, cmd, t=5):
        self.socket.settimeout(t)
        print(cmd)
        new_command = cast(str, cmd).encode(self.file_encoding, 'ignore') if type(cmd) is str else cast(bytes, cmd)
        self.socket.sendto(new_command, (self.ip, self.port))
        data, address = self.socket.recvfrom(1280)
        self.socket.settimeout(5)
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

    def is_available(self, t=5):
        return "x_mm_step" in self.socket_send("M4001", t=t)

    def add_check_sum(self, data, seekPos):
        seek_array = struct.pack('>I', seekPos)

        check_sum = 0
        data += b"000000"
        data_array = bytearray(data)
        data_size = len(data_array) - 6

        if data_size <= 0:
            return

        data_array[data_size] = seek_array[3]
        data_array[data_size + 1] = seek_array[2]
        data_array[data_size + 2] = seek_array[1]
        data_array[data_size + 3] = seek_array[0]

        for i in range(0, data_size + 4, 1):
            check_sum ^= data_array[i]

        data_array[data_size + 4] = check_sum
        data_array[data_size + 5] = 0x83

        return data_array

    def send_file_chunk(self, buff, seekPos):
        temp = bytearray(buff)
        temp_size = len(temp)
        if temp_size <= 0:
            return

        data = self.add_check_sum(buff, seekPos)
        data_size = len(data) - 6

        if data_size <= 0:
            raise Exception("File Size is empty!")

        return self.socket_send(data)

    def write_file_start(self, gcode_path):
        return self.socket_send(f'M28 {Path(gcode_path).name}')

    def write_file(self, gcode_path):
        with open(Path(config.GCODE_TEMP_PATH, Path(gcode_path).name + ".tz"), 'rb') as fp:
            while True:
                seekPos = fp.tell()
                chunk = fp.read(1280)
                if not chunk:
                    break
                self.send_file_chunk(chunk, seekPos)

        fp.close()

    def write_file_end(self, gcode_path):
        return self.socket_send(f"M29 {Path(gcode_path).name}")

    def upload_gcode(self, gcode_path, start_print=False):
        self.compress_gcode(gcode_path)
        self.write_file_start(gcode_path)
        self.write_file(gcode_path)
        self.write_file_end(gcode_path)
        if start_print:
            self.start_print(Path(gcode_path).name)

    def get_current_position(self):
        return self.socket_send('M114')

    def get_firmware_info(self):
        return self.socket_send('M115')

    def printer_shutdown(self):
        self.socket_send('M4003')

    def printer_light_off(self):
        self.socket_send('M107 T-3')

    def printer_light_on(self):
        self.socket_send('M106 S255 T-3')

    def printer_emergency_stop(self):
        self.socket_send('M112')

    def start_print(self, gcode):
        self.socket_send(f'M6030 ":{gcode}" I1')

    def pause_print(self):
        self.socket_send("M25")

    def resume_print(self):
        self.socket_send("M24")

    def cancel_print(self):
        self.socket_send("M33")

    def home_all(self):
        self.socket_send("G28", t=60)

    def home_x(self):
        self.socket_send("G28 X", t=60)

    def home_y(self):
        self.socket_send("G28 Y", t=60)

    def home_z(self):
        self.socket_send("G28 Z", t=60)

    def home_xy(self):
        self.socket_send("G28 X Y", t=60)

    def move_left(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 X{-1 * amount} F{speed}", t=60)

    def move_right(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 X{amount} F{speed}", t=60)

    def move_back(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 Y{amount} F{speed}", t=60)

    def move_front(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 Y{-1 * amount} F{speed}", t=60)

    def move_up(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 Z{amount} F{speed}", t=60)

    def move_down(self, amount=10, speed=1500):
        self.set_relative_positioning()
        self.socket_send(f"G0 Z{-1 * amount} F{speed}", t=60)

    def set_relative_positioning(self):
        self.socket_send("G91")

    def send_gcode_command(self, command):
        return self.socket_send(command, t=None)

    def compress_gcode(self, gcode_path):
        cfg = self.config
        cmd = f'"{os.path.normpath(self.vc_compress)}" "{gcode_path}" {cfg["x_mm_step"]} ' \
              f'{cfg["y_mm_step"]} {cfg["z_mm_step"]} {cfg["e_mm_step"]} {config.GCODE_TEMP_PATH} ' \
              f'{cfg["s_x_max"]} {cfg["s_y_max"]} {cfg["s_z_max"]} {cfg["s_machine_type"]}'
        print(cmd)
        _ = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        return os.path.exists(f"{self.temp_gcode}.tz")
