# -*- coding: utf-8 -*-

import os,sys
import socket, codecs
from datetime import *
import csv, openpyxl
import common, gl
from lxml import etree as et

# https://pypi.python.org/pypi/lxml/3.4.1

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')
SCRIPTPATH = os.path.join(SUITEPATH,'script')
RESULTPATH = os.path.join(SUITEPATH,'result')
JSONPATH = os.path.join(SCRIPTPATH, 'config.json')

davincicsvfile = common.parse_c_json(JSONPATH, 'davinci_csv_file')
testresultdir = common.parse_c_json(JSONPATH, 'test_result_dir')
rnr = common.parse_c_json(JSONPATH, 'davinci_rnr_log_dir')

rnrtmpdir = os.path.join(TESTPATH, rnr)

def l(str):
    common.log_info(str, gl.__logfile__)

def lr(str):
    common.log_err(str, gl.__logfile__)

def copy_result(deviceid, exetime):

    # Copy <deviceid> of DaVinci (Crosswalk xml result) from <test_suite>/tests to <test_result_dir> defined in config.json
    if not common.find_dir(testresultdir):
        common.mk_dir(testresultdir)
    try:
        common.copy_tree(os.path.join(TESTPATH, deviceid), os.path.join(testresultdir, deviceid))
    except Exception, ex:
        common.copy_files(os.path.join(TESTPATH, deviceid), os.path.join(testresultdir, deviceid))

    # Copy TestResult_<datetime> of DaVinci from <test_suite>/tests to <test_result_dir> defined in config.json
    tr = 'TestResult_' + exetime
    try:
        common.copy_tree(os.path.join(TESTPATH, tr), os.path.join(testresultdir, tr))
    except Exception, ex:
        common.copy_files(os.path.join(TESTPATH, tr), os.path.join(testresultdir, tr))

    # Copy _DaVinci_RnR_Logs of DaVinci from <test_suite>/tests to <test_result_dir> defined in config.json
    try:
        common.copy_tree(os.path.join(TESTPATH, rnr), os.path.join(testresultdir, rnr))
    except Exception, ex:
        common.copy_files(os.path.join(TESTPATH, rnr), os.path.join(testresultdir, rnr))

    # Copy result_<date>_<time>.log of DaVinci from <test_suite>/result to <test_result_dir> defined in config.json
    try:
        common.copy_tree(RESULTPATH, testresultdir)
    except Exception, ex:
        common.copy_files(RESULTPATH, testresultdir)

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
            l(c['Install'] + ' ' + c['Launch'] + ' ' + c['Random'] + ' ' + c['Back']
              + ' ' + c['Uninstall'] + ' ' + c['Logcat'] + ' ' + c['Result'] + ' ' + c['Reason'].strip())

            devicemode = ''
            try:
                devicemode = c['Device Model']
            except Exception, ex:
                lr(str(ex))

            application = ''
            try:
                application = c['Application'].decode('utf-8').replace('.apk','')
            except Exception, ex:
                application = c['\xef\xbb\xbfApplication'].decode('utf-8').replace('.apk','')
            applicationname = ''
            try:
                applicationname = c['App name']
            except Exception, ex:
                lr(str(ex))
            package = ''
            try:
                package = c['Package name']
            except Exception, ex:
                lr(str(ex))
            for i in ['Install', 'Launch', 'Random', 'Back', 'Uninstall', 'Logcat']:
                result = c[i]
                if result.lower() == 'skip':
                    result = 'BLOCK'
                insert_xml_case_result(version, deviceid, arch, q, testtime, application, applicationname, package, i.lower(), result, c['Reason'].strip(), reportlink.strip())
        copy_result(deviceid, exetime)
    else:
        l('Can\'t find file: ' + filepath)

def insert_xml_case_result(version, deviceid, arch, q, testtime, application, applicationname, package, step, result, failreason, reportlink):
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
    testcase.attrib['id'] = 'topapp_smoke_'+ application.lower() + '_' + step
    testcase.attrib['purpose'] = 'Verify ' + step + ' step of ' + applicationname + ' works correctly'
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

    wb = openpyxl.load_workbook(filename=filepath, use_iterators=True)
    ws = wb.get_sheet_by_name('all app result')

    fields_new = ['Application', 'App name', 'Package name', 'Device Model',
                  'Android Version', 'Device Build Number', 'App Version',
                  'Install', 'Launch', 'Random', 'Back', 'Uninstall', 'Logcat',
                  'Result', 'Reason', 'Link']
    writer = csv.DictWriter(open(filepathnew, "wb"), fieldnames=fields_new)
    writer.writeheader()

    data_dic = {}
    for rx in range(ws.get_highest_row()):
        temp_list = []
        r = rx + 1
        wapplication = ws.cell(row = r, column = 1).value
        wappname = ws.cell(row = r, column = 2).value
        wpackagename = ws.cell(row = r, column = 3).value
        wdevicemodel = ws.cell(row = r, column = 4).value
        wandroidversion = ws.cell(row = r, column = 5).value
        wdevicebuildnumber = ws.cell(row = r, column = 6).value
        wappversion = ws.cell(row = r, column = 7).value
        winstall = ws.cell(row = r, column = 8).value
        wlaunch = ws.cell(row = r, column = 9).value
        wrandom = ws.cell(row = r, column = 10).value
        wback = ws.cell(row = r, column = 11).value
        wuninstall = ws.cell(row = r, column = 12).value
        wresult = ws.cell(row = r, column = 13).value
        wreason = ws.cell(row = r, column = 14).value
        wlink = ws.cell(row = r, column = 15).value

        wlogcat = 'Logcat'
        if r > 1:
            wlogcat = check_logcat_result(filepath, wpackagename)
            temp_dict = {'Application': wapplication, 'App name': wappname, 'Package name': wpackagename, 'Device Model': wdevicemodel,
                         'Android Version': wandroidversion, 'Device Build Number': wdevicebuildnumber, 'App Version': wappversion,
                         'Install': winstall, 'Launch': wlaunch, 'Random': wrandom, 'Back': wback, 'Uninstall': wuninstall,
                         'Logcat': wlogcat, 'Result': wresult, 'Reason': wreason, 'Link': wlink}
            writer.writerow(temp_dict)

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
    l('Start to handle CSV and XML results:')
    l('------------------------------------------------------------------------------------------------------------------------------------')
    if common.find_glob_path(TESTPATH + '/TestResult_*'):
        for i in common.find_glob_path(TESTPATH + '/TestResult_*'):
            try:
                exetime = i.replace(TESTPATH, '').replace('\\', '').replace('TestResult_', '')
                filepath = os.path.join(i, davincicsvfile)
                filepathnew = filepath.replace('.xlsx','') + '_Add_Logcat.csv'
                csv_insert_logcat_result(filepath, filepathnew)
                csv_reader(version, deviceid, arch, filepathnew, exetime)
            except Exception, ex:
                lr(str(ex))
        l('Completed the top app smoke tests:')
        l('------------------------------------------------------------------------------------------------------------------------------------')
        l('Please get full test results in ' + testresultdir)
    else:
        lr('No csv files found, please rerun the test.')
