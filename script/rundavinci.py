# -*- coding: utf-8 -*-

# Copyright (c) 2015 Intel Corporation.
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
import time, csv, xlsxwriter
import threading
#from win32api import *
import subprocess
import common, gl

#pip install XlsxWriter
#pip --proxy=http://proxy.xxxx.com:911 install requests
#pip --proxy=http://proxy.xxxx.com:911 install wheel
#pip wheel XlsxWriter-0.6.6-py2.py3-none-any.whl
#pip install --use-wheel --no-index --find-links=wheelhouse XlsxWriter

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')
DAVINCIPATH = common.parse_c_json(JSONPATH, 'davinci_path')

def l(str):
    common.log_info(str, gl.__logfile__)

def lr(str):
    common.log_err(str, gl.__logfile__)

def clear_davinci_test(deviceid):
    l('Clean up test suite path and apk tests path:')
    l('------------------------------------------------------------------------------------------------------------------------------------')
    try:
        try:
            common.del_files(SUITEPATH, 'null')
            l('Delete null in ' + SUITEPATH + ' ----- DONE')
        except Exception, ex:
            lr(str(ex) + ' Delete null file ----- FAIL')
        try:
            common.del_files(SUITEPATH, '.png')
            l('Delete .png in ' + SUITEPATH + ' ----- DONE')
        except Exception, ex:
            lr(str(ex) + ' Delete .png ----- FAIL')
        try:
            common.del_files(SUITEPATH, '.info')
            l('Delete .info in ' + SUITEPATH + ' ----- DONE')
        except Exception, ex:
            lr(str(ex) + ' Delete .info ----- FAIL')
        try:
            common.del_files(SUITEPATH, '.txt')
            l('Delete .txt in ' + SUITEPATH + ' ----- DONE')
        except Exception, ex:
            lr(str(ex) + ' Delete .txt ----- FAIL')
        try:
            common.del_files(SUITEPATH, '.log')
            l('Delete .log in ' + SUITEPATH + ' ----- DONE')
        except Exception, ex:
            lr(str(ex) + ' Delete .log ----- FAIL')

        for i in ['.qs', '.xml','.csv', '.txt', '.log']:
            common.del_files(TESTPATH, i)
            l('Delete ' + i + ' in ' + TESTPATH + ' ----- DONE')

        davinci_rnr_log_dir = common.parse_c_json(JSONPATH, 'davinci_rnr_log_dir')
        if common.find_dir(os.path.join(TESTPATH, davinci_rnr_log_dir)):
            common.del_dir(os.path.join(TESTPATH, davinci_rnr_log_dir))
            l('Delete folder ' + os.path.join(TESTPATH, davinci_rnr_log_dir) + ' ----- DONE')

        device_id_dir = deviceid
        if common.find_dir(os.path.join(TESTPATH, device_id_dir)):
            common.del_dir(os.path.join(TESTPATH, device_id_dir))
            l('Delete folder ' + os.path.join(TESTPATH, device_id_dir) + ' ----- DONE')

        if common.find_glob_path(TESTPATH + '/TestResult_*'):
            for i in common.find_glob_path(TESTPATH + '/TestResult_*'):
                common.del_dir(i)
            l('Delete folder ' + i + ' ----- DONE')
    except Exception, ex:
        lr(str(ex) + ' Delete file or folder ----- FAIL')

def prepare_davinci_delete_default_device_cfg_txt():
    delete_default_device_cfg_txt_path = os.path.join(DAVINCIPATH, 'Scripts', 'default_device_cfg.txt')
    if common.find_file(delete_default_device_cfg_txt_path):
        common.del_file(delete_default_device_cfg_txt_path)
        l('Delete default_device_cfg.txt: ----- DONE')
    else:
        l('default_device_cfg.txt doesn\'t exist ----- OK')

def prepare_davinci_silent_mode():
    if common.find_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input1.txt')):
        common.copy_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input1.txt'), os.path.join(SUITEPATH, 'user_input1.txt'))
    if common.find_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input2.txt')):
        common.copy_file(os.path.join(DAVINCIPATH, 'Scripts', 'user_input2.txt'), os.path.join(SUITEPATH, 'user_input2.txt'))
    l('Prepare DaVinci silent mode test ----- DONE')

