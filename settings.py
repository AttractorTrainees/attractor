import os
from dal import GetData
from data_access_layer import MemoryDataAccessLayer
from models import User, Article

SERVER_NAME = b'BlogServer/0.1'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

database = MemoryDataAccessLayer()
users = [User(id=1, firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12346'),
         User(id=2, firstname='Petr', lastname='Petrov', login='peter_user', password='1234'),
         User(id=3, firstname='John', lastname='Smith', login='john_user', password='123456'),
         User(id=4, firstname='Aibek', lastname='Abdykasymov', login='aibek', password='12345789'), ]
acticles = [
    Article(id=1, author=users[0], title='Article1', text='TextArticle1'),
    Article(id=2, author=users[0], title='Article2', text='TextArticle2'),
    Article(id=3, author=users[1], title='Article3', text='TextArticle3'),
    Article(id=4, author=users[1], title='Article4', text='TextArticle4'),
    Article(id=5, author=users[2], title='Article5', text='TextArticle5'),
    Article(id=156, author=users[2], title='Article6', text='TextArticle6'),
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