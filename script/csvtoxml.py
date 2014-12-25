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
import socket, codecs
from datetime import *
import csv
import common, gl
from lxml import etree as et

# https://pypi.python.org/pypi/lxml/3.4.1

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')

davincicsvfile = common.parse_c_json(JSONPATH, 'davinci_csv_file')
testresultdir = common.parse_c_json(JSONPATH, 'test_result_dir')
rnr = common.parse_c_json(JSONPATH, 'davinci_rnr_log_dir')
rnrtmpdir = os.path.join(TESTPATH, rnr)

def copy_result(deviceid, exetime):
    if not common.find_dir(testresultdir):
        common.mk_dir(testresultdir)
    try:
        common.copy_tree(os.path.join(TESTPATH, deviceid), os.path.join(testresultdir, deviceid))
    except Exception, ex:
        common.copy_files(os.path.join(TESTPATH, deviceid), os.path.join(testresultdir, deviceid))

    tr = 'TestResult_' + exetime
    try:
        common.copy_tree(os.path.join(TESTPATH, tr), os.path.join(testresultdir, tr))
    except Exception, ex:
        common.copy_files(os.path.join(TESTPATH, tr), os.path.join(testresultdir, tr))

    try:
        common.copy_tree(rnrtmpdir, os.path.join(testresultdir, rnr))
    except Exception, ex:
        common.copy_files(rnrtmpdir, os.path.join(testresultdir, rnr))

def csv_reader(version, deviceid, arch, filepath, exetime):
    if common.find_file(filepath):
        p = os.path.join(TESTPATH, deviceid)
        common.mk_dir(p)
        p = os.path.join(TESTPATH, deviceid, exetime)
        common.mk_dir(p)

        q = os.path.join(p, common.parse_c_json(JSONPATH, 'test_result_xml_name'))
        generate_xml_report(version, deviceid, arch, q)

        dreader = csv.DictReader(open(filepath))
        #print len(list(dreader))

        for c in dreader:
            reportlink = str(c['Link']).replace('=HYPERLINK("','').replace('")','').replace('\\\\','\\')
            #testtime = c['TestTime']
            testtime = ''
            print c['Install'], c['Launch'], c['Random'], c['Back'], c['Uninstall'], c['Logcat'], c['Result'], c['Reason'].strip()
            for i in ['Install', 'Launch', 'Random', 'Back', 'Uninstall', 'Logcat']:
                result = c[i]
                if result.lower() == 'skip':
                    result = 'BLOCK'
                application = ''
                try:
                    application = c['Application'].decode('utf-8').replace('.apk','')
                except Exception, ex:
                    application = c['\xef\xbb\xbfApplication'].decode('utf-8').replace('.apk','')
                package = ''
                try:
                    package = c['Package']
                except Exception, ex:
                    print ex
                insert_xml_case_result(version, deviceid, arch, q, testtime, application, package, i.lower(), result, c['Reason'].strip(), reportlink.strip())
        copy_result(deviceid, exetime)
    else:
        print 'Can\'t find file: ' + filepath

def insert_xml_case_result(version, deviceid, arch, q, testtime, application, package, step, result, failreason, reportlink):
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
    testcase.attrib['component'] = common.parse_c_json(JSONPATH, 'test_suite_category') + '/' + common.parse_c_json(JSONPATH, 'test_suite_module') + '/' + package
    testcase.attrib['execution_type'] = 'auto'
    testcase.attrib['id'] = 'webapp_monkey_'+ application.lower() + '_' + step
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
    environment.attrib['device_name'] = common.parse_c_json(JSONPATH, 'device_name')[0]
    environment.attrib['host'] = socket.gethostname()
    environment.attrib['lite_version'] = ''
    environment.attrib['manufacturer'] = ''
    environment.attrib['resolution'] = ''
    environment.attrib['screen_size'] = ''
    environmentother = et.SubElement(environment, 'other')

    summary = et.SubElement(root, 'summary')
    summary.attrib['test_plan_name'] = common.parse_c_json(JSONPATH, 'name')
    start_at = et.SubElement(summary, 'start_at')
    start_at.text = gl.__starttime__
    end_at = et.SubElement(summary, 'end_at')
    end_at.text = endtime

    suite = et.SubElement(root, 'suite')
    suite.attrib['category'] = common.parse_c_json(JSONPATH, 'test_suite_category')
    suite.attrib['name'] = common.parse_c_json(JSONPATH, 'test_suite_name')

    set = et.SubElement(suite, 'set')
    set.attrib['name'] = common.parse_c_json(JSONPATH, 'test_suite_set_name')
    set.attrib['set_debug_msg'] = 'N/A'
    set.attrib['type'] = 'wrt'
    file = et.ElementTree(root)
    file.write(pathname, pretty_print=True, xml_declaration=True, encoding='utf-8')

def csv_insert_logcat_result(filepath, filepathnew):
    def add_logcat_record(record, result):
            record['Logcat'] = result
    with open(filepath, "rb") as fin:
        with open(filepathnew, "wb") as fout:
            fields = ['Application',
                      'App name',
                      'Device Model', 'Android Version', 'Device Build Number', 'Package',
                      'App Version',
                      'Install', 'Launch', 'Random', 'Back', 'Uninstall',
                      'Result', 'Reason', 'Link']
            fields_new = ['Application',
                      'App name',
                      'Device Model', 'Android Version', 'Device Build Number', 'Package',
                      'App Version',
                      'Install', 'Launch', 'Random', 'Back', 'Uninstall', 'Logcat',
                      'Result', 'Reason', 'Link']
            reader = csv.DictReader(fin, fieldnames=fields)
            writer = csv.DictWriter(fout, fieldnames=fields_new)
            writer.writeheader()
            #fout.write(",".join(fields) + '\n')
            reader.next()
            for record in reader:
                add_logcat_record(record, check_logcat_result(filepath, record['Package'].replace('.apk','')))
                writer.writerow(record)

def check_logcat_result(csvpath, apkpackage):
    keyword_fail = common.parse_c_json(JSONPATH, 'keyword_fail')
    logcatresult = 'BLOCK'
    num = 0
    logcatpkgpath = rnrtmpdir + '/*/' + 'apk_logcat_'+ apkpackage +'.txt'
    if common.find_glob_path(logcatpkgpath):
        for j in common.find_glob_path(logcatpkgpath):
            for k in keyword_fail:
                if common.find_text_in_file_case_insensitive(k.lower(), j):
                    num = num + 1
        if num > 0:
            logcatresult = 'FAIL'
        else:
            logcatresult = 'PASS'
        num = 0
    else:
        logcatresult = 'BLOCK'
    return logcatresult


def csv_xml(version, deviceid, arch):
    print '\nStart to handle CSV and XML results:'
    print '------------------------------------------------------------------------------------------------------------------------------------'
    if common.find_glob_path(TESTPATH + '/TestResult_*'):
        for i in common.find_glob_path(TESTPATH + '/TestResult_*'):
            try:
                exetime = i.replace(TESTPATH, '').replace('\\', '').replace('TestResult_', '')
                filepath = os.path.join(i, davincicsvfile)
                filepathnew = filepath.replace('.csv','') + '_Add_Logcat.csv'
                csv_insert_logcat_result(filepath, filepathnew)
                csv_reader(version, deviceid, arch, filepathnew, exetime)
            except Exception, ex:
                print ex
        print '\nCompleted the web app monkey tests:'
        print '------------------------------------------------------------------------------------------------------------------------------------'
        print 'Please get full test results in ' + testresultdir
    else:
        print 'No csv files found, please rerun the test.'
