import os

from models import Article
from settings import database
from tempate_engine import render
from response import Response
from parse import *
from errors import handler_error, valid_error, login_required
from settings import TEMPLATES_DIR
from session import Session


def open_html(template):
    file = open(os.path.join(TEMPLATES_DIR, template))
    html = file.readlines()
    return ''.join(html)


def index(request):
    session = Session(request)
    user = session.find_session()
    articles = database.get_all_articles()
    context = {'articles': articles, 'user': user}
    rendered_body = render(os.path.join(TEMPLATES_DIR, 'index.html'), context).encode()
    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def article(request, id):
    id = int(id.decode())
    article = database.get_article('id', id)
    if not article:
        return handler_error(None, 404)
    session = Session(request)
    user = session.find_session()
    owner = True if article.author == user else False
    context = {'article': article, 'user': user, 'owner': owner}
    template_path = os.path.join(TEMPLATES_DIR, 'articles.html')
    rendered_body = render(template_path, context).encode()
    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_status(b'OK')
    return response


def login(request):
    template_path = os.path.join(TEMPLATES_DIR, 'login.html')
    context = {'title': 'Авторизация', 'user': None}
    rendered_body = render(template_path, context).encode()
    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def sign_in(request):
    session = Session(request)
    sessionid = session.auth()
    user = None
    if sessionid:
        response = Response()
        response.set_cookie(sessionid)
        return response.redirect('/')
    return valid_error(1, user)


def logout(request):
    response = Response()
    response.delete_cookie()
    return response.redirect('/')


@login_required(error_code=3)
def send_article(request):
    template_path = os.path.join(TEMPLATES_DIR, 'add_article.html')
    session = Session(request)
    user = session.find_session()
    context = {'title': 'Добавить статью', 'user': user}

    rendered_body = render(template_path, context).encode()

    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def add_article(request):
    session = Session(request)
    author = session.find_session()
    article_data = query_parser(request.get_body())
    print(article_data)
    database.add_article(
        Article(author=author, title=article_data[b'title'].decode(), text=article_data[b'text'].decode()))
    response = Response()
    return response.redirect('/')


@login_required(error_code=2)
def edit_article(request, id):
    template_path = os.path.join(TEMPLATES_DIR, 'edit_article.html')
    session = Session(request)
    user = session.find_session()
    article = database.get_article('id', int(id.decode()))
    print('***********************************', article)
    context = {'title': 'Редактировать статью', 'user': user, 'article': article}

    rendered_body = render(template_path, context).encode()

    response = Response(body=rendered_body)
    response.set_header(b'Content-Type', b'text/html')
    response.set_code(b'200')
    response.set_status(b'OK')
    return response


def update_article(request):
    article_data = query_parser(request.get_body())
    print(article_data)
    database.update_article(id=int(article_data[b'id'].decode()), title=article_data[b'title'].decode(),
                            text=article_data[b'text'].decode())
    response = Response()
    return response.redirect('/')


def delete_article(request, id):
    article = database.get_article('id', int(id.decode()))
    if article:
        database.delete_article(article)
    response = Response()
    return response.redirect('/')


def contacts(request):
    pass
