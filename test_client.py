# -*- coding: utf-8 -*-
import unittest
import select
import string
import random

from client import Client
from server import Server

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client('localhost', 5000)
        self.server = Server()

    def test_same_socket_init_connect(self):
        client_aux = Client()
        client_aux.connect('localhost', 5000)

        self.assertEqual(self.client.host, client_aux.host)
        self.assertEqual(self.client.port, client_aux.port)


    def test_send_short_message_server(self):
        message = "message with short length"
        self.client.connect()
        self.assertEqual(self.client.recieve_data(), 'Entered room')
        self.client.send_data(message)

        self.assertEqual(self.client.recieve_data(), message)

    def test_send_long_test_server(self):
        characters = (string.ascii_uppercase +
                      string.digits + ' ')
        message = ''.join(random.choice(characters) for x in range(6000))
        self.client.connect()
        self.assertEqual(self.client.recieve_data(), 'Entered room')
        self.client.send_data(message)

        self.assertEqual(self.client.recieve_data(), message)


if __name__ == '__main__':
    unittest.main()
