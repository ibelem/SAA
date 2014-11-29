# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# Copyright (c) 2014 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this list
#   of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#        Zhang,Belem <belem.zhang@intel.com>

import os,sys
import threading
#from win32api import *
import subprocess
import common

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
CONFIGJSONPATH = os.path.join(SCRIPTPATH, 'config.json')
DAVINCIPATH = common.parse_config_json(CONFIGJSONPATH, 'davinci_path')

def clear_davinci_test(deviceid):
    print '***** Clean up files in test suite path and apk test path *****'
    try:
        davinci_rnr_log_dir = common.parse_config_json(CONFIGJSONPATH, 'davinci_rnr_log_dir')
        if common.find_dir(os.path.join(TESTPATH, davinci_rnr_log_dir)):
            common.del_dir(os.path.join(TESTPATH, davinci_rnr_log_dir))
            print '===== Delete folder: ' + os.path.join(TESTPATH, davinci_rnr_log_dir) + ' ====='
        device_id_dir = deviceid
        if common.find_dir(os.path.join(TESTPATH, device_id_dir)):
            common.del_dir(os.path.join(TESTPATH, device_id_dir))
            print '===== Delete folder: ' + os.path.join(TESTPATH, device_id_dir) + ' ====='
        for i in ['.qs','.txt','.xml','.csv']:
            common.del_files(TESTPATH, i)
        for j in ['.txt','.log']:
            common.del_files(SUITEPATH, j)
        print '===== Delete file: ' + '.qs, .xml, .csv, .txt, .log' + i + ' in ' + TESTPATH + ' ====='
    except Exception, ex:
        print ex,'\n##### Failed to delete files or folder, they\'ve been removed or don\'t exist. #####'

def run_davinci(version, deviceid, arch):
#    cmd = DAVINCIPATH + 'Scripts/run.bat ' + DAVINCIPATH + 'bin ' + TESTPATH
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