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

def csv_reader(version, deviceid, arch, filepath):
    if common.find_file(filepath):
        p = os.path.join(TESTPATH, deviceid)
        common.mk_dir(p)
        q = os.path.join(p, common.parse_config_json(CONFIGJSONPATH, 'test_result_xml_name'))
        generate_xml_report(version, deviceid, arch, q)

        dreader = csv.DictReader(open(filepath))
        #print len(list(dreader))

        for c in dreader:
            reportlink = str(c['ReportLink']).replace('=HYPERLINK("','').replace('")','').replace('\\\\','\\')
            print c['Install'], c['Launch'], c['Random'], c['Back'], c['Uninstall'], c['Result'], c['FailReason']
            for i in ['Install', 'Launch', 'Random', 'Back', 'Uninstall']:
                result = c[i]
                if result.lower() == 'skip':
                    result = 'BLOCK'
                insert_xml_case_result(version, deviceid, arch, q, c['TestTime'].strip(), c['Application'].lower().replace('.apk',''), i.upper(), result, c['FailReason'].strip(), reportlink.strip())
    else:
        print 'Can\'t find file: ' + filepath

def insert_xml_case_result(version, deviceid, arch, q, testtime, application, step, result, failreason, reportlink):
    parser = et.XMLParser(remove_blank_text=True)
    tree = et.parse(q, parser)
    #root = tree.getroot()
    set = tree.find('//set')

    t = failreason + ' ' + reportlink if failreason else reportlink
    if result != 'PASS':
        t = t
    else:
        t = reportlink

    testcase = et.SubElement(set, 'testcase')
    testcase.attrib['component'] = common.parse_config_json(CONFIGJSONPATH, 'test_suite_category') + '/' + common.parse_config_json(CONFIGJSONPATH, 'test_suite_module')
    testcase.attrib['execution_type'] = 'auto'
    testcase.attrib['id'] = 'wrt_sample_app_'+ application.lower() + '_' + step
    testcase.attrib['purpose'] = 'Verify ' + step + ' step of ' + application.lower() + ' works correctly'
    testcase.attrib['result'] = result
    #testcase.attrib['comment'] = t
    description = et.SubElement(testcase, 'description')
    pre_condition = et.SubElement(description, 'pre_condition')
    pre_condition.text = ''
    test_script_entry = et.SubElement(description, 'test_script_entry')
    test_script_entry.text = 'run.py'
    result_info = et.SubElement(testcase, 'result_info')
    actual_result = et.SubElement(result_info, 'actual_result')
    actual_result.text = result
    start = et.SubElement(result_info, 'start')
    start.text = testtime
    end = et.SubElement(result_info, 'end')
    stdout = et.SubElement(result_info, 'stdout')
    stdout.text = t
    stderr = et.SubElement(result_info, 'stderr')
    #stderr.text = failreason
    tree.write(q, pretty_print=True, xml_declaration=True, encoding='utf-8')

def generate_xml_report(version, deviceid, arch, pathname):
    if not version:
        version = ''

    dend = datetime.now()
    endtime = dend.strftime('%Y-%m-%d %H:%M:%S')

    root = et.Element('test_definition')
    root.addprevious(et.PI('xml-stylesheet', 'type="text/xsl" href="testresult.xsl"'))

    environment = et.SubElement(root, 'environment')
    environment.attrib['build_id'] = version
    environment.attrib['device_id'] = deviceid
    environment.attrib['device_model'] = ''
    environment.attrib['device_name'] = common.parse_config_json(CONFIGJSONPATH, 'device_name')[0]
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

def csv_xml(version, deviceid, arch):
    csv_reader(version, deviceid, arch, os.path.join(TESTPATH,common.parse_config_json(CONFIGJSONPATH, 'davinci_csv_file')))