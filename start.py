#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import parse_error_apache


class ApacheDB(object):

    def __init__(self):

        mysql_config = {'user':'apache',
                        'password':'1511256515',
                        'host':'127.0.0.1',
                        'database':'apache_log'}
        apache_conn = mysql.connector.connect(**mysql_config)
        apache_cur = apache_conn.cursor()


    def data_extractor(self, data):
        for lst in data:
            print lst
        
    def give_error_data(self):
        parse_error = parse_error_apache.ApacheLogParser()
        parse_error.parse_data_from_error_file('error_log')
        data = parse_error.lst
        self.data_extractor(data)

    def give_access_data(self):
        pass
        



if __name__ == '__main__':
    start = ApacheDB()
    start.give_error_data()
    #str(raw_input('1.- Error log to db 2.- Acces log to db'
    #              '3.- Show error_db 4.- Show access_db'))