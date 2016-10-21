import os
from settings import database
from tempate_engine import render
from response import Response
from parse import *
from errors import handler_error
from settings import TEMPLATES_DIR
from session import Session


def open_html(template):
    file = open(os.path.join(TEMPLATES_DIR, template))
    html = file.readlines()
    return ''.join(html)

def index(request):
    articles = database.get_all_articles()
    context = {'articles': articles}
    rendered_body = render(os.path.join(TEMPLATES_DIR, 'index.html'), context).encode()
    response = Response(body=rendered_body)

    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response

def article(request, id):
    id = int(id)
    article = database.get_article('id', id)
    if not article:
        return handler_error((404,))
    context = {'article': article}
    template_path = os.path.join(TEMPLATES_DIR, 'articles.html')
    rendered_body = render(template_path, context).encode()
    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_status(b'OK')
    return response

def login(request):
    session = Session(request)
    sessionid = session.auth()

    response = Response(request, body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    if sessionid:
        response.set_cookie(sessionid)

    return response

def logout(request):

    response = Response(request, body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    response.delete_cookie()

    return response

def about(request):
    pass


def contacts(request):
    pass
