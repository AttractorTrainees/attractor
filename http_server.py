import socket

from factory import RoutingFactory
from factory import RequestFactory
from parse import *
from routes import routes
from errors import handler_error
from settings import HOST, PORT, HOSTDOMAIN


class HTTPServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.request_factory = None
        self.routing_factory = None
        self.routing = None

    def activate_server(self):
        self.routing = self.routing_factory.createRouting(routes)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            print("Launching HTTP server...", HOSTDOMAIN)
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print("ERROR: Could not acquire port:", self.port, "\n")
            self.shutdown()
            import sys
            sys.exit(1)

        print("Server succesfully acquired the socket with port:", self.port)
        print("Waiting for connection\n")

        routingFactory = RoutingFactory()
        routing = routingFactory.createRouting(routes)

        while True:
            self.socket.listen(1)
            conn, adr = self.socket.accept()
            self.get_data(conn, routing)
            print("Got connection from:", adr, "\n")

    def get_data(self, connection, routing):
        buffer_size = 4096
        data = self.recv_all_data(connection, buffer_size)
        data = data.decode()
        if data:
            query, header, body = parse_http(data)

            # Check for right request, otherwise send response with status 400
            try:
                request = self.request_factory.createRequest(query, header, body)
            except Exception as e:
                response = handler_error, (400,)
                connection.send(response.encode_http())
                connection.close()
                return

            handler, args = routing.handle_request(request)
            response = handler(request, *args)
            response = response.encode_http()
            connection.send(response)

            connection.close()
            return

    def recv_all_data(self, connection, buffer_size):
        chunks = []
        EMPTY_BYTES = b''
        while True:
            data = connection.recv(buffer_size)
            if len(data) == buffer_size:
                chunks.append(data)
                continue
            chunks.append(data)
            print(chunks)
            data = EMPTY_BYTES.join(chunks)
            del chunks
            return data

    def shutdown(self):
        try:
            print("Shutting down the server")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed?", e)