def prepare_davinci_run_qs_py():
    davinci_device_environment_set = common.parse_c_json(JSONPATH, 'davinci_device_environment_set')
    #davinci_timeout = common.parse_c_json(JSONPATH, 'davinci_timeout')
    davinci_rerun_max = common.parse_c_json(JSONPATH, 'davinci_rerun_max')
    davinci_battery_threshold = common.parse_c_json(JSONPATH, 'davinci_battery_threshold')

    run_qs_path = os.path.join(DAVINCIPATH, 'Scripts', 'run_qs.py')
    run_qs_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'run_qs_bak.py')
    #power_pusher_abs_path = os.path.join(DAVINCIPATH, 'Scripts') + '/power_pusher.qs'

    if not common.find_file(run_qs_bak_path):
        common.copy_file(run_qs_path, run_qs_bak_path)
        if common.find_file(run_qs_bak_path):
            common.remove_glob_path(run_qs_path)

    if common.find_file(run_qs_bak_path):
        f_bak = open(run_qs_bak_path, "r+")
        target_file = open(run_qs_path, 'w')
        #pp_qs = "power_pusher.qs" => pp_qs = "ABSOLUTE_PATH/power_pusher.qs"
        g = f_bak.read()
        #g = re.sub(r'pp_qs = "power_pusher.qs"', 'pp_qs = "'+ power_pusher_abs_path +'"', g)
        # RunDavinci(device_name, qs_name) in run_qs.py
        #g = re.sub(r'timeout = 600', 'timeout = ' + davinci_timeout, g)
        #g = re.sub(r'timeout = 1000', 'timeout = ' + davinci_timeout, g)
        # RunTest(is_agressive) in run_qs.py
        g = re.sub(r'rerun_max = 3', 'rerun_max = ' + davinci_rerun_max, g)
        # Add changed = True in CreateNewCfg(camera_mode) in run_qs.py
        #g = re.sub(r'reuse = False', 'reuse = False\n        changed = True', g)
        # Modify threshold value ChooseDevice(dev_list, tar_flag) in run_qa.py
        g = re.sub(r'threshold = 20', 'threshold = ' + davinci_battery_threshold, g)
        # PrepareBeforeSmokeTest(device_name) in run_qs.py
        if davinci_device_environment_set == 'false':
            g = g.replace('PrepareBeforeSmokeTest(all_dev)', '#PrepareBeforeSmokeTest(all_dev)')
        #Strength Restart_adb() in run_qs.py
        g = g.replace('PrintAndLogErr("  - Please make sure adb service is OK.")', 'PrintAndLogErr("  - Please make sure adb service is OK.")\n        Restart_adb()')
        #Disable manual to choose reference devices in run_qs.py
        l('Disable manual to choose reference devices ----- DONE')
        g = re.sub(r'ref_dev_list = raw_input', '#ref_dev_list = raw_input', g)
        g = re.sub(r'if ref_dev_list == "0":', 'ref_dev_list = "0"\n                if ref_dev_list == "0":', g)
        #Disable manual to choose device group in run_qs.py
        l('Disable manual to choose device group ----- DONE')
        g = re.sub(r'selection_choice = raw_input', '#selection_choice = raw_input', g)
        g = re.sub(r'if selection_choice == "":', 'selection_choice = "0"\n            if selection_choice == "":', g)
        target_file.write(g)
        f_bak.close()
        target_file.close()

    if common.find_file(run_qs_path):
        #if common.find_text_in_file('pp_qs = "'+ power_pusher_abs_path +'"', run_qs_path) > 0:
        #    l('Set absolute path of pp_qs: ' + power_pusher_abs_path + ' ----- DONE')
        #if common.find_text_in_file('timeout = ' + davinci_timeout, run_qs_path) > 0:
        #    l('Set davinci_timeout: ' + davinci_timeout + ' ----- DONE')
        if common.find_text_in_file('rerun_max = ' + davinci_rerun_max, run_qs_path) > 0:
            l('Set davinci_rerun_max: ' + davinci_rerun_max + ' ----- DONE')
        if common.find_text_in_file('threshold = ' + davinci_battery_threshold, run_qs_path) > 0:
            l('Set davinci_battery_threshold: ' + davinci_battery_threshold + ' ----- DONE')
        if common.find_text_in_file('ref_dev_list = "0"', run_qs_path) > 0:
            l('Set reference devices: 0 ----- DONE')
        if common.find_text_in_file('selection_choice = "0"', run_qs_path) > 0:
            l('Set device group selection choice: 0 ----- DONE')

