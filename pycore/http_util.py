'''
Created on Aug 9, 2014

@author: Dean4Devil
'''

import time
import math

import urllib.parse

from http.cookies import SimpleCookie

from pycore.url_util import strip_request_uri
from pycore.user import User
from pycore.sql_util import MySQLHelper

class Request(dict):
    'Request object. Created from environ, this contains shortcuts to useful information like POST vars or cookies'
    
    def __init__(self, environ):
        'Creates a Request object from the environ given by WSGI.'
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.get_dict = strip_request_uri(environ['REQUEST_URI'])
        self.post_vars = None
        self.request_list = self.get_dict.get("r", ["default/default"])[0].split("/")
        if len(self.request_list) == 1:
            self.request_list.append("default")
    
    def parse_vars(self):
        'Parse POST vars into dictionary'
        if self.post_vars == None:
            self.post_vars = urllib.parse.parse_qs(self.environ['wsgi.input'].readline().decode('UTF-8'), True)


class Session(dict):
    'Session object. Contains information on login, user and cookies'
    
    def __init__(self, request):
        'Constructs a Session.'
        self.user = User(self)
        self.cookie = self.get_cookie(request.environ)
    
    def get_cookie(self, environ):
        'Either creates or retrieves the cookie to get persistent session/login'
        if 'HTTP_COOKIE' in environ:    # Client did send a cookie
            cookie = SimpleCookie(environ['HTTP_COOKIE'])
            if 'oetf' in cookie:    # Thats our cookie
                if cookie['oetf'].value != "":  # User could be logged in
                    user_auth_hash = cookie['oetf'].value
                    sql_helper = MySQLHelper()
                    result = sql_helper.query_one("session", ["user_id"], "user_auth_hash = '" + user_auth_hash + "'")
                    if result != []:
                        self.user.login(result['user_id'])
                    else:
                        cookie['oetf'] = ""
                    return cookie
        
        cookie = SimpleCookie()
        cookie['oetf'] = ""
        cookie['oetf']['expires'] = time.strftime("%a, %d %b %Y %H %M %S GMT", time.localtime(math.floor(time.time()) + 63072000 ))
        cookie['oetf']['path'] = "/"
        return cookie
    
    def finalize_view(self):
        'Returns a dictionary containing some more values for the templates'
        return {"username": self.user.get_username(),
                "is_logged_in": True if self.user.user_id != 0 else False }


class Response(dict):
    'Response object. Easier to handle than having to manually send all the headers & stuff'
    
    defined_status = {
        200: 'OK',
        201: 'CREATED',
        202: 'ACCEPTED',
        203: 'NON-AUTHORITATIVE INFORMATION',
        204: 'NO CONTENT',
        205: 'RESET CONTENT',
        206: 'PARTIAL CONTENT',
        301: 'MOVED PERMANENTLY',
        302: 'FOUND',
        303: 'SEE OTHER',
        304: 'NOT MODIFIED',
        305: 'USE PROXY',
        307: 'TEMPORARY REDIRECT',
        400: 'BAD REQUEST',
        401: 'UNAUTHORIZED',
        402: 'PAYMENT REQUIRED',
        403: 'FORBIDDEN',
        404: 'NOT FOUND',
        405: 'METHOD NOT ALLOWED',
        406: 'NOT ACCEPTABLE',
        407: 'PROXY AUTHENTICATION REQUIRED',
        408: 'REQUEST TIMEOUT',
        409: 'CONFLICT',
        410: 'GONE',
        411: 'LENGTH REQUIRED',
        412: 'PRECONDITION FAILED',
        413: 'REQUEST ENTITY TOO LARGE',
        414: 'REQUEST-URI TOO LONG',
        415: 'UNSUPPORTED MEDIA TYPE',
        416: 'REQUESTED RANGE NOT SATISFIABLE',
        417: 'EXPECTATION FAILED',
        422: 'UNPROCESSABLE ENTITY',
        429: 'TOO MANY REQUESTS',
        451: 'UNAVAILABLE FOR LEGAL REASONS', # http://www.451unavailable.org/
        500: 'INTERNAL SERVER ERROR',
        501: 'NOT IMPLEMENTED',
        502: 'BAD GATEWAY',
        503: 'SERVICE UNAVAILABLE',
        504: 'GATEWAY TIMEOUT',
        505: 'HTTP VERSION NOT SUPPORTED',
        509: 'BANDWIDTH LIMIT EXCEEDED',
    }
    
    def __init__(self, status, body, session):
        'Assembles a Response from the ground up.'
        self.headers = []
        self.headers.append(('Content-Type', 'text/html; charset=utf-8'))
        self.headers.append(('X-Powered-By', 'PyPeaches'))
        self.headers.append(('Pragma', 'no-cache'))
        
        if status in self.defined_status:
            self.status = str(status) + " " + self.defined_status[status]
        else:
            self.status = str(status) + " UNKNOWN ERROR"
        self.body = body
        self.session = session
        
        self.set_cookie(session.cookie)
    
    def set_cookie(self, cookie):
        'Adds a cookie to a response'
        cookieheaders = ('Set-Cookie', cookie['oetf'].OutputString())
        self.headers.append(cookieheaders)
    
    def send(self, response_function):
        'Executes the response.'
        
        headers = self.headers
        headers.append(('Content-length', str(sum(len(line) for line in self.body))))
        
        response_function(self.status, headers)
        
        return [ str(self.body).encode('utf_8') ]
    
    def set_custom_header(self, headers):
        'Adds custom headers to the response. headers should be a list of tuples with (name, val)'
        for head in headers:
            self.headers.append(head)


class HTTPError(Exception):
    'HTTP Error. Should get thrown by controllers or models, containing the reason and the http-code of the error.'
    def __init__(self, status, error_message, session, direct=False):
        'Constructs a new HTTPError'
        from views.error import Error as ErrorView
        self.status = status
        error_view = ErrorView(session)
        if direct:
            self.response = Response(status, error_message, session)
        else:
            self.response = Response(status, error_view.render({"error_message": error_message}), session)
    
    def responde(self):
        'Returns an error page'
        return self.response

def return_redirect_response(url, session, absolute=False):
    'Redirects to the given url.'
    if absolute == False:
        url = "http://oetfdev.renet/" + url
    response = Response(303, '', session)
    response.set_custom_header([("Location", url)])
    return response
