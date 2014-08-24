'''
Created on Aug 21, 2014

@author: Dean4Devil
'''

import mysql.connector

from pycore.sql_util import MySQLHelper

class SubmitTree():
    'A tree of all submits to that standard. I.e. OpenDriver is a tree, OpenDriver 0.2 is a submit.'
    
    def __init__(self, identifier):
        'Create a new Tree in memory.'
        self.sql_helper = MySQLHelper("oetf_submits")
        if self.sql_helper.check_exists(identifier):
            self.tree = self.sql_helper.query_data(identifier, "*", delimiter="", order="id", row_num=0)
        else:
            # First submit in that tree. Table does not exist yet.
            table = (
                "CREATE TABLE IF NOT EXISTS `{}` (".format(identifier),
                "`id` int(11) NOT NULL AUTO_INCREMENT,",
                "`version` varchar(32) COLLATE utf8mb4_bin NOT NULL",
                "`comment` text COLLATE utf8mb4_bin NOT NULL,",
                "`content` text COLLATE utf8mb4_bin NOT NULL,",
                "`published_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP",
                "PRIMARY KEY (`id`)",
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1 ;")
            con = self.sql_helper.return_con()
            cur = con.cursor()
            cur.execute(table)
            self.tree = []
            cur.close()
            con.close()

class Submit():
    'Submit element'