def prepare_davinci_generate_py():
    rtlibpkg = common.parse_c_json(JSONPATH, 'runtimelib_package')
    rtlibapk = common.parse_c_json(JSONPATH, 'runtimelib_apk')
    davinci_action_number = common.parse_c_json(JSONPATH, 'davinci_action_number')
    davinci_click_percentage = common.parse_c_json(JSONPATH, 'davinci_click_percentage')
    davinci_swipe_percentage = common.parse_c_json(JSONPATH, 'davinci_swipe_percentage')

    generate_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate.py')
    generate_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate_bak.py')

    if not common.find_file(generate_bak_path):
        common.copy_file(generate_path, generate_bak_path)
        if common.find_file(generate_bak_path):
            common.remove_glob_path(generate_path)

    if common.find_file(generate_bak_path):
        f_bak = open(generate_bak_path, "r+")
        target_file = open(generate_path, 'w')
        g = f_bak.read()
        #Disable manual to confirm settings in SmokeConfig.csv in generate.py
        l('Disable manual to confirm settings in SmokeConfig.csv ----- DONE')
        g = re.sub(r'config_done = raw_input', '#config_done = raw_input', g)
        target_file.write(g)
        f_bak.close()
        target_file.close()

    smokeconfig_path = os.path.join(DAVINCIPATH, 'Scripts', 'SmokeConfig.csv')
    smokeconfig_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'SmokeConfig_bak.csv')

    if not common.find_file(smokeconfig_bak_path):
        common.copy_file(smokeconfig_path, smokeconfig_bak_path)
        if common.find_file(smokeconfig_bak_path):
            common.remove_glob_path(smokeconfig_path)

    lists = []
    with open(smokeconfig_bak_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';',  quotechar = '|')
        for row in reader:
            lists.append(row)

    with open(smokeconfig_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';', quotechar = '|',  quoting=csv.QUOTE_MINIMAL)
        for row in lists:
            t = 'Total Action Number (click action number + swipe action number):,'
            if str(row[0]).find(t) >= 0:
                row[0] = row[0].replace('10','')
                row[0] = row[0].replace(t, t + davinci_action_number)
            t = 'Click Percentage (click action number / total action number) (%):,'
            if str(row[0]).find(t) >= 0:
                row[0] = row[0].replace('80','')
                row[0] = row[0].replace(t, t + davinci_click_percentage)
            t = 'Swipe Percentage (swipe action number / total action number) (%):,'
            if str(row[0]).find(t) >= 0:
                row[0] = row[0].replace('20','')
                row[0] = row[0].replace(t, t + davinci_swipe_percentage)
            t = 'Camera Mode (ScreenCap or Disabled):,ScreenCap'
            if str(row[0]).find(t) >= 0:
                row[0] = row[0].replace(',ScreenCap',',Disabled')
            t = 'Test login feature or not (Yes/No):,Yes'
            if str(row[0]).find(t) >= 0:
                row[0] = row[0].replace('Test login feature or not (Yes/No):,Yes','Test login feature or not (Yes/No):,No')
            if str(row[0]).find('with semicolons):,') >= 0:
                row[0] = row[0].replace('with semicolons):,', 'with semicolons):,' + rtlibpkg)
            writer.writerow(row)

    l('Set davinci_action_number: ' + davinci_action_number + ' ----- DONE')
    l('Set davinci_click_percentage: ' + davinci_click_percentage + ' ----- DONE')
    l('Set davinci_swipe_percentage: ' + davinci_swipe_percentage + ' ----- DONE')
    l('Disabled Screen Capture: ----- DONE')
    l('Disabled login feature: ----- DONE')
    l('Set package name of '+ rtlibapk + ': ' + rtlibpkg + ' for logcat capturing ----- DONE')

def prepare_davinci_generate_py_before_2dot3():
    davinci_action_number = common.parse_c_json(JSONPATH, 'davinci_action_number')
    davinci_click_percentage = common.parse_c_json(JSONPATH, 'davinci_click_percentage')
    davinci_swipe_percentage = common.parse_c_json(JSONPATH, 'davinci_swipe_percentage')

    generate_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate.py')
    generate_bak_path = os.path.join(DAVINCIPATH, 'Scripts', 'generate_bak.py')

    if not common.find_file(generate_bak_path):
        common.copy_file(generate_path, generate_bak_path)
        if common.find_file(generate_bak_path):
            common.remove_glob_path(generate_path)

    update_string = 'actionNum='+ davinci_action_number +', clickPro='+ davinci_click_percentage +', swipePro=' + davinci_swipe_percentage

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
            l('Set davinci_action_number: ' + davinci_action_number + ' ----- DONE')
            l('Set davinci_click_percentage: ' + davinci_click_percentage + ' ----- DONE')
            l('Set davinci_swipe_percentage: ' + davinci_swipe_percentage + ' ----- DONE')

def precondition_davinci():
    l('Update DaVinci run_qs.py and generate.py scripts base on config.json options:')
    l('------------------------------------------------------------------------------------------------------------------------------------')
    prepare_davinci_delete_default_device_cfg_txt()
    prepare_davinci_silent_mode()
    prepare_davinci_run_qs_py()
    prepare_davinci_generate_py()

def run_davinci(version, deviceid, arch):
    #    cmd = DAVINCIPATH + 'Scripts/run.bat ' + DAVINCIPATH + 'bin ' + TESTPATH
    #    cmd = DAVINCIPATH + 'Scripts/run.bat'
    #    t = MyThread(cmd)
    #    t.start()

    #set currentFolder=%~dp0
    #set DaVinciHome=%~1
    #set QScriptFolder=%~2
    #set CameraMode=%3
    #set aggressive=%4
    #set SilentMode=%5
    #set FileList=%6

    precondition_davinci()
    time.sleep(5)

    if (not common.find_file(os.path.join(SUITEPATH, 'user_input1.txt'))) or (not common.find_file(os.path.join(SUITEPATH, 'user_input2.txt'))):
        l('Unable to get init config file: user_input1.txt and user_input2.txt')
        sys.exit(0)

    cmdbat = DAVINCIPATH + 'Scripts/run.bat'
    args1 = DAVINCIPATH + 'bin'
    args2 = TESTPATH
    args3 = 'False'
    args4 = 'False'
    args5 = 'True'
    args6 = ''

    cmd = [cmdbat, args1, args2, args3, args4, args5, args6]
    cmdsystem = ' '.join(cmd)
    l('Start to run DaVinci:')
    l('------------------------------------------------------------------------------------------------------------------------------------')
    l(cmdsystem)
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