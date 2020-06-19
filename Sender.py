"""
TCP ESTHER SENDER

TCP Esther Senders periodically broadcast packets over a network. It also listens for replies from receivers indicate a
"speed up" or "slow down" message.
The rate at which the Sender transmits these packets is adjusted according to responses from Receivers.


Ty to https://raw.githubusercontent.com/ninedraft/python-udp/master/server.py
"""

import socket
import time
from datetime import datetime


class Sender:
    def __init__(self):
        self.period = 0.2
        self.port = 37020
        self.last_transmission_time = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # Enable reuse
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcasting mode
        self.server.settimeout(100)

    def send(self):
        TS = datetime.now()
        TS = TS.strftime("%Y-%m-%d %H:%M:%S.%f")
        message = bytes("Current_time={}, Period={}".format(TS, self.period), "UTF-8")
        self.server.sendto(message, ("<broadcast>", self.port))
        time.sleep(self.period)
        print(message)
        s.ack()

    def ack(self):
      ack = self.server.recv(4096)
      p = ack.decode('UTF-8')
      #print(p)
      self.period = float(p)

    def close(self):
        self.server.close()


if __name__ == "__main__":
    # Instantiate a sender class
    s = Sender()
    for i in range(100):
        s.send()
    s.close()
