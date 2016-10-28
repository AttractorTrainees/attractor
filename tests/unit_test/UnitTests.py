import handlers
from unittest import TestCase
from parse import *
from factory import RequestFactory, RoutingFactory
from parse import parse_http, multipart_parser
from routing import *
from request import Request
from routes import routes
from session import Session
from http_server import HTTPServer
from tests.multipart_data import multipart


class TestParse_http(TestCase):
    def test_parse_http(self):
        string = 'GET / HTTP/1.1\r\nUser-Agent: Mozilla\r\n\r\n'
        query, header, body = parse_http(string)
        self.assertEqual(query, ['GET', '/', 'HTTP/1.1'])
        self.assertEqual(header, {'USER-AGENT':'Mozilla'})
        self.assertEqual(body, '\r\n')


class TestQuery_parser(TestCase):
    def test_query_parser(self):
        string = 'name=allen&password=123'
        query = query_parser(string)
        self.assertEqual({'name': 'allen', 'password': '123'}, query)


class TestMultipart_parser(TestCase):
    def test_multipart_parser(self):
        query, header, body = parse_http(multipart)
        multipart_request = RequestFactory().createRequest(query, header, body)
        multipart_parsed = multipart_parser(body, multipart_request)
        self.assertEqual(3, len(multipart_parsed))
        list_of_keys = ['body', 'name', 'form']
        self.assertEqual(set(list(multipart_parsed[0].keys())), set(list_of_keys))


class TestRouting(TestCase):
    def test_handle_request(self):
        string = 'GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4\r\nCookie: Pycharm-46659b5b=1c84beb3-f64b-4038-82fb-06887ca9fd50; csrftoken=xXVqimJCWPtiyQfIy3G5yhFph1Ffl4xu\r\n\r\n'
        query, header, body = parse_http(string)
        requestFactory = RequestFactory()
        request = requestFactory.createRequest(query, header, body)
        routing = Routing(routes)
        handler, args = routing.handle_request(request)

        self.assertEqual(handler, handlers.index)

class CreateRequest(object):
    def __init__(self):
        self.method = 'GET'
        self.path = '/'
        self.version = 'HTTP/1.1'
        self.headers = {''}
        self.body = '\r\n'

    def create_request(self, headers, body):
        request = Request((self.method, self.path, self.version), headers, body)
        return request

class MockConnection(object):
    def __init__(self, data=b''):
        self.read = data
        self.sent = b''

    def recv(self, buf_size=None):
        return self.read

    def send(self, data):
        self.sent += data

    def close(self):
        pass

class MockClient(object):
    def __init__(self, server):
        self.server = server

    def __call__(self, url):
        routingFactory = RoutingFactory()
        routing = routingFactory.createRouting(routes)
        conn = MockConnection(b'GET ' + url.encode() + b' HTTP/1.1\r\nUser-Agent: Mozilla\r\n\r\n')
        self.server.get_data(conn, routing)
        return parse_http(conn.sent.decode())

class TestServer(TestCase):
    def test_404(self):
        server = HTTPServer()
        client = MockClient(server)
        reply, headers, body = client('/test/test')
        self.assertEqual(reply, ['HTTP/1.1', '404', 'NOT_FOUND'])
        self.assertEqual(headers['SERVER'], 'BlogServer/0.1')

class TestSessions(TestCase):

    def test_auth(self):
        body = '\r\nusername=john_user&password=123456'
        request = CreateRequest()
        session = Session(request.create_request(request.headers, body))
        sessionid = session.auth()
        self.assertNotEqual(sessionid, False)

    def test_find_session(self):
        headers = {'COOKIE': 'SESSIONID=123'}
        request = CreateRequest()
        session = Session(request.create_request(headers, request.body))
        user = session.find_session()
        self.assertNotEqual(user, None)


class TestResponse(TestCase):
    def test_response(self):
        pass

    def test_encode_http(self):
        pass

    def test_redirect(self):
        pass