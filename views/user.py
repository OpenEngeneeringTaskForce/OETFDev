'''
Created on Aug 18, 2014

This file contains all views associated with the "user" controller.

@author: Dean4Devil
'''

import random

from pycore.Base import ViewBase

class Login(ViewBase):
    'Login View'
    failed_list = ["Even MySQL thinks you are stupid!", 
                   "Wrong Username or Password you moron!", 
                   "If you are trying to hack this page, YOU ARE DOING IT WRONG!", 
                   "Try again Idiot!", 
                   "Thats not your password! Is that even your account??",
                   "Oh no, not YOU again....",
                   "Stahp! You are hurting meeeee! :<",
                   "You're gonna be my new meat bicycle!!",
                   "Short update: LOGIN FAILED!",
                   "THIS IS UNACCEPTABLE!!!",
                   "Looks like a tyop.",
                   "42 is not the answer here, nor is it the password, or even username, if it is... <a href='https://xkcd.com/936/'>https://xkcd.com/936/</a>"]


    def __init__(self, session):
        self.template_name = "login.tmpl"
        self.active = "login"
        super().__init__(session)
    
    def render(self, template_vars={}):
        # If login failed, answer with a random insult 
        if template_vars.get('failed', False):
            template_vars.update({'f_reason': self.failed_list[random.randrange(0, len(self.failed_list))]})
        return ViewBase.render(self, template_vars)

class Profile(ViewBase):
    'Profile View'
    def __init__(self, session):
        self.template_name = "profile.tmpl"
        self.active = "profile"
        super().__init__(session)

class Register(ViewBase):
    'Register View'
    def __init__(self, session):
        self.template_name = "register.tmpl"
        super().__init__(session)
