from factory import Factory
from server_handlers import static_handler
from handlers import index, contacts, article, login, sign_in, logout, add_article, send_article, edit_article, \
    update_article, delete_article
factory = Factory.RouteFactory()
routes = [
    factory.createRoute(b'GET', rb'^/', handler=index),
    factory.createRoute(b'GET', rb'^/articles/([0-9]+)/$', handler=article),
    factory.createRoute(b'GET', rb'^/static/(.*/.*)$', handler=static_handler),
    factory.createRoute(b'GET', rb'^/login/$', handler=login),
    factory.createRoute(b'POST', rb'^/login/$', handler=sign_in),
    factory.createRoute(b'GET', rb'^/logout/$', handler=logout),
    factory.createRoute(b'POST', rb'^/add_article/$', handler=add_article),
    factory.createRoute(b'GET', rb'^/send_article/$', handler=send_article),
    factory.createRoute(b'GET', rb'^/edit_article/([0-9]+)/$', handler=edit_article),
    factory.createRoute(b'POST', rb'^/update_article/$', handler=update_article),
    factory.createRoute(b'GET', rb'^/delete_article/([0-9]+)/$', handler=delete_article),
]
