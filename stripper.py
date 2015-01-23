# -*- coding:utf-8 -*-
#!/usr/bin/env python

import sys
import os
import re

# Remove Copyright comments in html page for W3C upstream
# HTML files root folder, html files in it's folder and subfolders will be stripped
w3c_tc_path = '/home/belem/github/SAA'
html_path = ''  #The path of html file which will be stripped

class FileStripper():
    # def __init__(self):
    # print self
    def html_traversal(self, path):
        # Traversal all files under w3c_tc_path folder and subfolders
        for root, dirs, files in os.walk(path):
                for fn in files:
                    if fn.split('.')[-1].find('py') >= 0:
                        if fn.split('.')[0].find('stripper') < 0:
                            html_path = root + '/' + fn
                            print 'Stripped: ', html_path
                            fs = FileStripper()
                            fs.strip_copyright(html_path)

    def strip_copyright(self, path):
        if not os.path.exists(path):
            print 'Error: py file - %s doesn\'t exist.' % path
        try:
            f = open(path)
            file_string = f.read()
            f.close()

            pattern = '# Copyright.*?com>'
            new_file_string = re.sub(re.compile(pattern, re.DOTALL), '', file_string)

            # Combine multiple empty lines into one empty line
            new_file_string = re.sub(re.compile('^[\r\n]+$', re.MULTILINE), '', new_file_string)

            f = open(path, 'w')
            f.write(new_file_string)
            f.close()

            # print new_file_string
            print 'Copyright comments were stripped successfully: ', path,'\r\n'

        except Exception, e:
            print str(e), path, '\r\n'

if __name__ == '__main__':
    fs = FileStripper()
    fs.html_traversal(w3c_tc_path)
