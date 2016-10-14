from routing import Route
from handlers import index, about, contacts

routes = [Route('GET', '/', index),
          Route('GET', '/about', about),
          Route('GET', '/contacts', contacts)]
