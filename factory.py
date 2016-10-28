class HTTPServerFactory(object):
    def createHTTPServer(self):
        from http_server import HTTPServer
        return HTTPServer()


class RoutingFactory(object):
    def createRouting(self, routes):
        from routing import Routing
        return Routing(routes)


class RequestFactory(object):
    def createRequest(self, query, header, body):
        from request import Request
        return Request(query, header, body)


class ResponseFactory(object):
    def createResponse(self, body=''):
        from response import Response
        return Response(body)


class SessionFactory(object):
    def createSession(self, request):
        from session import Session
        return Session(request)


class RouteFactory(object):
    def createRoute(self, method, path, handler):
        from routing import Route
        return Route(method, path, handler)


class UserFactory(object):
    def createUser(self, id=0, firstname='', lastname='', login='', password='', sessionid=''):
        from models import User
        return User(id, firstname, lastname, login, password, sessionid)


class ArticleFactory(object):
    def createArticle(self, author, id=0, title='', text=''):
        from models import Article
        return Article(author, id, title, text)


class MemoryDataAccessLayerFactory(object):
    def createMemoryDataAccessLayer(self):
        from data_access_layer import MemoryDataAccessLayer
        return MemoryDataAccessLayer()
