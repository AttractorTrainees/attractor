from factory import Factory


if __name__ == "__main__":
    factory = Factory.HTTPServerFactory()
    server = factory.createHTTPServer()
    server.activate_server()