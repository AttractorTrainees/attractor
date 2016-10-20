from models import Article, User


class MemoryDataAccessLayer(object):
    def __init__(self):
        self.users = []
        self.articles = []


    # User options
    def add_user(self, user):
        self.users.append(user)

    def delete_user(self, user):
        try:
            self.users.remove(user)
            return True
        except ValueError as error:
            print(error)
            return False

    def get_user(self, attr, value):
        for user in self.users:
            try:
                if user.find_field_value(attr, value):
                    return user
            except AttributeError:
                return None
        return None

    def update_user(self, id, firstname, lastname, login):
        user = self.get_user('id', id)
        if user:
            user.set_attribute('firstname', firstname)
            user.set_attribute('lastname', lastname)
            user.set_attribute('login', login)
            return user
        return None

    ##Articles options
    def get_all_articles_by_author(self, author):
        get_articles = []
        for article in self.articles:
            try:
                if article.find_field_value('author', author):
                    get_articles.append(article)
            except AttributeError:
                print('Задан неправильный атрибут')
                return []
        return get_articles


    def add_article(self, article):
        self.articles.append(article)

    def get_all_articles_dict(self):  ##
        data_articles = []
        for article in self.articles:
            data_articles.append(article.get_article_dict())
        return data_articles

    def get_article(self, attr, value):
        for article in self.articles:
            try:
                if article.find_field_value(attr, value):
                    return article
            except AttributeError:
                print('Поле %s модели Article не найдено' % attr)
                return None


    def get_all_acticles(self):
        return self.articles

    def delete_article(self, article):
        try:
            self.articles.remove(article)
            return True
        except ValueError as error:
            print(error)
            return False

    def update_article(self, id, title, text):
        article = self.get_article('id', id)
        if article:
            article.set_attribute('title', title)
            article.set_attribute('text', text)
            return article
        return None
