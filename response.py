class Response(object):
    def __init__(self, request, body=b''):
        self.version = request.get_version()
        self.path = request.get_path()
        self.method = request.get_method()
        self.body = body
        self.code = b''
        self.status = b''
        self.headers = {}

    def set_header(self, key, value):
        self.headers['key'] = value

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
