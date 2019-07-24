import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        IP = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack(b'256s', bytes(ifname[:15].encode('utf-8')))
        )[20:24])
    except OSError:
        IP = None
    return IP

# print(get_ip_address('wlan0'))