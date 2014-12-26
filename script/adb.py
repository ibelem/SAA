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



