# -*- coding: utf-8 -*-
import unittest
import select
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

    def test_send_short_message_server(self):
        print "testing short messages delivery...\n"
        client = Client("localhost", 5000)
        client.connect()
        
        response = client.receive_data()
        self.assertEqual(response, 'Entered room\n')
        
        message = "Testing some messaging\n"
        client.send_data(message)
        response = client.receive_data()
        self.assertEqual(response, message)

    def test_send_long_test_server(self):
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


if __name__ == '__main__':
    unittest.main()
