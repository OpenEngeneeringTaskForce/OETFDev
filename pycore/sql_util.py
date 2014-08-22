'''
Created on Aug 17, 2014

@author: Dean4Devil
'''

import mysql.connector
import configparser

from contextlib import closing
from builtins import int

configp = configparser.ConfigParser()
configp.read('config/mysql.conf')
config = dict(configp['MySQL'])

class MySQLHelper():
    'SQL Bindings'
    
    def query_data(self, table, selection, delimiter="", order="", row_num=0):
        '''
        Querys data with the information given:
        table should be a string containing the table name
        selection should be a list containing the names of the columns
        delimiter should be a string (i.e. " user_id = 0 AND username = '' ")
        row_num is the limit of results queried. 0 means all.
        '''
        if isinstance(row_num, int) and row_num < 0:
            raise OutOfBoundsException("Row number can't be negative!")
        select_string = ", ".join(selection) # If selection is only one element (i.e. "*") join() will do nothing
        if delimiter != "":
            delimiter = " WHERE " + delimiter
        if order != "":
            order = " ORDER BY " + order
        with closing(mysql.connector.connect(**config)) as con: # MySQL Connection gets automatically closed as soon as its no longer needed.
            result = []
            cur = con.cursor(dictionary=True) # Create a new dictionaried cursor. This will return rows formated as dicts (key=rowname, value=rowcontent)
            if row_num == 0: # Get all rows
                cur.execute("SELECT " + select_string + " FROM " + table + delimiter + order)
                for row in cur: # BTW: A cursor is an Iterable! Who would have guessed that!
                    result.append(row)
            else: # Get selected amount of rows
                cur.execute("SELECT " + select_string + " FROM " + table + delimiter + order + " LIMIT " + str(row_num))
                row = cur.fetchone()
                for _ in range(row_num):    # Query the cursor until either the limit is reached or no more results are available.
                    if row == None: break   # If row == None, the cursor is empty. 
                    result.append(row)
                    row = cur.fetchone()    # Refresh row with new row content
            cur.close()
            return result   # Return a list of 1 or more elements.
    
    def query_one(self, table, selection, delimiter="", order=""):   # Shortcut function, returns single element instead of list with one member
        result = self.query_data(table, selection, delimiter, order, 1)
        if result == []:
            return result
        return result[0]
    
    def delete_data(self, table, delimiter):
        with closing(mysql.connector.connect(**config)) as con: # MySQL Connection gets automatically closed as soon as its no longer needed.
            cur = con.cursor()
            cur.execute("DELETE FROM " + table + " WHERE " + delimiter)
            cur.close()
    
    def insert_data(self, table, insert_data):
        '''
        Insert the given data into the given table.
        table should be a string of the table name.
        insert_data should be a list of dictionaries of the format: [{column_name: to_be_inserted}]
        '''
        # insert_data = [{a:b, c:d}]
        with closing(mysql.connector.connect(**config)) as con: # MySQL Connection gets automatically closed as soon as its no longer needed.
            cur = con.cursor()
            for column_dict in insert_data:
                key_list = []
                val_list = []
                val_plhd = []
                for k, v in column_dict.items():    # For every value in the list of dicts one INSERT statement will be done
                    key_list.append(str(k))
                    val_list.append(str(v))
                    val_plhd.append("%s")
                cur.execute("INSERT INTO " + table + " ( " + ", ".join(key_list) + " ) VALUES ( " + ", ".join(val_plhd) + " )", val_list)
            con.commit()    # Execute all the statements
            cur.close()     # We're done here


class OutOfBoundsException(ValueError):
    'Raised if numeral values are out of the possible bounds'
