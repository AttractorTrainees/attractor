from datetime import datetime


class Article(object):
    def __init__(self, author, id=0, title='', text=''):
        self.id = id
        self.author = author
        self.title = title
        self.text = text
        self.created_datetime = datetime.now()
        self.updated_datetime = datetime.now()

    def find_field_value(self, attr, value):
        if getattr(self, attr) == value:
            return True
        else:
            return False

    def set_updated_datetime(self):
        self.updated_datetime = datetime.now()

    def get_article_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'text': self.text,
            'created_datetime': self.created_datetime,
            'updated_datetime': self.updated_datetime
        }

    def __str__(self):
        return '%d %s %s %s %s %s' % (self.id, self.author, self.title, self.text,
                                      self.created_datetime, self.updated_datetime)

    def set_attribute(self, attr, value):
        if hasattr(self, attr):
            setattr(self, attr, value)


class User(object):
    def __init__(self, id=0, firstname='', lastname='', login='', password='', sessionid=''):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.login = login
        self.password = password
        self.sessionid = sessionid

    def find_field_value(self, attr, value):
        if getattr(self, attr) == value:
            return True
        else:
            return False

    def __str__(self):
        return self.official_name

    @property
    def official_name(self):
        return '%s %s' % (self.firstname, self.lastname)

    def get_user_dict(self):
        return {'id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'login': self.login}

    def set_attribute(self, attr, value):
        if hasattr(self, attr):
            setattr(self, attr, value)
