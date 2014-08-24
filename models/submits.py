'''
Created on Aug 20, 2014

@author: Dean4Devil
'''

import hashlib

import mistune

from pycore.Base import ModelBase
from pycore.sql_util import MySQLHelper
from pycore.http_util import HTTPError

class ListSubmit(ModelBase):
    'Lists submits by chosen ordering'
    
    order_dict = {"Alphabet": "title", "Date": "date", "Tags": "title"}
    order_desc = {"Alphabet": False, "Date": True, "Tags": True}
    
    def get(self, order):
        'Get some submits. Order them as asked'
        sql_helper = MySQLHelper()
        submit_helper = MySQLHelper("submits")
        return_dict = {'order': order}
        return_dict['page'] = self.request.get_dict.get("page", 1)
        submits = sql_helper.query_data("submits", ["title", "description", "identifier", "publisher_id"])
        result = []
        for submit in submits:
            submit_data = submit_helper.query_one(submit['identifier'].decode('utf-8'), ["version", "comment", "published_date"], order="`id` DESC")
            submit.update(submit_data) # submit contains title description, identifier, publisher_id, version, comment, published_date
            result.append(submit)
        if len(result) > 10:
            return_dict['overflow'] = True
        submits = []
        for row in result:
            submit = {}
            submit['title'] = row['title'].decode('utf-8')
            submit['description'] = row['description'].decode('utf-8')
            submit['version'] = row['version'].decode('utf-8')
            submit['date'] = row['published_date']
            submit['publisher'] = sql_helper.query_one("users", ["username"], "id = '" + str(row['publisher_id']) + "'")['username'].decode('utf-8')
            submit['id'] = row['identifier'].decode('utf-8')
            submits.append(submit)
        return_dict['submits'] = sorted(submits, key=lambda submit: submit[self.order_dict[order]], reverse=self.order_desc[order])
        return return_dict

class DetailSubmit(ModelBase):
    'Show the details of a submit'
    def get(self):
        'Return a detailed form of the submit.'
        identifier = self.request.get_dict.get("id", [""])[0]
        if identifier == "":
            raise Exception("Nothing to show.")
        submit_helper = MySQLHelper('submits')
        submits = submit_helper.query_data(identifier, ["version", "comment", "content", "published_date"], order="`published_date` DESC")
        sql_helper = MySQLHelper()
        std_data = sql_helper.query_one("submits", ["title", "publisher_id"], "`identifier` = '" + identifier + "'")
        username = sql_helper.query_one("users", ["username"], "`id` = '" + str(std_data['publisher_id']) + "'")['username']
        version = self.request.get_dict.get("version", [""])[0]
        if version == "":
            submit = submits[0]
            submit['version'] = submit['version'].decode('utf-8')
            submit['title'] = std_data['title'].decode('utf-8')
            submit['comment'] = submit['comment'].decode('utf-8')
            submit['content'] = mistune.markdown(submit['content'].decode('utf-8'), escape=True)
            submit['publisher_name'] = username.decode('utf-8')
            if len(submits) > 1:
                submit['older'] = submits[1]['version'].decode('utf-8')
            return submit
        else:
            i = 0
            for row in submits:
                if row['version'] == version:
                    submit = row
                    submit['title'] = std_data['title'].decode('utf-8')
                    submit['publisher_name'] = username.decode('utf-8')
                    if i == 0:
                        submit['older'] = submits[1]['version'].decode('utf-8')
                    elif i == len(submits):
                        submit['newer'] = submits[i-1]['version'].decode('utf-8')
                    else:
                        submit['older'] = submits[i+1]['version'].decode('utf-8')
                        submit['newer'] = submits[i-1]['version'].decode('utf-8')
                    return submit
                i += 1
        raise Exception("Something went wrong!")

class NewSubmit(ModelBase):
    'Create a new submit'
    
    def get(self):
        return {}
    
    def post(self):
        try:
            self.request.parse_vars()   # Make sure the post vars are parsed
            title = self.request.post_vars.get("title")[0]
            version = self.request.post_vars.get("version")[0]
            description = self.request.post_vars.get("description")[0]
            content = self.request.post_vars.get("content")[0]
            publisher_id = self.session.user.user_id
            identifier = hashlib.sha1(title.encode('utf-8')).hexdigest()
            sql_helper = MySQLHelper()
            sql_helper.insert_data("submits", [{"title": title, "description": description, "identifier": identifier, "publisher_id": publisher_id}]) # Now we have that submit stored in the table.
            submit_helper = MySQLHelper('submits')
            from contextlib import closing
            with closing(submit_helper.return_con()) as con:
                cur = con.cursor()
                cur.execute(
                "CREATE TABLE IF NOT EXISTS `{}` (".format(identifier) +
                "`id` int(11) NOT NULL AUTO_INCREMENT," +
                "`version` varchar(32) COLLATE utf8mb4_bin NOT NULL," +
                "`comment` text COLLATE utf8mb4_bin NOT NULL," +
                "`content` text COLLATE utf8mb4_bin NOT NULL," +
                "`published_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "PRIMARY KEY (`id`)" +
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1 ;")
                cur.close()
            submit_helper.insert_data(identifier, [{"version": version, "comment": description, "content": content}])
        except Exception as e:
            raise HTTPError(500, "Submitting new paper has failed! " + str(e), self.session)
        return {}

def ajax_does_exists():
    'Does return a JSON object stating if that table name already exists'