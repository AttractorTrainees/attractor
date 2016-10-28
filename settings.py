import os
from factory import UserFactory
from factory import ArticleFactory

from data_access_layer import MemoryDataAccessLayer

SERVER_NAME = 'BlogServer/0.1'
HOST = '127.0.0.1'
PORT = 8000
HOSTDOMAIN = 'http://%s:%s' % (HOST, PORT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static'

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
OPTIONS = 'OPTIONS'
HEAD = 'HEAD'

userFactory = UserFactory()
articleFactory = ArticleFactory()




database = MemoryDataAccessLayer()
users = [userFactory.createUser(firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12346'),
         userFactory.createUser(firstname='Petr', lastname='Petrov', login='peter_user', password='1234',
                                sessionid='123'),
         userFactory.createUser(firstname='John', lastname='Smith', login='john_user', password='123456'),
         userFactory.createUser(firstname='Aibek', lastname='Abdykasymov', login='aibek', password='12345789'), ]
acticles = [
    articleFactory.createArticle(author=users[0], title='Article1', text='TextArticle1 ' * 10),
    articleFactory.createArticle(author=users[0], title='Article2', text='TextArticle2 ' * 10),
    articleFactory.createArticle(author=users[1], title='Article3', text='TextArticle3 ' * 10),
    articleFactory.createArticle(author=users[1], title='Article4', text='TextArticle4 ' * 10),
    articleFactory.createArticle(author=users[2], title='Article5', text='TextArticle5 ' * 10),
    articleFactory.createArticle(id=156, author=users[2], title='Article6', text='TextArticle6 ' * 10),
]



all_available_methods = [
    GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
]

for article in acticles:
    database.add_article(article)
del acticles
for user in users:
    database.add_user(user)
del users
