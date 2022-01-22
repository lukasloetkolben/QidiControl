import os
import socket
import struct
import subprocess
import time
from pathlib import Path
from typing import cast
import platform
from socket import *

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class QidiPrinter():

    def __init__(self, ip):
        self.ip = ip
        self.port = 3000
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.socket.setblocking(1) # note: experimental, default is 1
        self.socket.settimeout(5)

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
        print(new_command)
        self.socket.sendto(new_command, (self.ip, self.port))
        data, address = self.socket.recvfrom(1280)
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
        with open(gcode_path + ".tz", 'rb') as fp:
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

    def get_print_progress(self):
        return self.socket_send('M27')

    def start_print(self, gcode):
        self.socket_send(f'M6030 ":{gcode}" I1')

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
              f'{config["y_mm_step"]} {config["z_mm_step"]} {config["e_mm_step"]} {BASE} {config["s_x_max"]}' \
              f' {config["s_y_max"]} {config["s_z_max"]} {config["s_machine_type"]}'
        print(cmd)
        _ = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        return os.path.exists(f"{self.temp_gcode}.tz")
