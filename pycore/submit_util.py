'''
Created on Aug 21, 2014

@author: Dean4Devil
'''

import os
import dullwich

from dullwich.repo import Repo

from pycore.sql_util import MySQLHelper

class SubmitHelper:
    'Gets the information for a specific Submit'
    
    def __init__(self, path):
        repo = Repo(path)

class CreateHelper:
    'Creates a new submit'
    
    import re
    
    def __init__(self, title):
        self.sql_helper = MySQLHelper()
        path = re.sub(r'\s', '', title)
        os.mkdir(path)
        repo = Repo.init(path)
        

class UpdateHelper:
    'Updates a existing submit with a new version'
    
    def __init__(self):
        self.sql_helper = MySQLHelper()
