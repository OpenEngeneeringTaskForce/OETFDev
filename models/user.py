'''
Created on Aug 18, 2014

Contains all model classes for the user controller

@author: Dean4Devil
'''

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
            if self.session.user.login(post_username, post_password):
                return {'failed': False}
            else:
                return {'failed': True}
        except Exception as e:
            raise HTTPError(500, "Model raised: " + str(e), self.session) # Return a general error

class Profile(ModelBase):
    'Profile model'
    def get(self):
        return {}
