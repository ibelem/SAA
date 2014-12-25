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
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')

rtlibpkg = common.parse_c_json(JSONPATH, 'runtimelib_package')
rtlibapk = common.parse_c_json(JSONPATH, 'runtimelib_apk')

def download_runtimelib():
    print '*** TO DO ***'

def check_runtimelib(deviceid):
    if rtlibpkg in adb.list_pkg(deviceid):
        print rtlibapk +' was installed.'
        return True
    else:
        print rtlibapk +' is not installed.'
        return False

def uninstall_runtimelib(deviceid):
    if check_runtimelib(deviceid):
        try:
            adb.uninstall_pkg(deviceid, rtlibpkg)
            print 'Uninstall '+ rtlibapk +' ----- PASS.'
        except Exception, ex:
            print 'Uninstall '+ rtlibapk +'----- FAIL.',ex
            sys.exit(0)

def install_runtimelib(version, deviceid, arch):
    try:
        print '\nStart to handle ' + rtlibapk + ' process:'
        print '------------------------------------------------------------------------------------------------------------------------------------'
        adb.restart_adb()
        uninstall_runtimelib(deviceid)
        pkgpath = os.path.join(SUITEPATH, 'runtimelib', version, arch, rtlibapk)
        print 'Install '+ rtlibapk +' from', pkgpath
        adb.install_pkg(deviceid, pkgpath)
        print 'Install '+ rtlibapk +' ----- PASS.'
    except Exception, ex:
        print 'Install '+ rtlibapk +'----- FAIL.\n', ex
        sys.exit(0)

