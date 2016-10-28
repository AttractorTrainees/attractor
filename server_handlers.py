import os

from factory import ResponseFactory
from settings import STATIC_DIR
from errors import handler_error

responseFactory = ResponseFactory()
def static_handler(request, path):
    try:
        file = open(os.path.join(STATIC_DIR, path))
        static_body = "".join(file.readlines())
        response = responseFactory.createResponse(body=static_body)
        response.set_header('Content-Type', 'text/css')
        response.set_code('200')
        response.set_status('OK')
        return response
    except Exception:
        return handler_error(request, 404)
