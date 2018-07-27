#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time
import shutil
import threading
import time


reload(sys)
sys.setdefaultencoding('utf-8')



class MonitorMaxThread(threading.Thread):

    def __init__(self,interval,taskId,jobName,nodeName,logObj):  
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.TASK_ID=taskId
        self.JOB_NAME=jobName
        self.NODE_NAME=nodeName

        
    def cmd(self,cmdStr,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print cmdStr
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        while True:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine == '' and cmdp.poll()!=None:
                break
            if resultLine!='':
                self.RENDER_LOG.info(resultLine)
        
        resultStr = cmdp.stdout.read()
        #print resultStr
        resultCode = cmdp.returncode
        return resultStr
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        
        self.RENDER_LOG.info('------------------------- start monitor dog-------------------------')
        while not self.thread_stop:
            try:
                
                processCmd='wmic process where name="3dsmax.exe" get Name,CreationDate,WorkingSetSize'
                self.cmd(processCmd)
                time.sleep(self.interval)
            except Exception, e:
                print '[MonitorMaxThread.err]'
                print e
                self.RENDER_LOG.info(e)
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[MonitorMaxThread].stop...')
        try:
            print 'end'
            
        except Exception, e:
            print '[MonitorMaxThread.err]'
            print e
            

            