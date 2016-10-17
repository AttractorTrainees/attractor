from routing import Route
from handlers import index, about, contacts

routes = [Route(b'GET', b'/', handler=index),
          Route(b'GET', b'/about', about),
          Route(b'GET', b'/contacts', contacts)]
