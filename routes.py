from factory import RouteFactory
from server_handlers import static_handler
from handlers import index, contacts, article, login, sign_in, logout, add_article, send_article, edit_article, \
    update_article, delete_article
factory = RouteFactory()
routes = [
    factory.createRoute('GET', r'^/', handler=index),
    factory.createRoute('GET', r'^/articles/([0-9]+)/$', handler=article),
    factory.createRoute('GET', r'^/static/(.*/.*)$', handler=static_handler),
    factory.createRoute('GET', r'^/login/$', handler=login),
    factory.createRoute('POST', r'^/login/$', handler=sign_in),
    factory.createRoute('GET', r'^/logout/$', handler=logout),
    factory.createRoute('POST', r'^/add_article/$', handler=add_article),
    factory.createRoute('GET', r'^/send_article/$', handler=send_article),
    factory.createRoute('GET', r'^/edit_article/([0-9]+)/$', handler=edit_article),
    factory.createRoute('POST', r'^/update_article/$', handler=update_article),
    factory.createRoute('GET', r'^/delete_article/([0-9]+)/$', handler=delete_article),
]
