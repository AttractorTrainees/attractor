from server import database

class DataBase:
    def __init__(self):
        self.articles = []
        self.users = [(1, 'admin', 'admin','')]

class GetData:

    def get_articles(self):
        return list(database.articles)

    def get_article(self, id):
        for i in database.articles:
            if id == database.articles[i][0]:
                return database.articles[i]
        print('Запись не найдена')

    def add_article(self, content, author_id, date):
        articles = self.get_articles
        id = 0
        for i in articles:
            if id < articles[i][0]:
                id = articles[i][0]
        id += 1
        if content and author_id and date:
            database.articles.append((id, content, author_id, date))
                return True
        print('Заполнены не все поля')

    def delete_article(self, id):
        for i in database.articles:
            if id == database.articles[i][0]:
                database.articles.remove(i)
                return True
        print('Запись не найдена')

    def get_user(self, login):
        for i in database.users:
            if login == database.users[i][1]:
                return database.users[i]
        print('Запись не найдена')

    def get_sessionid(self):
        for i in database.users:
