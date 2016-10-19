import socket
from parser import *
from request import Request
from routing import Routing
from routes import routes


class HTTPServer:
    def __init__(self, port=8000):
        self.host = 'localhost'
        self.port = port

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            print("Launching HTTP server...", self.host, ":", self.port)
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print("ERROR: Could not aquire port:", self.port, "\n")
            self.shutdown()
            import sys
            sys.exit(1)

        print("Server succesfully acquired the socket with port:", self.port)
        print("Waiting for connection\n")
        routing = Routing(routes)
        while True:
            self.socket.listen(1)
            conn, adr = self.socket.accept()
            self.getting_data(conn, routing)
        print("Got connection from:", adr, "\n")

    def getting_data(self, connection, routing):
        buffer_size = 4096
        data = self.recv_all_data(connection, buffer_size)
        query, header, body = parse_http(data)
        request = Request(query, header, body)

        handler = routing.handle_request(request)
        response = handler(request)
        connection.send(response.encode_http())
        connection.close()

    def recv_all_data(self, connection, buffer_size):

        msglen = 0
        chunks = []
        EMPTY_BYTES = b''
        while True:
            data = connection.recv(buffer_size)
            if len(data) == buffer_size:
                chunks.append(data)
                continue
            msglen = len(data)
            chunks.append(data)
            data = EMPTY_BYTES.join(chunks)
            del chunks
            return data

    def shutdown(self):
        try:
            print("Shutting down the server")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed?", e)