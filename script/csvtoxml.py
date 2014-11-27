# -*- coding: utf-8 -*-
import os,sys
import csv

__author__ = 'zhangmin'

SUITEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
TESTPATH = os.path.join(SUITEPATH,'tests')

def csv_reader(filepath):
    dreader = csv.DictReader(open(filepath))
    #print len(list(dreader))
    for c in dreader:
        print c['TestTime'], c['DeviceName'], c['Application'], c['Package'], c['Activity']
        print c['Install'], c['Launch'], c['Random'], c['Back'], c['Uninstall'], c['Result'], c['FailReason'], c['ReportLink']

def generate_xml_report():
    print 'todo'

def csv_xml():
    csv_reader(os.path.join(TESTPATH,'Smoke_Test_Report.csv'))