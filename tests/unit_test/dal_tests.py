import unittest
from models import User, Article
from data_access_layer import MemoryDataAccessLayer


def create_some_queries():
    db = MemoryDataAccessLayer()
    users = [User(firstname='Ivan', lastname='Ivanov', login='super_mega_user', password='12346'),
             User(firstname='Petr', lastname='Petrov', login='peter_user', password='1234'),
             User(firstname='John', lastname='Smith', login='john_user', password='123456'),
             User(firstname='Aibek', lastname='Abdykasymov', login='aibek', password='12345789'), ]
    acticles = [
        Article(author=users[0], title='Article1', text='TextArticle1'),
        Article(author=users[0], title='Article2', text='TextArticle2'),
        Article(author=users[1], title='Article3', text='TextArticle3'),
        Article(author=users[1], title='Article4', text='TextArticle4'),
        Article(author=users[2], title='Article5', text='TextArticle5'),
        Article(author=users[2], title='Article6', text='TextArticle6'),
    ]
    for article in acticles:
        db.add_article(article)
    del acticles
    for user in users:
        db.add_user(user)
    del users

    return db


# class ModelUserTest(unittest.TestCase):

db = create_some_queries()

class DalUserTest(unittest.TestCase):
    def test_insert_and_get_user(self):
        user = User(id=125, firstname='Leonard', lastname='Shepard', login='super_general', password='12345')
        db.add_user(user)
        get_user = db.get_user('id', 125)
        self.assertEqual(user, get_user)

    def test_delete_user_from_db(self):
        user = db.get_user('id', 4)
        self.assertTrue(db.delete_user(user))

    def test_update_user_from_db(self):
        id, firstname, lastname, login = 1, 'Lesli', 'Vaigen', 'lesli'
        updated_user = db.update_user(id, firstname, lastname, login)

        self.assertEqual('Lesli', updated_user.firstname)
        self.assertEqual('Vaigen', updated_user.lastname)
        self.assertEqual('lesli', updated_user.login)


class DalArticleTest(unittest.TestCase):
    def test_get_all_acticles_by_author(self):
        author = db.get_user('login', 'super_mega_user')
        get_acticles = [db.get_article('id', 1), db.get_article('id', 2)]
        query_articles = db.get_all_articles_by_author(author)
        self.assertEqual(query_articles, get_acticles)

    def test_insert_and_get_article(self):
        author = db.get_user('id', 4)
        article = Article(id=7, author=author, title='New Article', text='Content-From-New-Article')
        db.add_article(article)
        get_article = db.get_article('id', 7)
        self.assertEqual(get_article, article)

    def test_delete_article(self):
        article = db.get_article('id', 4)
        self.assertTrue(db.delete_article(article))

    def test_update_article(self):
        db = create_some_queries()
        id, title, text = 1, 'TestTitle', 'TestText',
        updated_article = db.update_article(id, title, text)
        article = db.get_article('id', 1)
        self.assertEqual(article, updated_article)
