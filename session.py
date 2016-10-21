import hashlib
import random
from settings import database
from parse import *

class Session:
    def __init__(self, request):
        self.request = request

    def auth(self):
        post = self.getpost()
        sessionid = self.login(post)
        return sessionid

    def getpost(self):
        post = query_parser(self.request.get_body())
        return post

    def login(self, post):
        for user in database:
            try:
                if user.find_field_value('login', post['username']):
                    if user['password'] == post['password']:
                        sessionid = self.generate_session(post['password'])
                        user.set_attribute('sessionid', sessionid)
                        return (sessionid)
                    return ("Ваши логин или пароль не соответствуют.")
            except AttributeError:
                return False
        return False

    def logout(self):
        pass

    def find_session(self):
        for user in database:
            try:
                if user.find_field_value('sessionid', self.request.get_cookie()):
                    return user
            except AttributeError:
                return False
        return False

    def generate_session(self, password):
        salt = self.generate_salt
        sessionid = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        return sessionid

    def generate_salt(self):
        salt = ''
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt