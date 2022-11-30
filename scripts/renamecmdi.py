#!/usr/bin/env python3

import os
# import sys
import re
import shutil
from glob import glob

currentfile = os.path.dirname(os.path.realpath(__file__))
destpath = currentfile + "/trans/"
os.makedirs(destpath, exist_ok=True)

dir_path = currentfile + "/records/inprogress/"
# print(dir_path)
lijst = glob(dir_path + '*')
p = re.compile('.*?/md(\d\d?)')

for dir in lijst:
    print(dir)
    l = p.findall(dir)
    print(l[0])
    shutil.copyfile(dir + '/metadata/record.cmdi', destpath + l[0] + '.cmdi')