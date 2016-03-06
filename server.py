# -*- coding: utf-8 -*-
import sys
import socket
import select
import re

class Server():
    """
    Class for handling the server side
    """
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000

    def __init__(self):
        self.server_socket = None
        self.connection_list = []

    def initialize_server_socket(self):
        """
        Initialize the server socket
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", self.PORT))
            self.server_socket.listen(10)
            self.connection_list.append(self.server_socket)
        except:
            print "Could not initialize socket"
            sys.exit()

    def send_response_message(self, sock, message):
        """
        Send the response to the client
        :param sock: Socket where the response goes
        :type sock: Socket
        :para message: The message sent from the client
        :type message: string
        """
        try:
            sock.send(message)
        except:
            # broken socket connection may be, chat client pressed ctrl+c for example
            self.remove_socket(sock)

    def remove_socket(self, sock):
        """
        Remove the socket from the connection list
        :param sock: The socket to remove
        :type sock: Socket
        """
        if sock in self.connection_list:
            sock.close()
            self.connection_list.remove(sock)

    def connect_new_client(self, sock):
        """
        Add a new client to the connection list
        :param sock: New client connected to the server_socket
        :type sock: Socket
        :return addr: The IP address from the client
        :type addr: String
        """
        # Handle the case in which there is a new connection recieved through server_socket
        sockfd, addr = self.server_socket.accept()
        self.connection_list.append(sockfd)
        print "Client (%s, %s) connected" % addr

        self.send_response_message(sockfd, "Entered room\n")
        return addr

    def handle_message_from_client(self, sock):
        """
        Send the message back to the client.
        If it is not possible disconnect the client by removing it from the connection list
        :param sock: Client the server send the message back
        :type sock: Socket
        """
        try:
            data = self.__recvall(sock)
            if data:
                self.send_response_message(sock, data)
        except:
            self.send_response_message(sock, "Client is offline")
            self.remove_socket(sock)

    def __recvall(self, sock):
        """
        Keep receiving all data from client until it's done or the client disconnects.
        :param sock: The client socket who sends the data
        :type sock: Socket
        """
        total_data=[]
        keep_reading_data = True
        while keep_reading_data:
            data = sock.recv(self.RECV_BUFFER)
            if not data:
                    break
            elif re.search("\n", data):
                keep_reading_data = False
            total_data.append(data)
        return ''.join(total_data)


    def run_server(self):
        """
        Keep running the server, listening to new connections from clients
        and/or sending them the messages.
        """
        while 1:
            # Get the list of sockets which are ready to be read through select
            read_sockets,write_sockets,error_sockets = select.select(self.connection_list, [], [])

            for sock in read_sockets:
                # New connection
                if sock == self.server_socket:
                    self.connect_new_client(sock)
                # Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    self.handle_message_from_client(sock)

        self.server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.initialize_server_socket()

    print "Chat server started on port " + str(server.PORT)

    server.run_server()
