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

import os, sys, re
from time import sleep
import time
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
    print '\nClean up test suite path and apk test path:'
    try:
        for i in ['.qs','.txt','.xml','.csv', '.txt','.log']:
            common.del_files(TESTPATH, i)
        common.del_files(SUITEPATH, 'null')
        common.del_files(SUITEPATH, '.png')
        common.del_files(SUITEPATH, '.info')
        common.del_file(SUITEPATH + '/null')
        common.del_files(SUITEPATH, '.txt')
        common.del_files(SUITEPATH, '.log')

        print 'Delete file: ' + '.qs, .xml, .csv, .txt, .log' + i + ' in ' + TESTPATH + ' ----- PASS'

        davinci_rnr_log_dir = common.parse_config_json(CONFIGJSONPATH, 'davinci_rnr_log_dir')
        if common.find_dir(os.path.join(TESTPATH, davinci_rnr_log_dir)):
            common.del_dir(os.path.join(TESTPATH, davinci_rnr_log_dir))
            print 'Delete folder: ' + os.path.join(TESTPATH, davinci_rnr_log_dir) + ' ----- PASS'

        device_id_dir = deviceid
        if common.find_dir(os.path.join(TESTPATH, device_id_dir)):
            common.del_dir(os.path.join(TESTPATH, device_id_dir))
            print 'Delete folder: ' + os.path.join(TESTPATH, device_id_dir) + ' ----- PASS'

        if common.find_glob_path(TESTPATH + '/TestResult_*'):
            for i in common.find_glob_path(TESTPATH + '/TestResult_*'):
                common.del_dir(i)
            print 'Delete folder: ' + i + ' ----- PASS'
    except Exception, ex:
        print ex,'\nDelete files or folder ----- FAIL.'

def prepare_davinci_delete_default_device_cfg_txt():
    delete_default_device_cfg_txt_path = os.path.join(DAVINCIPATH, 'Scripts', 'default_device_cfg.txt')
    if common.find_file(delete_default_device_cfg_txt_path):
        common.del_file(delete_default_device_cfg_txt_path)
        print 'Delete default_device_cfg.txt: ----- PASS'
    else:
        print 'default_device_cfg.txt doesn\'t exist ----- Good'

def prepare_davinci_silent_mode():
    if common.find_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input1.txt')):
        common.copy_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input1.txt'), os.path.join(SUITEPATH, 'user_input1.txt'))
    if common.find_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input2.txt')):
        common.copy_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input2.txt'), os.path.join(SUITEPATH, 'user_input2.txt'))
    print 'Prepare DaVinci silent mode test ----- PASS'

def prepare_davinci_run_qs_py():
    davinci_device_environment_set = common.parse_config_json(CONFIGJSONPATH, 'davinci_device_environment_set')
    davinci_test_timeout = common.parse_config_json(CONFIGJSONPATH, 'davinci_test_timeout')
    davinci_test_rerun_max = common.parse_config_json(CONFIGJSONPATH, 'davinci_test_rerun_max')

    run_qs_path = os.path.join(DAVINCIPATH, 'Scripts', 'run_qs.py')
    run_qs_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'run_qs_bak.py')
    power_pusher_abs_path = os.path.join(DAVINCIPATH, 'Scripts') + '/power_pusher.qs'

    if not common.find_file(run_qs_bak_path):
        common.copy_file(run_qs_path, run_qs_bak_path)
        if common.find_file(run_qs_bak_path):
            common.remove_glob_path(run_qs_path)

    if common.find_file(run_qs_bak_path):
        f_bak = open(run_qs_bak_path, "r+")
        target_file = open(run_qs_path, 'w')
        #pp_qs = "power_pusher.qs" => pp_qs = "ABSOLUTE_PATH/power_pusher.qs"
        g = re.sub(r'pp_qs = "power_pusher.qs"', 'pp_qs = "'+ power_pusher_abs_path +'"', f_bak.read())
        # RunDavinci(device_name, qs_name) in run_qs.py
        g = re.sub(r'timeout = 600', 'timeout = ' + davinci_test_timeout, g)
        #g = re.sub(r'timeout = 1000', 'timeout = ' + davinci_test_timeout, g)
        # RunTest(is_agressive) in run_qs.py
        g = re.sub(r'rerun_max = 3', 'rerun_max = ' + davinci_test_rerun_max, g)
        # Add changed = True in CreateNewCfg(camera_mode) in run_qs.py
        g = re.sub(r'reuse = False', 'reuse = False\n        changed = True', g)
        # PrepareBeforeSmokeTest(device_name) in run_qs.py
        if davinci_device_environment_set == 'false':
            g = g.replace('PrepareBeforeSmokeTest(all_dev)', '#PrepareBeforeSmokeTest(all_dev)')
        target_file.write(g)
        f_bak.close()
        target_file.close()

    if common.find_file(run_qs_path):
        if common.find_text_in_file('timeout = ' + davinci_test_timeout, run_qs_path) > 0:
            print 'Set davinci_test_timeout: ' + davinci_test_timeout + ' ----- PASS'
        if common.find_text_in_file('rerun_max = ' + davinci_test_rerun_max, run_qs_path) > 0:
            print 'Set davinci_test_rerun_max: ' + davinci_test_rerun_max + ' ----- PASS'

