import hashlib
import random
from settings import database


def is_login(request):
    for user in database:
        try:
            if user.find_field_value('sessionid',request.get_cookie()):
                return user
        except AttributeError:
            return None
    return None



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
