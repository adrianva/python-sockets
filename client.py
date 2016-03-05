# telnet program example
import socket, select, string, sys

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

class Client(object):

    def __init__(self, host , port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except :
            print 'Unable to connect'
            sys.exit()
        print 'Connected to remote host. Start sending messages'
        prompt()

    def ready(self):
        socket_list = [sys.stdin, self.socket]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                self.recieve_data()
            #user entered a message
            else :
               self.send_data()

    def recieve_data(self):
        data = sock.recv(4096)
        if not data :
            print '\nDisconnected from chat server'
            sys.exit()
        else :
            #print data
            sys.stdout.write(data)
            prompt()

    def send_data(self):
        msg = sys.stdin.readline()
        self.socket.send(msg)
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
