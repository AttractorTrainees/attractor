from factory import HTTPServerFactory


if __name__ == "__main__":
    factory = HTTPServerFactory()
    server = factory.createHTTPServer()
    server.activate_server()