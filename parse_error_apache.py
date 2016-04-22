__author__ = 'maryan'

import re

DATA_RE = re.compile('\[(.*?)\]')
MESSAGE_RE = re.compile('.*[\]|\:] (.+)')
TYPE_MESSAGE_RE = re.compile('.*\] (.*)\:')


class ApacheLogParser():

    def __init__(self):
        self.res_dict = {}
        self.lst = []

    def main(self, file_type):
        if file_type == '/home/stryjko/Downloads/error_log':
            self.parse_data_from_error_file(file_type)
        else:
            self.parse_data_from_access_file(file_type)

    def parse_data_from_error_file(self, file_name):
        # read data from file
        with open(file_name) as f:
            lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue

            self.res_dict = {
                'date': re.findall(DATA_RE, line.strip())[0],
                'type_message': re.findall(DATA_RE, line.strip())[1] 
                if len(re.findall(DATA_RE, line.strip())) > 1 else re.findall(TYPE_MESSAGE_RE, line.strip()),
                'ip': re.findall(DATA_RE, line.strip())[2].replace('client', '').strip() 
                if len(re.findall(DATA_RE, line.strip())) > 2 else None,
                'message': re.findall(MESSAGE_RE, line.strip())[0]
            }
            self.lst.append(self.res_dict)
        print self.lst

    def parse_data_from_access_file(self, file_name):
    	pass

if __name__ == "__main__":
    ApacheLogParser().main('/home/stryjko/Downloads/error_log')
