# -*- coding: utf-8 -*-
import unittest
import string
import random
from client import Client

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client("localhost", 5000)

    def test_same_socket_init_connect(self):
        print "testing connection to server..."
        client_aux = Client()
        client_aux.connect('localhost', 5000)

        self.assertEqual(self.client.host, client_aux.host)
        self.assertEqual(self.client.port, client_aux.port)

    def test_send_short_message_to_server(self):
        print "testing short messages delivery...\n"
        client = Client("localhost", 5000)
        client.connect()
        
        response = client.receive_data()
        self.assertEqual(response, 'Entered room\n')
        
        message = "Testing some messaging\n"
        client.send_data(message)
        response = client.receive_data()
        self.assertEqual(response, message)

    def test_send_long_message_to_server(self):
        # Generate some random text larger than 4096 bytes
        characters = (string.ascii_uppercase +
                      string.digits + ' ')
        message = ''.join(random.choice(characters) for x in range(6000))
        message += "\n"

        client = Client("localhost", 5000)
        client.connect()
                
        response = client.receive_data()
        self.assertEqual(response, 'Entered room\n')
        
        client.send_data(message)
        response = client.receive_data()
        self.assertEqual(response, message)

    def test_connect_two_clients(self):
        client_1 = Client("localhost", 5000)
        client_1.connect()

        response = client_1.receive_data()
        self.assertEqual(response, 'Entered room\n')

        client_2 = Client("localhost", 5000)
        client_2.connect()

        response = client_2.receive_data()
        self.assertEqual(response, 'Entered room\n')                


if __name__ == '__main__':
    unittest.main()
