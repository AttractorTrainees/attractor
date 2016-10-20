import unittest
from models import User, Article
from data_access_layer import MemoryDataAccessLayer


def create_some_queries():
    db = MemoryDataAccessLayer()
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
        Article(id=6, author=users[2], title='Article6', text='TextArticle6'),
    ]
    for article in acticles:
        db.add_article(article)
    del acticles
    for user in users:
        db.add_user(user)
    del users

    return db


class ModelUserTest(unittest.TestCase):
    def test_get_user_dict(self):
        user = User(id=0, firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12345')
        user_dict = {'id': 0, 'firstname': 'Ivan', 'lastname': 'Ivanov', 'login': 'super_mega_user'}
        self.assertEqual(user.get_user_dict(), user_dict)


class DalUserTest(unittest.TestCase):
    def test_insert_and_get_user_from_db(self):
        db = create_some_queries()
        user = User(id=5, firstname='Leonard', lastname='Shepard', login='super_general', password='12345')
        db.add_user(user)
        get_user = db.get_user('id', 5)
        self.assertEqual(user, get_user)

    def test_delete_user_from_db(self):
        db = create_some_queries()
        user = User(id=1, firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12346')
        db.add_user(user)
        self.assertTrue(db.delete_user(user))

    def test_update_user_from_db(self):
        db = create_some_queries()
        id, firstname, lastname, login = 1, 'Lesli', 'Vaigen', 'lesli'
        updated_user = db.update_user(id, firstname, lastname, login)

        user = db.get_user('id', 1)
        self.assertEqual(user, updated_user)

    def test_get_all_acticles_by_author(self):
        db = create_some_queries()
        author = db.get_user('id', 1)
        get_acticles = [db.get_article('id', 1), db.get_article('id', 2)]
        query_articles = db.get_all_articles_by_author(author)
        self.assertEqual(query_articles, get_acticles)
