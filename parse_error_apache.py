__author__ = 'maryan'

import re
from datetime import datetime

DATA_RE = re.compile('\[(.*?)\]')
MESSAGE_RE = re.compile('.*\]\s(.+)')
ADD_MESSAGE_RE = re.compile('\(\d+\)(.+)')
TYPE_MESSAGE_RE = re.compile('.*\]\s(.*)\:')
ERROR_ID = re.compile('.*\]\s\((\d+)\)')
ACCESS_IP_RE = re.compile('(.+?)\s-\s-\s\[')
ACCESS_TIME_RE = re.compile('\[(.+?)\]')
ACCESS_REQUEST_RE = re.compile('.*\]\s\"(.+)\"')
ACCESS_RESPONSE_RE = re.compile('.*\".+\"\s(\d+)')
ACCESS_PORT_RE = re.compile('.*\".+\"\s\d+\s(\d+)')


class ApacheLogParser():

    def __init__(self):
        self.res_dict = {}
        self.lst = []

    def parse_data_from_error_file(self, file_name):
        # read data from file
        with open(file_name) as f:
            lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue

            if file_name == 'error_log':
                date = re.findall(DATA_RE, line.strip())[0]
                date = ' '.join(date.split(' ')[1:])
                self.res_dict = {
                    'date': str(datetime.strptime(date, '%b  %d %H:%M:%S %Y')),
                    'message_type': re.findall(DATA_RE, line.strip())[1] 
                    if len(re.findall(DATA_RE, line.strip())) > 1 else re.findall(TYPE_MESSAGE_RE, line.strip()),
                    'ip': re.findall(DATA_RE, line.strip())[2].replace('client', '').strip() 
                    if len(re.findall(DATA_RE, line.strip())) > 2 else 'None',
                    'message': re.findall(ADD_MESSAGE_RE, re.findall(MESSAGE_RE, line.strip())[0]) 
                    if re.findall(ERROR_ID, line.strip()) else re.findall(MESSAGE_RE, line.strip())[0],
                    'error_id': re.findall(ERROR_ID, line.strip())[0] if re.findall(ERROR_ID, line.strip()) else 'None'
                }
            else:
                date = re.findall(ACCESS_TIME_RE, line.strip())[0].split('-')[0].strip()
                self.res_dict = {
                    'ip': re.findall(ACCESS_IP_RE, line.strip())[0],
                    'date': str(datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')),
                    'http_request_type': 'None' 
                    if re.findall(ACCESS_REQUEST_RE, line.strip())[0] == '-' else re.findall(ACCESS_REQUEST_RE, line.strip())[0].split(' ')[0],
                    'http_request_url': 'None' 
                    if re.findall(ACCESS_REQUEST_RE, line.strip())[0] == '-' else re.findall(ACCESS_REQUEST_RE, line.strip())[0].split(' ')[1],
                    'http_request_protocol': 'None' 
                    if re.findall(ACCESS_REQUEST_RE, line.strip())[0] == '-' else re.findall(ACCESS_REQUEST_RE, line.strip())[0].split(' ')[2],
                    'http_response': re.findall(ACCESS_RESPONSE_RE, line.strip())[0],
                    'http_port': re.findall(ACCESS_PORT_RE, line.strip())[0] if re.findall(ACCESS_PORT_RE, line.strip()) else 'None'
                }
            self.lst.append(self.res_dict)