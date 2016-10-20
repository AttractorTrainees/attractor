import hashlib
import random


class Users:
    def __init__(self, user):
        self.user_id = None
        self.user_name = None
        self.session_id = None

    def user_auth(self, login, password):
        if user == get_user(login):
            self.password_verify(password, user[2])
            self.user_name = user[1]
            self.user_id = user[0]
            return True
        return False

    def check_sessionid(self, session_id):
        if session_id == self.session_id:
            return True
        return False

    def set_session_id(self):
        salt = generate_salt
        password = ''
        session_id = hashlib.sha1((salt + password).encode('utf-8')).hexdigest()
        return session_id

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
