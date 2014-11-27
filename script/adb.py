# -*- coding: utf-8 -*-
import os,sys
import subprocess

NAME = 'adb'
DEVICE_S = '-s'
SHELL_CMD = ['shell', 'pm list packages -3 -f']
DEVICES_CMD = ['devices']
INSTALL_CMD = ['install']
UNINSTALL_CMD = ['uninstall']

def get_devices():
    getdevicescmd = [NAME] + DEVICES_CMD
    print subprocess.check_output(getdevicescmd)
    
def install_pkg(device, pkgpath):
    installpkgcmd = [NAME] + ([DEVICE_S, device] if device else []) + INSTALL_CMD
    subprocess.check_call(installpkgcmd + [pkgpath])

def uninstall_pkg(device, package):
    uninstallpkgcmd = [NAME] + ([DEVICE_S, device] if device else []) + UNINSTALL_CMD
    subprocess.check_call(uninstallpkgcmd + [package])

def list_pkg(device):
    listpackagescmd = [NAME] + ([DEVICE_S, device] if device else []) + SHELL_CMD
    return subprocess.check_output(listpackagescmd)



