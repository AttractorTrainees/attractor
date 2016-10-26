import hashlib
import random
import string

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
        login = post[b'username'].decode()
        password = post[b'password'].decode()
        for user in database.get_all_users():
            try:
                if user.find_field_value('login', login):
                    if password == user.get_password():
                        sessionid = self.generate_session(password)
                        user.set_attribute('sessionid', sessionid)
                        return sessionid
                    return False
            except AttributeError:
                return False
        return False

    def logout(self):
        pass

    def find_session(self):
        for user in database.get_all_users():
            try:
                if user.find_field_value('sessionid', self.request.get_cookie()):
                    return user
            except AttributeError:
                continue
        return None

    def generate_session(self, password):
        salt = self.generate_salt()
        sessionid = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        return sessionid

    def generate_salt(self):
        salt = ''
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt
