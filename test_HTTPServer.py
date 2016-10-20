from unittest import TestCase
from http_server import HTTPServer
from settings import *
import socket
from routes import Route
from handlers import *
from request import *

routes = [Route(b'GET', b'/', index),
          Route(b'GET', b'/about', about),
          Route(b'GET', b'/contacts', contacts)]


class TestHTTPServer(TestCase):
    def test_activate_server(self):
        server = HTTPServer()
        self.assertEqual(server.port, 8000)
        self.assertEqual(server.host, 'localhost')


    def test_activate_server_wrong_port(self):
        server = HTTPServer()
        self.assertNotEquals(server.port, 8080)


class TestRoutes(TestCase):
    def test_routes_is_not_equal_request(self):
        query = [b'GET', b'/path', b'HTTP/1.1']
        header = None
        body = None
        request = Request(query, header, body)
        method = query[0]
        path = query[1]
        handler = index

        self.assertNotEqual((method, path, handler), routes[0])
        self.assertNotEqual((method, path, handler), routes[1])
        self.assertNotEqual((method, path, handler), routes[2])

    def test_routes_is_equal_index_request(self):
        query = [b'GET', b'/', b'HTTP/1.1']
        header = None
        body = None
        request = Request(query, header, body)
        method = query[0]
        path = query[1]
        handler = index

        self.assertEqual((method, path, handler), (b'GET', b'/', index))

    def test_routes_is_equal_about_request(self):
        query = [b'GET', b'/about', b'HTTP/1.1']
        header = None
        body = None
        request = Request(query, header, body)
        method = query[0]
        path = query[1]
        handler = index
        version = request.get_version()
        body = request.set_body(None)
        header = request.set_header(None)

        self.assertEqual((method, path, handler), (b'GET', b'/about', index))
        self.assertEqual(version, b'HTTP/1.1')
        self.assertEqual(body, None)
        self.assertEqual(header, None)


