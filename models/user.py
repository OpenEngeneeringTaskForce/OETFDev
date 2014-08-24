'''
Created on Aug 18, 2014

Contains all model classes for the user controller

@author: Dean4Devil
'''

import sys

from pycore.Base import ModelBase
from pycore.http_util import HTTPError

class Login(ModelBase):
    'Login model'
    def get(self):
        return {}
    
    def post(self):
        try:
            self.request.parse_vars()   # post_vars now are a thing
            post_username = self.request.post_vars.get("username")[0]
            post_password = self.request.post_vars.get("password")[0]
            if self.session.user.check_login(post_username, post_password):
                return {'failed': False}
            else:
                return {'failed': True}
        except Exception as e:
            raise HTTPError(500, "Model raised: " + str(e), self.session, True) # Return a general error

class Profile(ModelBase):
    'Profile model'
    def get(self):
        return {"path": str(sys.path)}

class Register(ModelBase):
    'Register model'
    def get(self):
        try:
            from pycore.sql_util import MySQLHelper
            sql_helper = MySQLHelper()
            key = self.request.get_dict.get("key", [""])[0]
            res = sql_helper.query_one("register", "key", "key == '" + key + "'")
            if res == []:
                raise HTTPError(403, "You are not allowed to do this.")
            else:
                return {}
        except HTTPError:
            raise
        except Exception as e:
            raise HTTPError(500, str(e), self.session)
    
    def post(self):
        try:
            from pycore.sql_util import MySQLHelper
            sql_helper = MySQLHelper()
            key = self.request.get_dict.get("key", [""])[0]
            res = sql_helper.query_one("register", "key", "key == '" + key + "'")
            if res == []:
                raise HTTPError(403, "You are not allowed to do this.")
            else:
                self.request.parse_vars()   # post_vars now are a thing
                try:
                    import hashlib
                    post_username = self.request.post_vars.get("username")[0]
                    post_email = self.request.post_vars.get("email")[0]
                    post_password = self.request.post_vars.get("password")[0]
                    salt = hashlib.sha512(post_username.encode('utf-8')).hexdigest()[:30]
                    hash = hashlib.sha512(salt.encode('utf-8'))
                    hash.update(post_password.encode('utf-8'))
                    hash_password = hash.hexdigest()
                    sql_helper.insert_data("users", [{"username": post_username, "email": post_email, "password": hash_password}])
                except Exception as e:
                    return {"failed": True, "f_reason": str(e)}
        except HTTPError:
            raise
        
