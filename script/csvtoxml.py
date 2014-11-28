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
import socket
from datetime import *
import csv
import common, gl
from lxml import etree as et
# https://pypi.python.org/pypi/lxml/3.4.1

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
CONFIGJSONPATH = os.path.join(SCRIPTPATH, 'config.json')

def csv_reader(version, filepath):
    if common.find_file(filepath):

        p = os.path.join(TESTPATH, common.parse_config_json(CONFIGJSONPATH, 'device_id'))
        print p
        common.mk_dir(p)
        q = os.path.join(p, common.parse_config_json(CONFIGJSONPATH, 'test_result_xml_name'))
        generate_xml_report(version, q)

        dreader = csv.DictReader(open(filepath))
        #print len(list(dreader))

        print q
        tree = et.parse(q)

        root = tree.getroot()
        set = er.getElement('set')

        testcase = et.SubElement(set, 'testcase')
        testcase.attrib['component'] = common.parse_config_json(CONFIGJSONPATH, 'test_suite_category') + '/' + common.parse_config_json(CONFIGJSONPATH, 'test_suite_module')
        testcase.attrib['execution_type'] = 'auto'
        testcase.attrib['id'] = 'wrt'
        testcase.attrib['purpose'] = 'auto'
        testcase.attrib['result'] = 'wrt'

        for c in dreader:
            print c['TestTime'], c['DeviceName'], c['Application'], c['Package'], c['Activity']
            print c['Install'], c['Launch'], c['Random'], c['Back'], c['Uninstall'], c['Result'], c['FailReason']
            print str(c['ReportLink']).replace('=HYPERLINK("','').replace('")','').replace('\\\\','\\')

        file = et.ElementTree(root)
        file.write(q, pretty_print=True, xml_declaration=True, encoding='utf-8')

    else:
        print 'Can\'t find file: ' + filepath

def generate_xml_report(version, pathname):
    if not version:
        version = ''

    dend = datetime.now()
    endtime = dend.strftime('%Y-%m-%d %H:%M:%S')

    root = et.Element('test_definition')
    root.addprevious(et.PI('xml-stylesheet', 'type="text/xsl" href="testresult.xsl"'))

    environment = et.SubElement(root, 'environment')
    environment.attrib['build_id'] = version
    environment.attrib['device_id'] = common.parse_config_json(CONFIGJSONPATH, 'device_id')
    environment.attrib['device_model'] = ''
    environment.attrib['device_name'] = common.parse_config_json(CONFIGJSONPATH, 'device_name')
    environment.attrib['host'] = socket.gethostname()
    environment.attrib['lite_version'] = ''
    environment.attrib['manufacturer'] = ''
    environment.attrib['resolution'] = ''
    environment.attrib['screen_size'] = ''
    environmentother = et.SubElement(environment, 'other')

    summary = et.SubElement(root, 'summary')
    summary.attrib['test_plan_name'] = common.parse_config_json(CONFIGJSONPATH, 'name')
    start_at = et.SubElement(summary, 'start_at')
    start_at.text = gl.__starttime__
    end_at = et.SubElement(summary, 'end_at')
    end_at.text = endtime

    suite = et.SubElement(root, 'suite')
    suite.attrib['category'] = common.parse_config_json(CONFIGJSONPATH, 'test_suite_category')
    suite.attrib['name'] = common.parse_config_json(CONFIGJSONPATH, 'test_suite_name')

    set = et.SubElement(suite, 'set')
    set.attrib['name'] = common.parse_config_json(CONFIGJSONPATH, 'test_suite_set_name')
    set.attrib['set_debug_msg'] = 'N/A'
    set.attrib['type'] = 'wrt'

    file = et.ElementTree(root)
    file.write(pathname, pretty_print=True, xml_declaration=True, encoding='utf-8')

def csv_xml(version):
    csv_reader(version, os.path.join(TESTPATH,'Smoke_Test_Report.csv'))