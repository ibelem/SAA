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
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION 'AS IS'
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
from datetime import *
from optparse import OptionParser
from script import common, adb, runtimelib, rundavinci, csvtoxml, gl
import threading

SUITEPATH = os.path.dirname(os.path.abspath(__file__))
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
CONFIGJSONPATH = os.path.join(SCRIPTPATH, 'config.json')

runtimelibapk = common.parse_config_json(CONFIGJSONPATH, 'runtimelib_apk')

def run(version, deviceid, arch):
    rundavinci.clear_davinci_test(deviceid)
    runtimelib.install_runtimelib(version, deviceid, arch)
    rundavinci.run_davinci(version, deviceid, arch)
    csvtoxml.csv_xml(version, deviceid, arch)

def option_check(version, deviceid, arch):
    if version:
        print 'Version:', version
    else:
        print '##### Version option is not defined. #####\nPlease use -v or --version with the build number of '+ runtimelibapk +'.'
        sys.exit(0)

    if arch and deviceid:
        arch = arch.lower()
        print 'Device:', deviceid
        print 'Architecture:', arch
        run(version, deviceid, arch)
    elif arch and not deviceid:
        print '##### Device id option is not defined. #####\nUse \'python run.py -h\' get more information.'
    elif deviceid and not arch:
        print '##### Architecture option is not defined. #####\nUse \'python run.py -h\' get more information.'
    else:
        for i in common.parse_config_json(CONFIGJSONPATH, 'device'):
            print 'Device:', i['device_id']
            print 'Architecture:', i['device_arch']
            print 'Name:', i['device_name']
            run(version, i['device_id'], i['device_arch'])

def main():
    parser = OptionParser()
    parser.add_option('-v', '--version', dest='version',
                  help = '(required) build number of ' + runtimelibapk + '.')
    #parser.add_option('-c', '--clear', dest='clear',
    #            help = '(optional) clear the test suite environment from the beginning.')
    parser.add_option('-a', '--arch', dest='arch',
                  help = '(optional) architecture (x86 or arm) of '+ runtimelibapk +'. -d is required if you use it.')
    parser.add_option('-d', '--device', dest='device',
              help = '(optional) device ID of the test device. -a is required if you use it.')
    (options, args) = parser.parse_args()

    print args

    d = datetime.now()
    gl.__starttime__ = d.strftime('%Y-%m-%d %H:%M:%S')

    option_check(options.version, options.device, options.arch)

if __name__ == '__main__':
    sys.exit(main())
    #python run.py -v 11.39.251.0 -a x86 -d MedfieldC3567E1E