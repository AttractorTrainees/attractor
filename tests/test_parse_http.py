from unittest import TestCase
from parse import *

class TestParsers(TestCase):
    def test_parse_http(self):
        self.assertEqual(parse_http(b'GET / HTTP/1.1\r\nUser-Agent: Mozilla'),
                         ([b'GET', b'/', b'HTTP/1.1'], {b'USER-AGENT': b'Mozilla'}, b''))

    def test_query_parser(self):
        self.assertEqual(query_parser(b'\r\ntitle=123&text=123&id=0'),
                             ({b'text': b'123', b'title': b'123', b'id': b'0'}))

    def test_multipart_parser(self):
        pass


