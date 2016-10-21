from tempate_engine import render
from response import Response
from settings import TEMPLATES_DIR
import os


def handler_error_404(request, *args):
    template = 'error_404.html'
    body = render(os.path.join(TEMPLATES_DIR, template), {}).encode()
    response = Response(request, body)
    response.set_code(code=b'404')
    response.set_status(status=b'Not Found')
    return response


def text(request, *args):
    print('ошибка', args)


class HTTPError(Exception):
    pass
