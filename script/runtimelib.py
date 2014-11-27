# -*- coding: utf-8 -*-
import os,sys
from script import adb

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)

def download_runtimelib():
    print '*** TO DO ***'

def check_runtimelib(deviceid):
    if 'org.xwalk.core' in adb.list_pkg(deviceid):
        print '===== XWalkRuntimeLib.apk was installed. ====='
        return True
    else:
        print '===== XWalkRuntimeLib.apk is not installed. ====='
        return False

def uninstall_runtimelib(deviceid):
    if check_runtimelib(deviceid):
        try:
            print '***** Start to uninstall existed XWalkRuntimeLib. *****'
            adb.uninstall_pkg(deviceid, 'org.xwalk.core')
            print '===== Uninstall XWalkRuntimeLib successfully. ====='
        except Exception, ex:
            print '##### Failed to uninstall XWalkRuntimeLib. ##### ',ex
            sys.exit(0)

def install_runtimelib(version, arch, deviceid):
    if version:
        print 'Version:',version
    else:
        print '##### Version option is not defined. #####\nPlease use -v or --version with the build number of RuntimeLib.apk.'
        sys.exit(0)
    if arch:
        arch = arch.lower()
        print 'Architecture:',arch
    else:
        print '#####Architecture option is not defined. #####\nPlease use -a or --arch with values x86 or arm.'
        sys.exit(0)
    if deviceid:
        print 'Device:',deviceid
    else:
        print '----- Device ID option is not defined. -----\nConnect to default device to test.'

    try:
        uninstall_runtimelib(deviceid);
        pkgpath = os.path.join(SUITEPATH, 'runtimelib', version, arch, 'XWalkRuntimeLib.apk')
        print '***** Start to install XWalkRuntimeLib.apk from', pkgpath, '*****'
        adb.install_pkg(deviceid, pkgpath)
        print '===== XWalkRuntimeLib.apk is installed successfully. ====='
    except Exception, ex:
        print '##### Failed to install XWalkRuntimeLib.apk. #####\n',ex
        sys.exit(0)

