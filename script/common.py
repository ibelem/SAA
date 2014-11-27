# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import shutil

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

def del_folder(path):
    shutil.rmtree(path)