'''
Created on Aug 20, 2014

@author: Dean4Devil
'''

from pycore.Base import ControllerBase
from pycore.http_util import Response, HTTPError, return_redirect_response

class SubmitController(ControllerBase):
    'Controller for posting and listing all avail. submits'
    
    def get(self, model):
        'Gets submits'
        try:
            if model == "list":
                from models.submits import ListSubmit as Model
                from views.submits import ListView as View
                model = Model(self.request, self.session)
                view = View(self.session)
                order = self.request.get_dict.get("sort", [""])[0]
                if order == "alphabet":  # List submits by Alphabe
                    view_args = model.get("Alphabet")
                elif order == "date":        # List submits by submission date
                    view_args = model.get("Date")
                elif order == "tags":         # List submits by tags attached
                    view_args = model.get("Tags")
                else:
                    raise Exception("Not a known sorting!")
                body = view.render(view_args)
                return Response(200, body, self.session)
            if model == "submit_new":
                from models.submits import NewSubmit as Model
                from views.submits import NewSubmitView as View
                model = Model(self.request, self.session)
                view = View(self.session)
                view_args = model.get()
                body = view.render(view_args)
                return Response(200, body, self.session)
            if model == "detail":
                from models.submits import DetailSubmit as Model
                from views.submits import SubmitView as View
                model = Model(self.request, self.session)
                view = View(self.session)
                view_args = model.get()
                body = view.render(view_args)
                return Response(200, body, self.session)
        except HTTPError:
            raise
        except Exception as e:
            raise HTTPError(500, "Controller raised: " + str(e), self.session)
    
    def post(self, model):
        'Posts a new submit'
        try:
            if model == "submit_new":
                from models.submits import NewSubmit as Model
                model = Model(self.request, self.session)
                model.post()
                return return_redirect_response("?r=submits/list;sort=alphabet", self.session)
            if model == "does_exist": # AJAX request if title is already existing
                pass
        except HTTPError:
            raise
        except Exception as e:
            raise HTTPError(500, "Controller raised: " + str(e), self.session)
