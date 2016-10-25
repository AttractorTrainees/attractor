import os
from dal import GetData
from data_access_layer import MemoryDataAccessLayer
from models import User, Article

'(.*\/.*)$'
SERVER_NAME = b'BlogServer/0.1'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

database = MemoryDataAccessLayer()
users = [User(firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12346'),
         User(firstname='Petr', lastname='Petrov', login='peter_user', password='1234'),
         User(firstname='John', lastname='Smith', login='john_user', password='123456'),
         User(firstname='Aibek', lastname='Abdykasymov', login='aibek', password='12345789'), ]
acticles = [
    Article(author=users[0], title='Article1', text='TextArticle1 '*10),
    Article(author=users[0], title='Article2', text='TextArticle2 '*10),
    Article(author=users[1], title='Article3', text='TextArticle3 '*10),
    Article(author=users[1], title='Article4', text='TextArticle4 '*10),
    Article(author=users[2], title='Article5', text='TextArticle5 '*10),
    Article(id=156, author=users[2], title='Article6', text='TextArticle6 '*10),
]

all_available_methods = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'
]

for article in acticles:
    database.add_article(article)
del acticles
for user in users:
    database.add_user(user)
del users
