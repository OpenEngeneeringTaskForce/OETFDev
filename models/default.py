'''
Created on Aug 18, 2014

Contains all model classes for the default controller

@author: Dean4Devil
'''

from pycore.Base import ModelBase

class Default(ModelBase):
    'Default model'
    def get(self):
        return {}

class About(ModelBase):
    'About model'
    def get(self):
        return {}
