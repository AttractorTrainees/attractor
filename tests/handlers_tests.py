import unittest
from request import Request
from session import Session
from factory import Factory
from routes import routes
from http_server import HTTPServer
from parse import parse_http

class CreateRequest(object):
    def __init__(self):
        self.method = b'GET'
        self.path = b'/'
        self.version = b'HTTP/1.1'
        self.headers = {b''}
        self.body = b'\r\n'

    def create_request(self, headers, body):
        request = Request((self.method, self.path, self.version), headers, body)
        return request

class MockConnection(object):
    def __init__(self, data=''):
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
        routingFactory = Factory.RoutingFactory()
        routing = routingFactory.createRouting(routes)
        conn = MockConnection(b'GET ' + str.encode(url) + b' HTTP/1.1\r\nUser-Agent: Mozilla\r\n\r\n')
        self.server.getting_data(conn, routing)
        return parse_http(conn.sent)

class TestServer(unittest.TestCase):
    def test_404(self):
        server = HTTPServer()
        client = MockClient(server)
        reply, headers, body = client('/test/test')
        print(reply)
        print(headers)
        print(body)
        self.assertEqual(reply, [b'HTTP/1.1', b'404', b'NOT_FOUND'])
        self.assertEqual(headers[b'SERVER'], b'BlogServer/0.1')


class TestSessions(unittest.TestCase):

    def test_auth(self):
        body = b'\r\nusername=john_user&password=123456'
        request = CreateRequest()
        session = Session(request.create_request(request.headers, body))
        sessionid = session.auth()
        self.assertNotEqual(sessionid, False)

    def test_find_session(self):
        headers = {b'COOKIE': b'SESSIONID=123'}
        request = CreateRequest()
        session = Session(request.create_request(headers, request.body))
        user = session.find_session()
        self.assertNotEqual(user, None)


class TestResponse(unittest.TestCase):
    def test_response(self):
        pass

    def test_encode_http(self):
        pass

    def test_redirect(self):
        pass

