# telnet program example
import socket, select, string, sys

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

class Client(object):
    """
    Class for handle the Client side
    """

    def __init__(self, host=None, port=None):
        """
        Constructor of Client

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
        except :
            print 'Unable to connect'
            sys.exit()
        print 'Connected to remote host. Start sending messages'
        prompt()

    def ready(self):
        """
        Execute the core of functionality it check if the client must send or recieve data
        """

        # list of the sockect avaliables
        socket_list = [sys.stdin, self.socket]

        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            # if is the same socket it's mean it must read
            if sock == self.socket:
                data = self.recieve_data()
                sys.stdout.write(data)
                prompt()
            else:  # in other case, writte
                msg = sys.stdin.readline()
                self.send_data(msg)

    def recieve_data(self):
        """
        Read the data for  the socket  and print it
        """
        data = self.socket.recv(4096)
        if not data :
            print '\nDisconnected from chat server'
            sys.exit()
        else :
            print('data received {}'.format(data))
            return data


    def send_data(self, data=None):
        """
        The User wirtte data and send it to the server
        """
        self.socket.send(data)
        prompt()

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    client = Client(host, port)

    client.connect()


    while 1:
        client.ready()
