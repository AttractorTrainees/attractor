from routing import Route
from server_handlers import static_handler
from handlers import index, contacts, article, login, sign_in, logout, add_article, send_article, edit_article, \
    update_article, delete_article

routes = [
    Route(b'GET', rb'^/', handler=index),
    Route(b'GET', rb'^/articles/([0-9]+)/$', handler=article),
    Route(b'GET', rb'^/static/(.*/.*)$', handler=static_handler),
    Route(b'GET', rb'^/login/$', handler=login),
    Route(b'POST', rb'^/login/$', handler=sign_in),
    Route(b'GET', rb'^/logout/$', handler=logout),
    Route(b'POST', rb'^/add_article/$', handler=add_article),
    Route(b'GET', rb'^/send_article/$', handler=send_article),
    Route(b'GET', rb'^/edit_article/([0-9]+)/$', handler=edit_article),
    Route(b'POST', rb'^/update_article/$', handler=update_article),
    Route(b'GET', rb'^/delete_article/([0-9]+)/$', handler=delete_article),
]
