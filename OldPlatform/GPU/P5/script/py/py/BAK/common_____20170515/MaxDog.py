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
import codecs


reload(sys)
sys.setdefaultencoding('utf-8')

class MaxLog():
    def __init__(self,taskId,cgVersion,logObj,logWork,jobName): 
              
            self.thread_stop = False
            self.RENDER_LOG=logObj
            userProFile=os.environ["userprofile"]
            userTempFile=os.environ["temp"]
            
            self.MAX_LOG=userProFile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+cgVersion.replace('3ds Max ','')+' - 64bit\\enu\\Network\\Max.log'
            self.VRAY_LOG=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
            
            renderLogDir=os.path.join(logWork,taskId)
            self.WORK_VRAY_LOG=os.path.join(renderLogDir,(jobName+'_vray.txt'))
            self.WORK_MAX_LOG=os.path.join(renderLogDir,(jobName+'_max.txt'))
        
            self.RENDER_LOG.info('[MonitorLog]'+self.MAX_LOG)
            self.RENDER_LOG.info('[MonitorLog]'+self.VRAY_LOG)
        
    def readFile(self,path):
        if os.path.exists(path):
            fileObject=open(path)
            line=fileObject.readlines()
            
            return line
        pass
        
    def writeFile(self,filePath,list,writeMode):
        fileObject=codecs.open(filePath,writeMode)
        for line in list :
            fileObject.write(line)
        fileObject.close()
        
    def do(self):
        if os.path.exists(self.MAX_LOG):
            self.RENDER_LOG.info('[MonitorLog].handle maxlog...')
            maxLoglist=self.readFile(self.MAX_LOG)
            self.writeFile(self.WORK_MAX_LOG,maxLoglist,'w')
            
        if os.path.exists(self.VRAY_LOG):
            self.RENDER_LOG.info('[MonitorLog].handle vraylog...')
            vrayLogList=self.readFile(self.VRAY_LOG)
            self.writeFile(self.WORK_VRAY_LOG,vrayLogList,'w')
        self.RENDER_LOG.info('[MonitorLog].sleep...')
    
    
class MonitorLog(threading.Thread):
    def __init__(self,interval,taskId,cgVersion,logObj,logWork,jobName): 
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        
        self.maxLog = MaxLog(taskId,cgVersion,logObj,logWork,jobName)
            

            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorLog-------------------------')    
        
            
        
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorLog].start...')
            self.maxLog.do()
            
            
            time.sleep(self.interval)
        self.RENDER_LOG.info('------------------------- end MonitorLog-------------------------')   
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[MonitorLog].stop...')
        try:
            print 'end'
            
        except Exception, e:
            print '[MonitorLog.err]'
            print e
            
            
class MonitorLMU(threading.Thread):
    def __init__(self,interval,taskId,jobName,nodeName,logObj,workCfg): 
            threading.Thread.__init__(self)
            self.interval = interval  
            self.thread_stop = False
            self.RENDER_LOG=logObj
            self.TASK_ID=taskId
            self.JOB_NAME=jobName
            self.NODE_NAME=nodeName
            self.WORK_CFG=workCfg
            
    def checkProcess(self,procName):
        try:
            file_handle = os.popen('tasklist /FI "IMAGENAME eq ' + procName + '"')
            file_content = file_handle.read()
            if file_content.find(procName) > -1:
                self.RENDER_LOG.info('[MonitorLMU]....LMU EXISTS...')
                #sys.exit(-5)
            else:
                self.RENDER_LOG.info('[MonitorLMU]....LMU NOT EXISTS...')
                
        except BaseException,e:
            print str(e)
            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorLMU-------------------------')    
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorLMU].checkProcess...')
            self.checkProcess('LMU.exe')
            self.RENDER_LOG.info('[MonitorLMU].sleep...')
            time.sleep(self.interval)
        self.RENDER_LOG.info('------------------------- end MonitorLMU-------------------------')   
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[MonitorLMU].stop...')
        try:
            print 'end'
            
        except Exception, e:
            print '[MonitorLMU.err]'
            print e
            
            
class MonitorMaxThread(threading.Thread):

    def __init__(self,interval,taskId,jobName,nodeName,logObj,workCfg):  
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.TASK_ID=taskId
        self.JOB_NAME=jobName
        self.NODE_NAME=nodeName
        self.WORK_CFG=workCfg
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        
        self.RENDER_LOG.info('------------------------- start monitor dog-------------------------')
        
        
        tempTxt=os.path.join(self.WORK_CFG,'temp.txt').replace('\\','/')
        tempBat=os.path.join(self.WORK_CFG,'temp.bat').replace('\\','/')
        

        
        while not self.thread_stop:
            try:
                
                self.RENDER_LOG.info('____dog___')
                #os.system('echo fvok----------->>'+tempTxt)
                
                if os.path.exists(tempBat):
                    self.RENDER_LOG.info('run temp.bat')
                    os.system(tempBat+'>>'+tempTxt)
                    
                self.RENDER_LOG.info('sleep...')
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
            

            