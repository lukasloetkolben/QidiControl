from socket import *


def search_printer():
    pc_ip = gethostbyname(gethostname())
    timeout = 0

    while True:
        timeout += 0.02
        if timeout >= 0.5:
            timeout = 0.02

        for i in range(0, 255):
            printer_ip = pc_ip[:pc_ip.rfind('.') + 1] + str(i)

            s = socket(AF_INET, SOCK_DGRAM)
            s.settimeout(timeout)
            try:
                s.sendto("M4001".encode('utf-8', 'ignore'), (printer_ip, 3000))
                data, address = s.recvfrom(1280)
                if all(x in data.decode('utf-8') for x in ["X","Y","Z","E"]):
                    return printer_ip
            except Exception:
                continue
