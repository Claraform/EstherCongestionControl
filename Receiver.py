"""
ESTHER CONGESTION CONTROL RECEIVER

Receivers listen for ECC packets, and, of needed, replies with a speed up or slow down message.


Ty to https://raw.githubusercontent.com/ninedraft/python-udp/master/client.py
"""

import socket
from datetime import datetime, timedelta
from random import randint
from time import sleep


class Receiver:

    def __init__(self):
        LINESPEED = 100000  # In Mbps
        PACKETSIZE = 65535  # In bytes

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Enable broadcasting mode
        self.client.bind(("", 37020))
        self.next_expected = None
        self.threshold = PACKETSIZE/LINESPEED # Some acceptible delay threshold in seconds, which can cater for TX time

    def listen(self):
        data, addr = self.client.recvfrom(1024)
        rightnow = datetime.now()
        print("received message:{}".format(data.decode("UTF-8")))
        decoded = data.decode('UTF-8')

        send_time = decoded[decoded.find('=')+1: decoded.find(',')]
        period = float(decoded[decoded.find('d=')+2:])
        newperiod = period
        #print(period)

        if self.next_expected is not None:
            print("Expected timestamp at {}".format(self.next_expected))
            print("Received timestamp at {}".format(rightnow))
            if rightnow > (self.next_expected+timedelta(seconds=self.threshold)):
                print("Timestamp arrived late!")
                print("Difference is {} ".format((rightnow - self.next_expected).total_seconds()))
                # TODO: Send response to server to tell em to slow down
                newperiod = period * 1.1
                print("Setting period to", newperiod)
                #message = b'slow'
                #self.client.sendto(newperiod, addr)
            else:
                print("Timestamp arrived early or on time!")
                print("Difference is {} ".format((self.next_expected-rightnow).total_seconds()))
                # TODO: Send response to server to tell em to speed up
                #message = b'fast'
                newperiod = period * 0.9
                print("Setting period to", newperiod)
        
        message = str(newperiod).encode('utf_8')
        self.client.sendto(message, addr)
        self.next_expected = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=float(period))
        print("----------------------------")
        #Fake some delay time
        sleep(randint(1,8)*0.1)




rec = Receiver()
while True:
    rec.listen()

