import os
import sys
import functools
from dao.user import UserDao

def authorize(user):
    userdao = UserDao()
    return userdao.authorize(user):

