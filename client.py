# -*- coding: utf-8 -*-
import sys
import re
import socket 
import select
import string

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

class Client(object):
    """
    Class for handling the Client side
    """

    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    
    def __init__(self, host=None, port=None):
        """
        Initialize the client

        :param host: ip of he Server
        :type user: string
        :param port: port of he Server
        :type user: integer
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)

    def connect(self, host=None, port=None):
        """
        Connect to Server if the host or port is None use their own

        :param host: ip of he Server
        :type host: String
        :param port: port of he Server
        :type port: Integer
        """

        self.host = host if host else self.host
        self.port = port if port else self.port

        try:
            self.socket.connect((self.host, self.port))
        except:
            print 'Unable to connect'
            sys.exit()
        print 'Connected to remote host. Start sending messages'

    def ready(self):
        """
        Execute the core functionality. Send or receive the message to/from the server
        """
        while 1:
            # list of the available sockets
            socket_list = [sys.stdin, self.socket]

            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                # if is the same socket it's mean it must read
                if sock == self.socket:
                    data = self.receive_data()

                    sys.stdout.write("<server response> " + data)
                    prompt()
                else:  # in other case, write
                    msg = sys.stdin.readline()
                    self.send_data(msg)

    def receive_data(self):
        """
        Read the data from the socket and print it
        :return data: Data sent by server
        :type data: String
        """
        #data = self.socket.recv(self.RECV_BUFFER)
        data = self.__recvall()
        if not data:
            print '\nDisconnected from chat server'
            sys.exit()
        else:
            return data

    def __recvall(self):
        """
        Keep receiving all data from the server until it's done.
        """
        total_data=[]
        keep_reading_data = True
        while keep_reading_data:
            data = self.socket.recv(self.RECV_BUFFER)
            if not data:
                    break
            elif re.search("\n", data):
                keep_reading_data = False
            total_data.append(data)
        return ''.join(total_data)

    def send_data(self, data=None):
        """
        Send the data to the server
        :param data: The data to send to the server
        :type data: String
        """
        self.socket.send(data)

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    client = Client(host, port)

    client.connect()
    client.ready()
