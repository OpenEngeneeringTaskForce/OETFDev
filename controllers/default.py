'''
Created on Aug 18, 2014

Default controller file

@author: Dean4Devil
'''

from pycore.Base import ControllerBase
from pycore.http_util import HTTPError, Response

class Default(ControllerBase):
    'Default controller'
    # I don't need anything special, so no other __init__ than already defined in ControllerBase
    
    def get(self, model):
        'GET data from model'
        if model == "default":
            # Return the default page
            try:
                from models.default import Default as Model
                from views.default import Default as View
                model = Model(self.request, self.session)
                view = View(self.session)
                view_vars = model.get() # {}
                
                body = view.render(view_vars) # <- NoneType object is not iterable
                
                return Response(200, body, self.session)
            except Exception as e:
                raise HTTPError(500, "Controller raised: " + str(e), self.session)
        if model == "about":
            # Return the about page
            try:
                from models.default import About as Model
                from views.default import About as View
                model = Model(self.request, self.session)
                view = View(self.session)
                template_vars = model.get()
                body = view.render(template_vars)
                return Response(200, body, self.session)
            except Exception as e:
                raise HTTPError(500, "Controller raised: " + str(e), self.session)
