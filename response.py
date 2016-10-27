from datetime import datetime, time, timedelta
from settings import *


class Response(object):
    def __init__(self, body):
        # self.version = request.get_version()
        # self.path = request.get_path()
        # self.method = request.get_method()
        self.version = b'HTTP/1.1'
        self.body = body
        self.code = b''
        self.status = b''
        self.headers = {}
        self.set_default_headers()

    def set_default_headers(self):
        self.headers.setdefault(b'Server', SERVER_NAME)
        self.headers.setdefault(b'Date', datetime.now().ctime().encode())
        self.headers.setdefault(b'Content-Length', str(len(self.body)).encode())


    def set_cookie(self, sessionid):
        expires = datetime.utcnow() + timedelta(days=30)  # expires in 30 days
        expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.set_header(b'Set-cookie',
                        b'SESSIONID=%s;  path=/; expires=%s;' % (sessionid.encode(), expires.encode()))

    def delete_cookie(self):
        self.set_header(b'Set-cookie', b'SESSIONID=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/;')

    def set_code(self, code):
        self.code = code

    def set_status(self, status):
        self.status = status

    def set_header(self, key, value):
        if type(key) != bytes:
            key = key.encode()
        if type(value) != bytes:
            value = value.encode()
        self.headers[key] = value

    def get_headers(self):
        return self.headers

    def encode_http(self):
        try:
            data = [b' '.join([self.version, self.code, self.status])]
            lines = []
            for key, value in sorted(iter(self.headers.items())):
                lines.append(b'%s: %s' % (key, value))
            header_lines = b'\r\n'.join(lines)
            if header_lines:
                data.append(header_lines)
                data.append(b'')
            if self.body:
                data.append(self.body)
            http_data = b'\r\n'.join(data)
            return http_data
        except Exception as ex:
            print(ex)
            raise

    def redirect(self, location=''):
        self.set_code(b'303')
        self.set_status(b'See Other')
        if type(location) != bytes:
            location = location.encode()
        self.set_header(b'Location', location)
        return self
