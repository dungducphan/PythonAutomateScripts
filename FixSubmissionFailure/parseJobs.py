#!/usr/bin/python

import re
import os
import subprocess
import time

# Prepare REGEX for 'Error'
errorRegex = re.compile(r'Error')
filesRegex = re.compile(r'dm41 : (\d.\d{4}) -- ssq14 :   (\d.\d{4}) -- ssq24 :   (\d.\d{4}) -- fileIndex :  (\d) -- (\d{1,3})')

# Read job.out file
tempFile = open('./jobSubmit.out', 'r')

previousLine = ''
for line in tempFile:
    if 'str' in line:
        break
    else:
        errorSearch = errorRegex.search(line)
        if (errorSearch is not None):
            filesSearch = filesRegex.findall(previousLine)
            bashCommand = "echo \"dm41 : " + filesSearch[0][0] + " -- ssq14 : " + filesSearch[0][1] + " -- ssq24 : " + filesSearch[0][2] + " -- fileIndex : " + filesSearch[0][3] + " -- " + filesSearch[0][4] + " \" "
            process = subprocess.Popen(bashCommand, shell=True)
            bashCommand = "jobsub_submit --expected-lifetime=36h --memory=1500MB --role=Analysis --resource-provides=usage_model=DEDICATED,OPPORTUNISTIC -G minos -g file:///pnfs/minos/persistent/users/dphan/FeldmanCousinsAppearanceAnalysisDM0d004/NueFitStandard/analysisjob.sh " + filesSearch[0][0] + " " + filesSearch[0][1] + " " + filesSearch[0][2] + " " + filesSearch[0][3] + " " + filesSearch[0][4]
            process = subprocess.Popen(bashCommand, shell=True)
            time.sleep(10);
    previousLine = line

# Clean up
tempFile.close()
