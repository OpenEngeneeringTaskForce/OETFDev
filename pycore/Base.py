'''
Created on Aug 16, 2014

@author: Dean4Devil
'''

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


# Rule of thumb for these classes: If you DON'T overwrite their classes you are probably doing something wrong.
class ControllerBase():
    '''
    Parent class for all controllers.
    While its not necessary to extend this class, it does not hurt and provides useful functions.
    '''
    
    def __init__(self, request, session):
        '''
        Constructor. Setup everything necessary here.
        '''
        self.request = request
        self.session = session
    
    def get(self, model):
        '''
        Responder function for a HTTP GET request for this controllers/model.
        This is the normal behavior for a controllers.
        Returns either a pycore.http_util.Response (if successful)
        or an pycore.http_util.HTTPError (if not)
        '''
    
    def post(self, model):
        '''
        Responder fuction for a HTTP POST request.
        '''


class ModelBase():
    '''
    Parent class for all models.
    While its not necessary to extend this class, it does not hurt and provides useful functions.
    '''
    
    def __init__(self, request, session):
        'Constructor. Setup everything necessary here.'
        self.request = request
        self.session = session
    
    def post(self):
        'POST data to model'
    
    def get(self):
        'GET data from model. Default behavior'


class ViewBase():
    '''
    Parent class for all views.
    While its not necessary to extend this class, it does not hurt and provides useful functions.
    '''
    
    def __init__(self, session):
        'Creates a view object identified by template_name and modified by session'
        self.env = Environment()
        self.env.loader = FileSystemLoader(['views/templates/'])
        self.session_vars = session.finalize_view()
        self.session_vars[self.active] = True   # This will highlight the current page in the sidebar
        # TODO: Get template modifiers from session here (i.e. User object etc.)
    
    def render(self, template_vars={}):
        'Renders the view and returns a string containing the HTML as String'
        template = self.env.get_template(self.template_name)
        template_vars.update(self.session_vars)
        return template.render(template_vars)