def prepare_davinci_generate_py():
    davinci_test_action_number = common.parse_config_json(CONFIGJSONPATH, 'davinci_test_action_number')
    davinci_test_click_percentage = common.parse_config_json(CONFIGJSONPATH, 'davinci_test_click_percentage')
    davinci_test_swipe_percentage = common.parse_config_json(CONFIGJSONPATH, 'davinci_test_swipe_percentage')

    generate_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate.py')
    generate_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate_bak.py')

    if not common.find_file(generate_bak_path):
        common.copy_file(generate_path, generate_bak_path)
        if common.find_file(generate_bak_path):
            common.remove_glob_path(generate_path)

    update_string = 'actionNum='+ davinci_test_action_number +', clickPro='+ davinci_test_click_percentage +', swipePro=' + davinci_test_swipe_percentage

    if common.find_file(generate_bak_path):
        f_bak = open(generate_bak_path, "r+")
        target_file = open(generate_path, 'w')
        # actionNum=10, clickPro=80, swipePro=20 in generate.py
        g = re.sub(r'actionNum=10, clickPro=80, swipePro=20',
                   update_string,
                   f_bak.read())
        target_file.write(g)
        f_bak.close()
        target_file.close()

    if common.find_file(generate_path):
        if common.find_text_in_file(update_string, generate_path) > 0:
            print 'Set davinci_test_action_number: ' + davinci_test_action_number + ' ----- PASS'
            print 'Set davinci_test_click_percentage: ' + davinci_test_click_percentage + ' ----- PASS'
            print 'Set davinci_test_swipe_percentage: ' + davinci_test_swipe_percentage + ' ----- PASS'

def precondition_davinci():
    prepare_davinci_delete_default_device_cfg_txt()
    prepare_davinci_silent_mode()
    prepare_davinci_run_qs_py()
    prepare_davinci_generate_py()
    print '\n'

def run_davinci(version, deviceid, arch):
    #    cmd = DAVINCIPATH + 'Scripts/run.bat ' + DAVINCIPATH + 'bin ' + TESTPATH
    #    cmd = DAVINCIPATH + 'Scripts/run.bat'
    #    t = MyThread(cmd)
    #    t.start()

    #    set currentFolder=%~dp0
    #    set DaVinciHome=%~1
    #    set QScriptFolder=%~2
    #    set CameraMode=%3
    #    set videoRecording=%4
    #    set relaunch=%5
    #    set aggressive=%6
    #    set SilentMode=%7

    precondition_davinci()
    time.sleep(5)

    if (not common.find_file(os.path.join(SUITEPATH, 'user_input1.txt'))) or (not common.find_file(os.path.join(SUITEPATH, 'user_input2.txt'))):
        print 'Unable to get init config file of user_input1.txt and user_input2.txt'
        sys.exit(0)

    cmdbat = DAVINCIPATH + 'Scripts/run.bat'
    args1 = DAVINCIPATH + 'bin'
    args2 = TESTPATH
    args3 = 'ScreenCap'
    args4 = 'False'
    args5 = 'False'
    args6 = 'False'
    args7 = 'True'
    cmd = [cmdbat, args1, args2, args3, args4, args5, args6, args7]
    cmdsystem = ' '.join(cmd)
    print cmdsystem
    print '\n'
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