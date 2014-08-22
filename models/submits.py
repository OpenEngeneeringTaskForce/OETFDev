'''
Created on Aug 20, 2014

@author: Dean4Devil
'''

from pycore.Base import ModelBase
from pycore.sql_util import MySQLHelper
from pycore.http_util import HTTPError

class ListSubmit(ModelBase):
    'Lists submits by chosen ordering'
    
    order_dict = {"Alphabet": "title", "Date": "published_date", "Tags": ""}
    
    def get(self, order):
        'Get some submits. Order them as asked'
        sql_helper = MySQLHelper()
        return_dict = {'order': order}
        return_dict['page'] = self.request.get_dict.get("page", 1)
        result = sql_helper.query_data("submits", ["title", "version", "publisher_id", "published_date"], order=self.order_dict[order])
        if len(result) > 10:
            return_dict['overflow'] = True
        submits = []
        for row in result:
            submit = {}
            submit['title'] = row['title'].decode('utf-8')
            submit['date'] = row['published_date']
            submit['publisher'] = sql_helper.query_one("users", ["username"], "id = '" + str(row['publisher_id']) + "'")['username'].decode('utf-8')
            submits.append(submit)
        return_dict['submits'] = submits
        return return_dict

class DetailSubmit(ModelBase):
    'Show the details of a submit'

class NewSubmit(ModelBase):
    'Create a new submit'
    
    def get(self):
        return {}
    
    def post(self):
        try:
            self.request.parse_vars()   # Make sure the post vars are parsed
        except Exception as e:
            raise HTTPError(500, "Submitting new paper has failed! " + str(e), self.session)
        return {}
