import os
from tempate_engine import render
from response import Response

from settings import TEMPLATES_DIR


def open_html(template):
    file = open(os.path.join(TEMPLATES_DIR, template))
    html = file.readlines()
    return ''.join(html)


def index(request):
    context = {'itemlist': [1, 2, 3]}
    rendered_body = render(os.path.join(TEMPLATES_DIR, 'index.html'), context).encode()
    response = Response(request, body=rendered_body)

    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def about(request):
    pass


def contacts(request):
    pass
