from factory import HTTPServerFactory, RequestFactory, RoutingFactory


if __name__ == "__main__":
    http_server_factory = HTTPServerFactory()
    request_factory = RequestFactory()
    routing_factory = RoutingFactory()

    server = http_server_factory.createHTTPServer()
    server.routing_factory = routing_factory
    server.request_factory = request_factory
    server.activate_server()