import os
import sys
from core import db

class UserDao(object):

    def __init__(self):
        pass

    @classmethod
    def authorize(self, user):
        user.password = db.encrypt_passwd(user.password)
        query = "select * from user where name=:name and password=:password"
        result = []
        with db.connection() as connection:
            result = connection.fetch_one(query, vars(user))
            print result
        if result:
            return True
        else:
            return False
         
    def wrap_result(self, result):
        pass

class User(object):

    def __init__(self, *argc):
        pass
