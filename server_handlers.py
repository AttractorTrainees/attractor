import os
from settings import STATIC_DIR
from response import Response


def static_handler(request, path):
    file = open(os.path.join(STATIC_DIR, path.decode()))
    static_body = "".join(file.readlines()).encode()
    print(static_body)
    response = Response(request, body=static_body)
    response.set_header(b'Content-Type', b'text/css')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response
