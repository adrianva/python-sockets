# -*- coding: utf-8 -*-
import unittest
import select
import string
import random

from server import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    def test_initialize_server_socket(self):
        self.server.initialize_server_socket()
        # When initialize the server the list of connections contains the socket server
        self.assertEqual(1, len(self.server.connection_list))


if __name__ == '__main__':
    unittest.main()

