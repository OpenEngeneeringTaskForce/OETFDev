'''
Created on Aug 17, 2014

@author: Dean4Devil
'''
import os
import hashlib

from pycore.sql_util import MySQLHelper

class User():
    '''
    User class. Provides authentication etc.
    '''
    
    def __init__(self, session):
        'User constructor.'
        self.session = session
        self.username = ""
        self.user_id = 0
        self.sql_helper = MySQLHelper()
    
    def login(self, username, password):
        'Logs the user in. Takes either username or userid or both. If username nor userid is given login() will fail.'
        try:
            tabledata = self.sql_helper.query_one("users", ["id", "password"], "username = '" + username + "'")
            if tabledata == []: # No user with that username
                return False
            table_password = tabledata['password'].decode('utf-8')
            hash_password = password    # Make it actually hash the real password
            if password == table_password: # Login successful
                # Generate an auth hash for that user:
                self.user_auth_hash = hashlib.sha512(os.urandom(256)).hexdigest() # This creates a hash with a collision chance of 1 / 16^128
                self.user_id = tabledata['id']
                self.username = username
                self.sql_helper.insert_data("session", [{'user_id': str(self.user_id), 'user_auth_hash': str(self.user_auth_hash)}])   # Insert new Session data into SessionTable
                self.session.cookie = self.user_auth_hash    # Override the session cookie with the new value
                return True
            return False
        except Exception as e:
            raise Exception("login raised: " + str(e))
        
    def get_username(self):
        return self.username
