'''
Created on Aug 16, 2014

@author: Dean4Devil
'''

from urllib.parse import parse_qs, urlparse

def strip_request_uri(urlstring):
    ''' Takes the URL string and splits it into handleable parts '''
    parse_res = urlparse(urlstring)
    return parse_qs(parse_res.query)
