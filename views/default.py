'''
Created on Aug 18, 2014

This file contains all views associated with the "default" controller.

@author: Dean4Devil
'''

from pycore.Base import ViewBase

class Default(ViewBase):
    'Default View'
    def __init__(self, session):
        self.template_name = "default.tmpl" # Link to the filename of the template you want to use. NOT PATH
        self.active = "default" # This will highlight the link in the sidebar
        super().__init__(session) # Yeah, it DOES make a difference where you put the super(), so WATCH OUT!

class About(ViewBase):
    'About View'
    def __init__(self, session):
        self.template_name = "about.tmpl"
        self.active = "about"
        super().__init__(session)
