from errors import handler_error_404
class Routing(object):
    def __init__(self, routes):
        self.routes = routes

    def handle_request(self, request):
        method = request.get_method()
        path = request.get_path()

        for route in self.routes:
            if route.method == method and route.path == path:
                return route.handler
        return handler_error_404


class Route(object):
    def __init__(self, method, path, handler):
        self.method = method
        self.path = path
        self.handler = handler
