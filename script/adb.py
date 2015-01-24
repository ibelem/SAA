# -*- coding: utf-8 -*-

import os,sys
import subprocess
import common, gl

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')
DAVINCIPATH = common.parse_c_json(JSONPATH, 'davinci_path')

NAME = 'adb'
DEVICE_S = '-s'
SHELL_CMD = ['shell', 'pm list packages -3 -f']
DEVICES_CMD = ['devices']
INSTALL_CMD = ['install']
UNINSTALL_CMD = ['uninstall']

def get_devices():
    getdevicescmd = [NAME] + DEVICES_CMD
    l(subprocess.check_output(getdevicescmd))
    
def install_pkg(device, pkgpath):
    installpkgcmd = [NAME] + ([DEVICE_S, device] if device else []) + INSTALL_CMD
    subprocess.check_call(installpkgcmd + [pkgpath])

def uninstall_pkg(device, package):
    uninstallpkgcmd = [NAME] + ([DEVICE_S, device] if device else []) + UNINSTALL_CMD
    subprocess.check_call(uninstallpkgcmd + [package])

def list_pkg(device):
    listpackagescmd = [NAME] + ([DEVICE_S, device] if device else []) + SHELL_CMD
    return subprocess.check_output(listpackagescmd)

def restart_adb():
    l('Restart adb service ...')
    res = os.popen('adb kill-server').readlines()
    res = os.popen('adb start-server').readlines()
    resinfo = ''.join(res)
    l(resinfo)
    if resinfo.find('daemon started successfully') < 0:
        l('Restart adb service ----- FAIL')
        restart_adb()
    else:
        res = os.popen('adb devices').readlines()
        return 0

def l(str):
    common.log_info(str, gl.__logfile__)
