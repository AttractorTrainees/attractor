from unittest import TestCase
from parse import *

class TestParse_http(TestCase):
    def test_parse_http(self):
        string = b"""
            'GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4\r\nCookie: Pycharm-46659b5b=1c84beb3-f64b-4038-82fb-06887ca9fd50; csrftoken=xXVqimJCWPtiyQfIy3G5yhFph1Ffl4xu\r\n\r\n'
        """
        query, header, body = parse_http(string)

        self.assertTrue(query, True)
        self.assertTrue(header, True)
        self.assertTrue(body, True)

class TestQuery_parser(TestCase):
    def test_query_parser(self):
        string = b'name=allen&password=123'
        query = query_parser(string)
        self.assertEqual({b'name': b'allen', b'password': b'123'}, query)


