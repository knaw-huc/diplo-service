#!/usr/bin/env python3

import os
import sys
import re

fn = sys.argv[1]
if os.path.exists(fn):
    fr = open(os.path.abspath(fn), 'r')    
    lines = fr.readlines()


# print(lines)
# exit
filedest = open('conv_' + fn , 'w')

# REGEXP for timestamp and speaker
idcue = re.compile('^\d+?$')
timestamp = re.compile('^\d\d\:\d\d\:.*')
speaker = re.compile('^(.+?)\:')

speakeralert = 'no'
for line in lines:
    if idcue.search(line):
        # print('1 ' + line)
        # line = ""
        # filedest.write(line)
        continue
    else:
        if(speakeralert == 'yes' and speaker.match(line)):
            search = speaker.findall(line)
            newspeaker = '<v ' + search[0] + '>'
            line = newspeaker    # no newline that's what we want
    
        speakeralert = 'no'

        if(timestamp.match(line)):
            speakeralert = 'yes'
        
        filedest.write(line)