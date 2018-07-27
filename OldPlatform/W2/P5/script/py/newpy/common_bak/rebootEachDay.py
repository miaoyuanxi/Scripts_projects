# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 18:30:58 2014

@author: hyc
"""


import sys
import subprocess
import time
import os,sys

# set the interval time for rebooting, the unit is 'hour'
rebootTime = 24


def uptime():
    """Returns the uptime in a Windows machine"""

    if not sys.platform.startswith('win'):
        raise RuntimeError, 'This function is to be used in windows only'
    cmd = 'net statistics server'
    p = subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (child_stdin, child_stdout) = (p.stdin, p.stdout)
    lines = child_stdout.readlines()
    child_stdin.close()
    child_stdout.close()
    lines = [line.strip() for line in lines if line.strip()]
    startDate, startTime = lines[1].split()[2:4]
    timeArray = time.strptime( startDate + ' ' + startTime, '%Y/%m/%d %H:%M:%S' )
    
    upTime = time.mktime( timeArray )
    
    return upTime



if __name__ == '__main__':
    now = time.time()
    uptime = uptime()
    if now - uptime > rebootTime * 3600 :
        print 'window will reboot in 2 seconds.'
        os.system('TASKKILL /F /IM enf*.exe /T')
        time.sleep(10)
        os.system( 'shutdown -r -t 2' )
        time.sleep(10)
        #sys.exit(-1)
    else:
        print 'computer uptime less than ', rebootTime, ' hours: ', str( (now - uptime)/3600 ),' hours'








