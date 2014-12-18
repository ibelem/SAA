# -*- coding: utf-8 -*-
#!/usr/bin/env python

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

import os, sys
import re, codecs
import shutil, glob
import json


def multi_replace(string, dic):
    rx = re.compile('|'.join(map(re.escape, dic)))
    def one_xlat(match):
        return dic[match.group(0)]
    return rx.sub(one_xlat, string)

def rename_file(dir, na, nb):
    files = os.listdir(dir)
    for i in files:
        if i.find(na) > -1:
            f_path = dir + os.sep + i
            if os.path.isfile(f_path):
                os.rename(f_path, dir + os.sep + i.replace(na,nb))

def del_files(path, ext):
    for root , dirs, files in os.walk(path):
        for name in files:
            if name.endswith(ext):
                os.remove(os.path.join(root, name))

def del_dir(path):
    shutil.rmtree(path)

def find_file(pathname):
    return _find(pathname)

def find_dir(path):
    return _find(path, matchFunc=os.path.isdir)

def mk_dir(path):
    if not find_dir(path):
        os.mkdir(path)

#class Error(Exception): False
def _find(pathname, matchFunc=os.path.isfile):
    for dirname in sys.path:
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
    #raise Error("##### Can't find file %s" % pathname)

def find_glob_path(filepath):
    return glob.glob(filepath)

def remove_glob_path(filepath):
    if find_glob_path(filepath):
        for path in glob.glob(filepath):
            os.remove(path)

def find_text_in_file(str, filepath):
    count = 0
    reader = open(filepath, "r+")
    line = reader.readline()#读取第一行数据
    while line != '' and line != None:#循环读取数据行
        li = re.findall(str, line)
        count = count + len(li)
        line = reader.readline()
    reader.close()
    return count

def copy_tree(sourceDir,  targetDir):
    shutil.copytree(sourceDir,  targetDir)

def copy_file(sourceDir,  targetDir):
    shutil.copy(sourceDir,  targetDir)

def copy_files(sourceDir,  targetDir):
     if sourceDir.find(".git") > 0:
         return
     for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         if os.path.isfile(sourceFile):
             if not os.path.exists(targetDir):
                 os.makedirs(targetDir)
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                     open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile):
             First_Directory = False
             copy_files(sourceFile, targetFile)

def parse_config_json(pathname, field):
    fp = open(pathname)
    reader = fp.read()
    d = json.loads(reader, strict=False)
    if field.startswith('device_'):
        t = []
        for var in d['device']:
            t.append(var[field])
        return t
    if field.startswith('rtlib_'):
        t = []
        for var in d['runtimelib_test_build']:
            t.append(var[field])
        return t
    elif field.startswith('davinci_'):
        return d['davinci'][field]
    elif field.startswith('runtimelib_'):
        return d['runtimelib'][field]
    elif field.startswith('test_suite_'):
        return d['test_suite'][field]
    elif field.startswith('test_result_'):
        return d['test_result'][field]
    else:
        for var in d:
            value = d[field]
            return value



