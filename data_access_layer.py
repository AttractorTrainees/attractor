from models import Article, User


class MemoryDataAccessLayer(object):
    def __init__(self):
        self.users = []
        self.articles = []


    ##User options
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
            user.set_attribute('lastname', firstname)
            user.set_attribute('login', firstname)
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


    def get_data_all_articles(self, ):  ##
        pass


    def get_article(self, attr, value):
        for article in self.articles:
            try:
                if article.find_field_value(attr, value):
                    return article
            except AttributeError:
                return None


    def get_all_acticles(self):
        return self.articles
