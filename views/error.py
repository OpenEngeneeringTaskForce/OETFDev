'''
Created on Aug 18, 2014

This file contains all views associated with the "default" controller.

@author: Dean4Devil
'''

from pycore.Base import ViewBase

class Error(ViewBase):
    'General error, nothing specific'
    def __init__(self, session):
        self.template_name = "error.tmpl"
        self.active = "error"
        super().__init__(session)

class Error_404(ViewBase):
    'Default View'
    def __init__(self, session):
        self.template_name = "404.tmpl"
        self.active = "error"
        super().__init__(session)
