#-*-coding:utf-8-*-
from dao.user import UserDao, User
from bottle import request, redirect

##########################################################
#                    user operation module               #    
##########################################################

def wrap_user(attrs):
    user = User()
    for attr, value in attrs.items():
        setattr(user, attr, value)
    return user

def authorize_user():
    try:
        name, password = unicode(request.forms.get("name"), "utf-8"), request.forms.get("password")
        attrs = {"name":name, "password":password}
        user = wrap_user(attrs)
        userDao = UserDao()
        if userDao.authorize(user):
            redirect("/main")
        else:
            return {"message":"User or Password error"}
    except TypeError:
        return {"message":"User or Password error"}
