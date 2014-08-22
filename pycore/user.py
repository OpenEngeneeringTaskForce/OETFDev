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
    
    def check_login(self, username, password):
        'Logs the user in. Takes either username or userid or both. If username nor userid is given login() will fail.'
        try:
            tabledata = self.sql_helper.query_one("users", ["id", "password"], "username = '" + username + "'")
            if tabledata == []: # No user with that username
                return False
            table_password = tabledata['password'].decode('utf-8')
            salt = hashlib.sha512(username.encode('utf-8')).hexdigest()[:30]
            hash = hashlib.sha512(salt.encode('utf-8'))
            hash.update(password.encode('utf-8'))
            hash_password = hash.hexdigest()
            if hash_password == table_password: # Login successful
                # Generate an auth hash for that user:
                self.user_auth_hash = hashlib.sha512(os.urandom(256)).hexdigest() # This creates a hash with a collision chance of 1 / 16^128
                self.user_id = tabledata['id']
                self.username = username
                self.sql_helper.insert_data("session", [{'user_id': str(self.user_id), 'user_auth_hash': str(self.user_auth_hash)}])   # Insert new Session data into SessionTable
                self.session.cookie['oetf'] = self.user_auth_hash    # Override the session cookie with the new value
                return True
            return False
        except Exception as e:
            raise Exception("check login raised: " + str(e))
    
    def login(self, user_id):
        try:
            tabledata = self.sql_helper.query_one("users", ["username"], "id = '" + str(user_id) + "'")
            self.user_id = user_id
            self.username = tabledata['username'].decode('utf-8')
        except Exception as e:
            raise Exception("login raised: " + str(e))
    
    def logout(self):
        try:
            self.sql_helper.delete_data("session", "user_auth_hash = '" + self.session.cookie['oetf'].value + "'")
            self.session.cookie['oetf'] = ""
            self.user_id = 0
            self.username = ""
        except Exception as e:
            raise Exception("logout failed: " + str(e))
    
    def get_username(self):
        return self.username
