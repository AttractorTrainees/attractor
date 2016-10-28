import os

from factory import SessionFactory
from factory import ResponseFactory
from factory import ArticleFactory
from settings import database
from new_template_engine import TemplateEngine
from parse import *
from errors import handler_error, valid_error, login_required, LOGIN_FAILED_ERROR, CREATE_PERMISSION_DENIED_ERROR, EDIT_PERMISSION_DENIED_ERROR



TEXT_HTML = 'text/html'
CONTENT_TYPE = 'Content-type'
CODE_200 = '200'
OK = 'OK'

sessionFactory = SessionFactory()
responseFactory = ResponseFactory()
articleFactory = ArticleFactory()


def index(request):
    session = sessionFactory.createSession(request)
    user = session.find_session()
    articles = database.get_all_articles()
    context = {'articles': articles, 'user': user}
    rendered_body = TemplateEngine.render_template('index.html', context)
    response = responseFactory.createResponse(body=rendered_body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_code(CODE_200)
    response.set_status(OK)
    return response


def article(request, id):
    id = int(id)
    article = database.get_article('id', id)
    if not article:
        return handler_error(None, 404)
    session = sessionFactory.createSession(request)
    user = session.find_session()
    owner = True if article.author == user else False
    context = {'article': article, 'user': user, 'owner': owner}
    rendered_body = TemplateEngine.render_template('articles.html', context)
    response = responseFactory.createResponse(body=rendered_body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_status(OK)
    return response


def login(request):
    context = {'title': 'Авторизация', 'user': None}
    rendered_body = TemplateEngine.render_template('login.html', context)
    response = responseFactory.createResponse(body=rendered_body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_code(CODE_200)
    response.set_status(OK)
    return response


def sign_in(request):
    session = sessionFactory.createSession(request)
    sessionid = session.auth()
    user = None
    if sessionid:
        response = responseFactory.createResponse()
        response.set_cookie(sessionid)
        return response.redirect('/')
    return valid_error(1, user)


def logout(request):
    response = responseFactory.createResponse()
    response.delete_cookie()
    return response.redirect('/')


@login_required(error_code=CREATE_PERMISSION_DENIED_ERROR)
def send_article(request):
    session = sessionFactory.createSession(request)
    user = session.find_session()
    context = {'title': 'Добавить статью', 'user': user}

    rendered_body = TemplateEngine.render_template('add_article.html', context)
    response = responseFactory.createResponse(body=rendered_body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_code(CODE_200)
    response.set_status(OK)
    return response


def add_article(request):
    session = sessionFactory.createSession(request)
    author = session.find_session()
    article_data = query_parser(request.get_body())
    print(article_data)
    if author:
        database.add_article(
            articleFactory.createArticle(author=author, title=article_data['title'], text=article_data['text']))
    response = responseFactory.createResponse()
    return response.redirect('/')


@login_required(error_code=EDIT_PERMISSION_DENIED_ERROR)
def edit_article(request, id):
    session = sessionFactory.createSession(request)
    user = session.find_session()
    article = database.get_article('id', int(id))
    context = {'title': 'Редактировать статью', 'user': user, 'article': article}

    rendered_body = TemplateEngine.render_template('edit_article.html', context)

    response = responseFactory.createResponse(body=rendered_body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_code(CODE_200)
    response.set_status(OK)
    return response


def update_article(request):
    session = sessionFactory.createSession(request)
    author = session.find_session()
    article_data = query_parser(request.get_body())
    print(article_data)
    if author:
        database.update_article(id=int(article_data['id']), title=article_data['title'],
                                text=article_data['text'])
    response = responseFactory.createResponse()
    return response.redirect('/')


def delete_article(request, id):
    article = database.get_article('id', int(id))
    if article:
        database.delete_article(article)
        response = responseFactory.createResponse()
    return response.redirect('/')


def contacts(request):
    pass
