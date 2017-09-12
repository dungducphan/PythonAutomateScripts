import subprocess
import time
import os
import re

# Build check regex
paramRegex = re.compile(r'\d.\d{4}')

# Initiate file objects
tempFile = open('./listPoints.txt', 'r')
listFile = open('./listPointsUnRun.txt', 'w')

for line in tempFile:
    if 'str' in line:
        break
    else:
        paramSearch = paramRegex.findall(line)
        for i in range(0, 5):
            fileToCheck = 'gridfile_dm_' + paramSearch[0] + '_ssq14_' + paramSearch[1] + '_ssq24_' + paramSearch[2] + '_' + str(i) + '.root'
            bashCommand = 'ls ./Output/' + fileToCheck
            process = subprocess.Popen(bashCommand, shell=True, stdout = subprocess.PIPE)
            if (process.stdout.read() != ''):
                pass
            else:
                listFile.write(paramSearch[0] + ', ' + paramSearch[1] + ', ' + paramSearch[2] + ', ' + str(i) + '\n')

tempFile.close()
listFile.close()
