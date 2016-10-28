from datetime import datetime, time, timedelta
from settings import *


class Response(object):
    def __init__(self, body):
        # self.version = request.get_version()
        # self.path = request.get_path()
        # self.method = request.get_method()
        self.version = 'HTTP/1.1'
        self.body = body
        self.code = ''
        self.status = ''
        self.headers = {}
        self.set_default_headers()

    def set_default_headers(self):
        self.headers.setdefault('Server', SERVER_NAME)
        self.headers.setdefault('Date', datetime.now().ctime())
        self.headers.setdefault('Content-Length', str(len(self.body)))


    def set_cookie(self, sessionid):
        expires = datetime.utcnow() + timedelta(days=30)  # expires in 30 days
        expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.set_header('Set-cookie',
                        'SESSIONID=%s;  path=/; expires=%s;' % (sessionid, expires))

    def delete_cookie(self):
        self.set_header('Set-cookie', 'SESSIONID=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/;')

    def set_code(self, code):
        self.code = code

    def set_status(self, status):
        self.status = status

    def set_header(self, key, value):
        self.headers[key] = value

    def get_headers(self):
        return self.headers

    def encode_http(self):
        try:
            data = [b' '.join([self.version.encode(), self.code.encode(), self.status.encode()])]
            lines = []
            for key, value in sorted(iter(self.headers.items())):
                lines.append(b'%s: %s' % (key.encode(), value.encode()))
            header_lines = b'\r\n'.join(lines)
            if header_lines:
                data.append(header_lines)
                data.append(b'')
            if self.body:
                data.append(self.body.encode())
            http_data = b'\r\n'.join(data)
            return http_data
        except Exception as ex:
            print(ex)
            raise

    def redirect(self, location=''):
        self.set_code('303')
        self.set_status('See Other')
        self.set_header('Location', location)
        return self
