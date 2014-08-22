'''
Created on Aug 21, 2014

@author: Dean4Devil
'''

from pycore.Base import ViewBase

class ListView(ViewBase):
    'Profile view. Nothing special here either.'
    
    def __init__(self, session):
        self.template_name = "list_submits.tmpl" # Link to the filename of the template you want to use. NOT PATH
        self.active = "list" # This will highlight the link in the sidebar
        super().__init__(session)

class SubmitView(ViewBase):
    'Shows a single submit with all the features of it.'
    
    def __init__(self, session):
        self.template_name = "detail_submit.tmpl"
        self.active = "list"
        super().__init__(session)

class NewSubmitView(ViewBase):
    'Form to post a new submit or add to an existing standard.'
    def __init__(self, session):
        self.template_name = "new_submit.tmpl"
        self.active = "submit"
        super().__init__(session)
