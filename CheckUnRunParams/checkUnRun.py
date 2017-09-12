import subprocess
import time
import os
import re

# Build check regex
paramRegex = re.compile(r'\d.\d{4}')
dot2dRegex = re.compile(r'[.]')

# Initiate file objects
tempFile = open('./listPoints.txt', 'r')

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
                bashCommand = 'jobsub_submit --expected-lifetime=48h --memory=1350MB --role=Analysis --resource-provides=usage_model=DEDICATED,OPPORTUNISTIC -G minos -g file:///pnfs/minos/persistent/users/dphan/FeldmanCousinsAppearanceAnalysisDM' + dot2dRegex.sub('d', str(float(paramSearch[0]))) + '/GridGenStandard/analysisjob.sh ' + paramSearch[0] + ' ' + paramSearch[1] + ' ' + paramSearch[2] + ' ' + str(i)
                # print(bashCommand)
                process = subprocess.Popen(bashCommand, shell=True)
                time.sleep(10)

tempFile.close()
