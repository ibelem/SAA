# -*- coding: utf-8 -*-
import os,sys
import threading
from win32api import *
import subprocess

PROJECTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
DAVINCIPATH = 'C:/Intel/BiTS/DaVinci/'
TESTPATH = os.path.join(PROJECTPATH,'tests')


def main():
    cmd = DAVINCIPATH + 'Scripts/run.bat ' + DAVINCIPATH + 'bin ' + TESTPATH
    #p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    #stdout, stderr = p.communicate()
    #print p.returncode # is 0 if success
    t = MyThread(cmd)
    t.start()

class MyThread(threading.Thread):
    def __init__(self, batpath, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.batpath = batpath
    def run(self):
        ShellExecute(0, None, self.batpath, None, "c:\\", True)

if __name__ == '__main__':
    sys.exit(main())