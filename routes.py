from routing import Route
from server_handlers import static_handler
from handlers import index, about, contacts, article, login, sign_in

routes = [
    Route(b'GET', rb'^/', handler=index),
    Route(b'GET', rb'^/articles/([0-9]+)/$', handler=article),
    Route(b'GET', rb'^/static/(.*/.*)$', handler=static_handler),
    Route(b'GET', rb'^/login/$', handler=login),
    Route(b'POST', rb'^/login/$', handler=sign_in),
]
