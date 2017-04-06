# -*- coding:utf-8 -*-
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.conf import settings as django_settings

'''
  security_key就是settings.py中设置的SECRET_KEY，salt是经过base64加密的SECRET_KEY， 
  generate_validate_token 函数通过URLSafeTimedSerializer在用户注册时生成一个令牌。
  用户名在令牌中被编了码。生成令牌之后，会将带有token的验证链接发送到注册邮箱。
  在confirm_validate_token 函数中，只要令牌没过期，那它就会返回一个用户名，过期时间为3600秒。
  remove_validate_token 函数中，无论令牌过不过期，都会返回一个用户名，用于删除user。
'''


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print serializer.loads(token, salt=self.salt)
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)    # 定义为全局变量