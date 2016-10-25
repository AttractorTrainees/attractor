from unittest import TestCase
from selenium.webdriver.common.keys import Keys
from http_server import HTTPServer
from settings import *
import socket
from routes import Route
from handlers import *
from request import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

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

    def test_set_code_response(self):
        pass

    def test_data_bufersize(self):
        server = HTTPServer()
        buffer_size = 4096
        data = 200

        self.assertGreater(buffer_size, data)


class TestSelenium(TestCase):
    def test_if_user_is_not_authenticated(self):
        self.driver = webdriver.Firefox(    )
        self.driver.get("http://localhost:8000")
        body_text = self.driver.find_element_by_class_name('button').text
        print(body_text)
        self.assertEqual('Войти', body_text)
        self.driver.quit()

    def test_page_login(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:8000/login/")
        body_text = str(self.driver.find_element_by_tag_name('body').text).split('\n')
        print(body_text)
        self.assertIn('Логин', body_text)
        self.driver.quit()

    def test_login_page_submit(self):
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
        self.driver.quit()

    def test_you_have_no_accsses_to_send(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8000/send_article/')
        body_text = str(self.driver.find_element_by_tag_name('body').text).split('\n')
        print(body_text)
        self.assertIn('У вас недостаточно прав для добавления записи.', body_text)
        self.driver.quit()

    def test_you_have_no_accsses_to_edit(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8000/edit_article/1/')
        body_text = str(self.driver.find_element_by_tag_name('body').text).split('\n')
        print(body_text)
        self.assertIn('У вас недостаточно прав редактировать эту запись.', body_text)
        self.driver.quit()

    def test_not_found_url(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8000/abra-kadabra')
        body_text = str(self.driver.find_element_by_tag_name('body').text).split('\n')
        print(body_text)
        self.assertIn('404', body_text)
        self.driver.quit()

    def test_if_user_login(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://localhost:8000/login/')
        self.driver.set_script_timeout(50)
        username = self.driver.find_element_by_name('username')
        username.clear()
        username.send_keys('peter_user')
        password = self.driver.find_element_by_name('password')
        password.clear()
        password.send_keys('1234')
        enter = self.driver.find_element_by_name('enter').click()
        try:
            WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_class_name('button').text == 'Добавить запись')
        except Exception as e:
            print('Time out error')
        elem = str(self.driver.find_element_by_class_name('button').text).split('\n')
        print(elem)
        self.driver.quit()
        self.assertIn('Выйти', elem)
