from datetime import datetime

DATE_FORMAT = '%d %b %Y %H:%M:%S'


class IdentityException(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return self.__value


class Model(object):
    def find_field_value(self, attr, value):
        if getattr(self, attr) == value:
            return True
        else:
            return False

    def set_attribute(self, attr, value):
        if hasattr(self, attr):
            setattr(self, attr, value)


class IdentityPermission(object):
    counter = 0

    def identity(self, id=0):
        if id == 0:
            self.__class__.counter += 1
        elif id > self.counter:
            self.__class__.counter = id
        else:
            raise IdentityException('id должна быть больше')
        return self.counter

    def set_identity(self, counter):
        self.__class__.counter = counter


class Article(Model, IdentityPermission):
    def __init__(self, author='', id=0, title='', text=''):
        self.id = self.identity(id)
        self.author = author
        self.title = title
        self.text = text
        self.created_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.updated_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def set_updated_datetime(self):
        self.updated_datetime = datetime.now()

    def __str__(self):
        return '%d %s %s %s %s %s' % (self.id, self.author, self.title, self.text,
                                      self.created_datetime, self.updated_datetime)


class User(Model, IdentityPermission):
    def __init__(self, id=0, firstname='', lastname='', login='', password='', sessionid=''):
        self.id = self.identity(id)
        self.firstname = firstname
        self.lastname = lastname
        self.login = login
        self.password = password
        self.sessionid = sessionid

    def __str__(self):
        return self.official_name

    @property
    def official_name(self):
        return '%s %s' % (self.firstname, self.lastname)

    def get_password(self):
        return self.password
