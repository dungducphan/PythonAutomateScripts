#!/usr/bin/python

import re
import os
import subprocess

# Prepare REGEX for 'Error'
filesRegex = re.compile(r'\d{6,9}.\d@fifebatch[1,2].fnal.gov')

# Read job.out file
tempFile = open('./jobIDsToRemove.out', 'r')

for line in tempFile:
    if 'str' in line:
        break
    else:
        filesSearch = filesRegex.findall(line)
        if (filesSearch is not None):
            bashCommand = "echo \"jobsub_rm --jobid=" + filesSearch[0] + "\""
            process = subprocess.Popen(bashCommand, shell=True)
            bashCommand = "jobsub_rm --jobid=" + filesSearch[0]
            process = subprocess.Popen(bashCommand, shell=True)
# Clean up
tempFile.close()
