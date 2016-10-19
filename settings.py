import os
from dal import GetData
database=GetData()
SERVER_NAME = b'BlogServer/0.1'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')
