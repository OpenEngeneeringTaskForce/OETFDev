'''
Created on Aug 18, 2014

User controller file (Login, profile and such)

@author: Dean4Devil
'''

from pycore.Base import ControllerBase
from pycore.http_util import HTTPError, Response, return_redirect_response
from pycore.sql_util import MySQLHelper

class UserController(ControllerBase):
    'User controller providing stuff like login and profile view'
    
    def __init__(self, request, session):
        super().__init__(request, session)
    
    def get(self, model):
        'GET'
        if model == "login":
            # GET on login -> return the login form
            try:
                from models.user import Login as Model
                from views.user import Login as View
                model = Model(self.request, self.session)
                view = View(self.session)
                view_vars = model.get()
                body = view.render(view_vars)
                return Response(200, body, self.session)
            except Exception as e:
                raise HTTPError(500, "Controller raised: " + str(e), self.session)
    
    def post(self, model):
        'POST'
        if model == "login":
            try:
                #POST'ed Login -> check if cred's are valid.
                from models.user import Login as Model
                model = Model(self.request, self.session)
                view_vars = model.post()
                if view_vars['failed']:
                    from views.user import Login as View
                    view = View(self.session)
                    body = view.render(view_vars)
                    return Response(200, body, self.session)
                else:
                    return return_redirect_response("", self.session)
            except Exception as e:
                raise HTTPError(500, "Controller raised: " + str(e), self.session)
