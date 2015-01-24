# -*- coding: utf-8 -*-

import os,sys
from script import adb, common, gl

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')

rtlibpkg = common.parse_c_json(JSONPATH, 'runtimelib_package')
rtlibapk = common.parse_c_json(JSONPATH, 'runtimelib_apk')

def l(str):
    common.log_info(str, gl.__logfile__)

def lr(str):
    common.log_err(str, gl.__logfile__)

def download_runtimelib():
    l('TO DO download_runtimelib()')

def check_runtimelib(deviceid):
    if rtlibpkg in adb.list_pkg(deviceid):
        l(rtlibapk +' was installed.')
        return True
    else:
        lr(rtlibapk +' is not installed.')
        return False

def uninstall_runtimelib(deviceid):
    if check_runtimelib(deviceid):
        try:
            adb.uninstall_pkg(deviceid, rtlibpkg)
            l('Uninstall ' + rtlibapk +' ----- PASS')
        except Exception, ex:
            lr(str(ex) + ' Uninstall ' + rtlibapk +' ----- FAIL')
            sys.exit(0)

def install_runtimelib(version, deviceid, arch):
    try:
        l('Start to handle ' + rtlibapk + ' process:')
        l('------------------------------------------------------------------------------------------------------------------------------------')
        adb.restart_adb()
        uninstall_runtimelib(deviceid)
        pkgpath = os.path.join(SUITEPATH, 'runtimelib', version, arch, rtlibapk)
        l('Install '+ rtlibapk +' from ' + pkgpath)
        adb.install_pkg(deviceid, pkgpath)
        l('Install '+ rtlibapk +' ----- PASS')
    except Exception, ex:
        lr(str(ex) + ' Install '+ rtlibapk +'----- FAIL')
        sys.exit(0)
