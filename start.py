#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import parse_error_apache
import sys
from os import system


class ApacheDB(object):

    def __init__(self):

        self.mysql_config = {'user':'apache',
                             'password':'1511256515',
                             'host':'127.0.0.1',
                             'database':'apache_log'}
        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

    def start_program(self):
        system('clear')
        print """ --- Apache logs parser --- \n
1. Add error log to DB
2. Add access log to DB
3. View error log
4. View access log\n
9. Exit"""

        choice = str(raw_input('Enter your choice: '))

        if choice == '1':
            self.give_error_data()
        elif choice == '2':
            self.give_access_data()
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '9':
            sys.exit()

        
    def give_error_data(self):
        parse_error = parse_error_apache.ApacheLogParser()
        parse_error.parse_data_from_error_file('error_log')
        data = parse_error.lst
        self.insert_error_lst(data)

    def give_access_data(self):
        pass

    def insert_error_lst(self, data):

        for item in data:
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

    def insert_access_lst(self, data):
        pass
            


if __name__ == '__main__':
    start = ApacheDB()
    start.start_program()
    