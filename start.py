#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yuriy K.'

import mysql.connector
from mysql.connector import Error
import parse_error_apache
import sys
from os import system
from time import sleep


class ApacheDB(object):

    def __init__(self):

        self.mysql_config = {'user':'apache',
                             'password':'1511256515',
                             'host':'127.0.0.1',
                             'database':'apache_log'}

        self.errors = []

    def start_program(self):
        system('clear')
        print """ --- Apache logs parser --- \n
  1. Add error log to DB
  2. Add access log to DB
  3. View error log
  4. View access log\n
  5. Delete all data from error log
  6. Delete all data from access log\n
  9. Exit\n"""

        choice = str(raw_input('Enter your choice: '))

        if choice == '1':
            self.give_error_data()
        elif choice == '2':
            self.give_access_data()
        elif choice == '3':
            self.select_all('error')
        elif choice == '4':
            self.select_all('access')
        elif choice == '5':
            self.delete_data('error')
        elif choice == '6':
            self.delete_data('access')
        elif choice == '9':
            system('clear')
            print 'Bye'
            sleep(2)
            sys.exit()

        
    def give_error_data(self):
        parse_error = parse_error_apache.ApacheLogParser()
        parse_error.parse_data_from_error_file('error_log')
        data = parse_error.lst
        self.insert_error_lst(data)

    def give_access_data(self):
        parse_acces = parse_error_apache.ApacheLogParser()
        parse_acces.parse_data_from_error_file('access_log')
        data = parse_acces.lst
        self.insert_access_lst(data)

    def insert_error_lst(self, data):

        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

        for item in data:
            dt = item['date']
            ip = item['ip']
            e_id = item['error_id']

            if type(item['message']) == list:
                msg = item['message']
                print 'list'
            else:
                print 'str'
                msg = []
                msg.append(item['message'])
            print msg

            if item['message_type'] == ['statistics']:
                msg_t = item['message_type'][0]
            else:
                msg_t = item['message_type']

            sql = """INSERT INTO error_log (date, message_type, 
                  ip, error_id, message) VALUES ('%s', '%s', 
                  '%s', '%s', '%s')""" % (dt, msg_t, ip, e_id, msg[0])
            
            try:
                self.apache_cur.execute(sql)
                self.apache_conn.commit()

            except Error as error:
                self.errors.append(error)

        if self.errors:
            #system('clear')
            print 'We have there some errors: \n'

            for error in self.errors:
                print error, '\n'

            choice = str(raw_input('Continue? (yes/no): '))

            if choice == 'yes':
                self.start_program()
            elif choice == 'no':
                print 'Bye!'
                sleep(2)
                sys.exit()
    
        self.apache_cur.close()
        self.apache_conn.close()
        system('clear')
        print 'Data added!'
        sleep(2)
        self.start_program()

    def insert_access_lst(self, data):

        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

        for item in data:
            hp = item['http_port']
            ip = item['ip']
            hrp = item['http_request_protocol']
            hru = item['http_request_url']
            dt = item['date']
            hrt = item['http_request_type']
            hr = item['http_response']

            sql = """INSERT INTO access_log (date, ip, http_port, 
                    http_request_type, http_request_protocol,
                    http_request_url, http_response) VALUES ('%s', 
                    '%s', '%s', '%s', '%s', '%s', '%s')""" \
                    % (dt, ip, hp, hrt, hrp, hru, hr)
            try:
                self.apache_cur.execute(sql)
                self.apache_conn.commit()

            except Error as error:
                self.errors.append(error)

        if self.errors:
            system('clear')
            print 'We have there some errors: \n'

            for error in self.errors:
                print error, '\n'

            choice = str(raw_input('Continue? (yes/no): '))

            if choice == 'yes':
                self.start_program()
            elif choice == 'no':
                print 'Bye!'
                sleep(2)
                sys.exit()
            
        self.apache_cur.close()
        self.apache_conn.close()
        system('clear')
        print 'Data added!'
        sleep(2)
        self.start_program()


    def select_all(self, table):

        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

        if table == 'error':
            sql = """SELECT * FROM error_log """
        elif table == 'access':
            sql = """SELECT * FROM access_log """

        self.apache_cur.execute(sql)
        rows = self.apache_cur.fetchall()
        sys.stdout.write("\x1b[8;25;120t") #resize terminal

        for row in rows:
            a = '| ' + row[0] + ' | ' + row[1] + ' | ' + row[2] \
                 + ' | ' + row[3] + ' | ' + row[4] + ' |'
            print a
            print '-'*len(a)

        self.apache_cur.close()
        self.apache_conn.close()

        choice = str(raw_input('Open menu? (yes/no): '))

        if choice == 'yes':
            self.start_program()
        elif choice == 'no':
            sys.exit()


    def delete_data(self, table):

        self.apache_conn = mysql.connector.connect(**self.mysql_config)
        self.apache_cur = self.apache_conn.cursor()

        if table == 'error':
            sql = """TRUNCATE error_log"""
        elif table == 'access':
            sql = """TRUNCATE access_log"""

        choice = str(raw_input('Are you sure? (yes/no)'))
        if choice == 'yes':
            self.apache_cur.execute(sql)
            self.apache_conn.commit()
            self.apache_cur.close()
            self.apache_conn.close()
            system('clear')
            print 'Data deleted!'
            sleep(2)
            self.start_program()
        else:
            system('clear')
            self.start_program()




if __name__ == '__main__':
    start = ApacheDB()
    start.start_program()
    