# Tcp Chat server
 
import socket, select

RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 5000

class Server():
    """
    Class for handle the server side
    """
    def __init__(self):
        self.server_socket = None
        self.connection_list = []

    def initialize_server_socket(self):
        """
        Initialize the server socket
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this has no effect, why ?
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", PORT))
        self.server_socket.listen(10)

    def message_response (self, sock, message):
        """
        Send the response to the client
        :param sock: Socket where the response goes
        :type sock: Socket
        :para message: The message sent from the client
        :type message: string
        """
        #Do not send the message to master socket and the client who has send us the message
        try :
            sock.send(message)
        except :
            # broken socket connection may be, chat client pressed ctrl+c for example
            sock.close()
            print "Connection removed"
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
         
        self.message_response(sockfd, "[%s:%s] entered room\n" % addr)
        return addr

    def handle_message_from_client(self, sock, addr):
        """
        Send the message back to the client.
        If it is not possible disconnect the client by removing it from the connection list
        :param sock: Client the server send the message back
        :type sock: Socket
        """
        try:
            data = sock.recv(RECV_BUFFER)
            if data:
                self.message_response(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)      
        except:
            self.message_response(sock, "Client (%s, %s) is offline" % addr)
            print "Client (%s, %s) is offline" % addr
            sock.close()
            self.connection_list.remove(sock) 
 
if __name__ == "__main__":
    server = Server()
    server.initialize_server_socket()
 
    # Add server socket to the list of readable connections
    server.connection_list.append(server.server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(server.connection_list, [], [])
 
        for sock in read_sockets:
            #New connection
            if sock == server.server_socket:
                addr = server.connect_new_client(sock)
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                server.handle_message_from_client(sock, addr)
     
    server.server_socket.close()