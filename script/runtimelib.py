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
from script import adb, common

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
CONFIGJSONPATH = os.path.join(SCRIPTPATH, 'config.json')

runtimelibpkg = common.parse_config_json(CONFIGJSONPATH, 'runtimelib_package')
runtimelibapk = common.parse_config_json(CONFIGJSONPATH, 'runtimelib_apk')

def download_runtimelib():
    print '*** TO DO ***'

def check_runtimelib(deviceid):
    if runtimelibpkg in adb.list_pkg(deviceid):
        print '===== '+ runtimelibapk +' was installed. ====='
        return True
    else:
        print '===== '+ runtimelibapk +' is not installed. ====='
        return False

def uninstall_runtimelib(deviceid):
    if check_runtimelib(deviceid):
        try:
            print '***** Start to uninstall existed '+ runtimelibapk +'. *****'
            adb.uninstall_pkg(deviceid, runtimelibpkg)
            print '===== Uninstall '+ runtimelibapk +' successfully. ====='
        except Exception, ex:
            print '##### Failed to uninstall '+ runtimelibapk +'. ##### ',ex
            sys.exit(0)

def install_runtimelib(version, deviceid, arch):
    try:
        uninstall_runtimelib(deviceid);
        pkgpath = os.path.join(SUITEPATH, 'runtimelib', version, arch, runtimelibapk)
        print '***** Start to install '+ runtimelibapk +' from', pkgpath, '*****'
        adb.install_pkg(deviceid, pkgpath)
        print '===== '+ runtimelibapk +' is installed successfully. ====='
    except Exception, ex:
        print '##### Failed to install '+ runtimelibapk +'. #####\n', ex
        sys.exit(0)

