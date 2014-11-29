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
import re
import shutil
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

def _find(pathname, matchFunc=os.path.isfile):
    for dirname in sys.path:
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
        else:
            return False

def parse_config_json(pathname, field):
    fp = open(pathname)
    reader = fp.read()
    d = json.loads(reader, strict=False)
    if field == 'device_id' or field == 'device_name':
        t = []
        for var in d['device']:
            t.append(var[field])
        return t
    else:
        for var in d:
            value = d[field]
            return value



