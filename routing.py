import re
from errors import handler_error_404, text


class Routing(object):
    def __init__(self, routes):
        self.routes = routes

    def handle_request(self, request):
        method = request.get_method()
        path = request.get_path()

        for route in self.routes:
            if route.method == method and self.get_match_path(route.path, path):
                return route.handler, self.get_args(route.path, path)
        return handler_error_404, ()

    def get_match_path(self, rexep_path, path):
        rexep = re.compile(rexep_path)
        match = re.match(rexep, path)
        if match and match.group() == path:
            return True
        return False

    def get_args(self, rexep_path, path):
        value = None
        rexep = re.compile(rexep_path)
        match = re.match(rexep, path)
        if match:
            value = match.groups()
        return value


class Route(object):
    def __init__(self, method, path, handler):
        self.method = method
        self.path = path
        self.handler = handler
