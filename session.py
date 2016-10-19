import hashlib
import random


class Users:
    def __init__(self, user):
        self.userid = None
        self.username = None
        self.sessionid = None

    def user_auth(self, login, password):
        if finduser =.get_user(login):
            self.password_verify(password, finduser[2])
            self.username = finduser[1]
            self.userid = finduser[0]
            return True
        return False

    def check_sessionid(self, sessionid):
        if sessionid == self.sessionid:
            return True
        return False

    def set_sessionid(self):
        salt = generate_salt
        password =
        sessionid = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        return sessionid

    def generate_salt(self):
        salt = ''
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def get_username(self):
        return self.username

    def password_verify(self, password, passwordfromdb):
        if password == passwordfromdb:
            return True
        return False
