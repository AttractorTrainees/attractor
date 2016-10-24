class Request(object):
    def __init__(self, query, headers, body):
        self._method = query[0]
        self._path = query[1]
        self._version = query[2]
        self._headers = headers
        self._body = body

    def get_method(self):
        return self._method

    def set_method(self, method):
        self._method = method

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_headers(self):
        return self._headers

    def get_header(self, name):
        return self._headers.get(name)

    def get_body(self):
        return self._body

    def set_body(self, body):
        self._body = body

    def get_cookie(self):
        value = self.get_header(b'COOKIE')
        if value:
            sessionid = value.split(b'=', 1)[1:]
            if sessionid:
                return sessionid.decode()
            return None
        return None