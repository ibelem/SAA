# -*- coding: utf-8 -*-
import os,sys
import threading
#from win32api import *
import subprocess
import common

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
DAVINCIPATH = 'C:/Intel/BiTS/DaVinci/'
TESTPATH = os.path.join(SUITEPATH,'tests')

def clear_davinci_test():
    print '===== Clean up files in test suite path and apk test path ====='
    try:
        for i in ['.qs','.xml','.txt']:
            common.del_files(TESTPATH, i)
            print '===== Delete file: ' + '*' + i + ' in ' + TESTPATH + ' ====='
        for j in ['.txt','.log']:
            common.del_files(SUITEPATH, j)
            print '===== Delete file: ' + '*' + j + ' in ' + SUITEPATH + ' ====='
        common.del_folder(os.path.join(TESTPATH, '_DaVinci_RnR_Logs'))
        print '===== Delete folder: ' + os.path.join(TESTPATH, '_DaVinci_RnR_Logs') + ' ====='
    except Exception, ex:
        print ex,'\n##### Failed to delete files or folder, they\'ve been removed or don\'t exist. #####'

def run_davinci():
    #cmd = DAVINCIPATH + 'Scripts/run.bat ' + DAVINCIPATH + 'bin ' + TESTPATH
#    cmd = DAVINCIPATH + 'Scripts/run.bat'
#    t = MyThread(cmd)
#    t.start()

    cmdbat = DAVINCIPATH + 'Scripts/run.bat'
    args1 = DAVINCIPATH + 'bin'
    args2 = TESTPATH
    cmd = [cmdbat, args1, args2]
    cmdsystem = cmdbat + ' ' + args1 + ' ' + args2
    os.system(cmdsystem)
#    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
#    stdout, stderr = p.communicate()
#    print p.returncode

# class MyThread(threading.Thread):
#    def __init__(self, batpath, **kwargs):
#        threading.Thread.__init__(self, **kwargs)
#        self.batpath = batpath
#    def run(self):
#        ShellExecute(0, None, self.batpath, DAVINCIPATH + 'bin ' + TESTPATH, DAVINCIPATH, True)

if __name__ == '__main__':
    sys.exit(run_davinci())