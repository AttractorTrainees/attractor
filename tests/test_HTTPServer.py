from unittest import TestCase

from selenium.webdriver.common.keys import Keys

from http_server import HTTPServer
from settings import *
import socket
from routes import Route
from handlers import *
from request import *
import selenium
from selenium import webdriver


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

        self.assertEqual((method, path, handler), (b'GET', b'/about', index))
        self.assertEqual(version, b'HTTP/1.1')
        self.assertEqual(body, None)
        self.assertEqual(header, None)

    def test_set_code_response(self):
        pass

    def test_data_bufersize(self):
        server = HTTPServer()
        buffer_size = 4096
        data = 200

        self.assertGreater(buffer_size, data)


class TestSelenium(TestCase):


    def test_open_our_blog(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:8000")
        self.elem = self.driver.find_element()
        assert "No results found." not in self.driver.page_source


    # def tearDown(self):
    #     self.driver.close()