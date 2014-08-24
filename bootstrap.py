#/bin/python3github.com/FSX/misaka
# -*- coding: utf-8
'''
Created on Aug 18, 2014

@author: Dean4Devil
'''

import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

from pycore.http_util import Request, Response, Session, HTTPError
from views.error import Error_404

def application(environ, responder):
    'The WSGI entry hook'
    
    # Create a request out of environ
    request = Request(environ)
    
    # Same for a session
    session = Session(request)
    
    try:
        return dynamify(request, session).send(responder) # Takes the Response object returned by dynamify and returnes the body (headers is handled by function internally)
    except AttributeError:
        error_view = Error_404(session)
        return HTTPError(404, error_view.render(), session, direct=True).responde().send()
    except Exception as e:
        return HTTPError(500, str(e), session).responde().send()

def dynamify(request, session):
    'Tried to dynamify the Webpage and returns it. If fail, fail'
    try:
        req_method = request.environ['REQUEST_METHOD']
        if request.request_list[0] == "default":
            from controllers.default import Default
            controller = Default(request, session)
            if req_method == "GET":
                return controller.get(request.request_list[1])
        if request.request_list[0] == "user":
            from controllers.user import UserController
            controller = UserController(request, session)
            if req_method == "GET":
                return controller.get(request.request_list[1])
            if req_method == "POST":
                return controller.post(request.request_list[1])
        if request.request_list[0] == "submits":
            from controllers.submits import SubmitController
            controller = SubmitController(request, session)
            if req_method == "GET":
                return controller.get(request.request_list[1])
            if req_method == "POST":
                return controller.post(request.request_list[1])
        
        # Nothing was returned. Make it a 404' for good measure
        error_view = Error_404(session)
        raise HTTPError(404, error_view.render(), session, direct=True)
    except HTTPError as error:
        return error.responde()
    # If something is NOT an HTTPError, raise into apache's error.log
