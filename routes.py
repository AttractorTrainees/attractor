from routing import Route
from handlers import index, about, contacts,article

routes = [Route(b'GET', rb'^/', handler=index),
          Route(b'GET', rb'^/articles/([0-9]+)/$', handler=article),
          Route(b'GET', rb'^/about', about),
          Route(b'GET', rb'^/contacts', contacts)]
