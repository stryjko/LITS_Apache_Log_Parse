#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import parse_error_apache


class ApacheDB(object):

    def __init__(self):

        self.mysql_config = {'user':'apache',
                             'password':'1511256515',
                             'host':'127.0.0.1',
                             'database':'apache_log'}
        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

        
    def give_error_data(self):
        parse_error = parse_error_apache.ApacheLogParser()
        parse_error.parse_data_from_error_file('error_log')
        data = parse_error.lst
        self.insert_error_lst(data)

    def give_access_data(self):
        pass

    def insert_error_lst(self, data):

        for item in data:
            #self.insert_len = ', '.join(['%s'] * len(item))
            dt = item['date']
            msg_t = item['message_type']
            ip = item['ip']
            e_id = item['error_id']
            msg = item['message']

            sql = """INSERT INTO error_log (date, message_type, ip, 
                  error_id, message) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
                  % (dt, msg_t, ip, e_id, msg)
            
            try:
                self.apache_cur.execute(sql)
                self.apache_conn.commit()

            except Error as error:
                print error
            
        self.apache_cur.close()
        self.apache_conn.close()
            


if __name__ == '__main__':
    start = ApacheDB()
    start.give_error_data()
    #str(raw_input('1.- Error log to db 2.- Acces log to db'
    #              '3.- Show error_db 4.- Show access_db'))