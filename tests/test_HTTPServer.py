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
          Route(b'GET', b'/contacts', contacts),
          ]


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

    # def test_routes_is_equal_about_request(self):
    #     query = [b'GET', b'/about', b'HTTP/1.1']
    #     header = None
    #     body = None
    #     request = Request(query, header, body)
    #     method = query[0]
    #     path = query[1]
    #     handler = index
    #     version = request.get_version()
    #     body = request.set_body(None)
    #
    #     self.asserNotEqual((method, path, handler), (b'GET', b'/about', index))
    #     self.assertNotEqual(version, b'HTTP/1.1')
    #     self.assertNotEqual(body, None)
    #     self.assertNotEqual(header, None)

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
        self.elem = self.driver.find_element_by_class_name("button")
        self.elem.click()
        # we are in login page
        # assert self.elem.text

    def test_login_page(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:8000/login/")
        self.enter = self.driver.find_element_by_name('enter')
        self.username = self.driver.find_element_by_name('username')
        self.username.clear()
        self.username.send_keys('peter_user')
        self.password = self.driver.find_element_by_name('password')
        self.password.clear()
        self.password.send_keys('1234')
        self.enter.submit()


