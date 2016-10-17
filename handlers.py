import os

from response import Response

from attractor.settings import TEMPLATES_DIR


def open_html(template):
    file = open(os.path.join(TEMPLATES_DIR, template))
    html = file.readlines()
    return ''.join(html).encode()


def index(request):
    body = open_html('index.html')
    response = Response(request, body=body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def about(request):
    pass


def contacts(request):
    pass
