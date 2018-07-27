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


class DogUtil():

    @staticmethod
    def RBLog(logStr,myLog=None):
        if myLog==None:
            print logStr
        else:
            myLog.info(logStr)
    
    @staticmethod
    def maxCmd(cmdStr,myLog=None):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        DogUtil.RBLog(cmdStr,myLog)
        cmdp=subprocess.Popen(cmdStr,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break   
            DogUtil.RBLog(buff)
            if '[End maxscript render]' in buff:
                try:
                    os.system('taskkill /F /IM 3dsmax.exe /T')
                except  Exception, e:
                    DogUtil.RBLog('taskkill 3dsmax.exe exeception')  
                    DogUtil.RBLog(e)  
                try:
                    os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
                except  Exception, e:
                    DogUtil.RBLog('taskkill 3dsmaxcmd.exe exeception')  
                    DogUtil.RBLog(e)          
        resultCode = cmdp.returncode
        return resultCode
        
        
    @staticmethod
    def runCmd(cmd,myLog=None):
        print 'cmd='+cmd
        cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break   
            if myLog!=None :
                myLog.info(buff)
            # self.G_RENDERCMD_LOGGER.info(buff)
            # self.G_PROCESS_LOGGER.info(buff)          
        resultCode = cmdp.returncode
        return resultCode
        
        
        
        
    @staticmethod
    def restartWin(progressLog):
        progressLog.info('MaxLogDEBUG_restartWin')            
        try:
            os.system('shutdown /r /t 0')
        except  Exception, e:
            progressLog.info('MaxLogDEBUG_restartWin exeception')  
            progressLog.info(e)
            
    @staticmethod
    def killMax(progressLog):
        progressLog.info('MaxLogDEBUG_TASKKILL_3DSMAXCMD')            
        try:
            os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
        except  Exception, e:
            progressLog.info('MaxLog2taskkill 3dsmaxcmd.exe exeception')  
            progressLog.info(e) 
        
        
        progressLog.info('MaxLogDEBUG_TASKKILL_3DSMAX')
        try:
            os.system('taskkill /F /IM 3dsmax.exe /T')
        except  Exception, e:
            progressLog.info('MaxLog2taskkill 3dsmax.exe exeception')  
            progressLog.info(e) 
            
    @staticmethod
    def checkProcess(procName):
        try:
            file_handle = os.popen('tasklist /FI "IMAGENAME eq ' + procName + '"')
            file_content = file_handle.read()
            if file_content.find(procName) > -1:
                return True
            else:
                return False
        except BaseException,e:
            print str(e)
            return False  
            
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
    
        maxLoglist=[]
        vrayLogList=[]
        if os.path.exists(self.MAX_LOG):
            self.RENDER_LOG.info('[MonitorLog].handle maxlog...')
            maxLoglist=self.readFile(self.MAX_LOG)
            self.writeFile(self.WORK_MAX_LOG,maxLoglist,'w')
            
        if os.path.exists(self.VRAY_LOG):
            self.RENDER_LOG.info('[MonitorLog].handle vraylog...')
            vrayLogList=self.readFile(self.VRAY_LOG)
            self.writeFile(self.WORK_VRAY_LOG,vrayLogList,'w')
            
            
                    
        self.RENDER_LOG.info('[MonitorLog].sleep...')
        return maxLoglist,vrayLogList
        
    
    
class MonitorLog(threading.Thread):
    def __init__(self,interval,taskId,cgVersion,logObj,feeLog,logWork,jobName): 
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.FEE_LOG=feeLog
        
        self.maxLog = MaxLog(taskId,cgVersion,logObj,logWork,jobName)
            

            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorLog-------------------------')    
        
            
        
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorLog].start...')
            maxLogList,vrayLogList=self.maxLog.do()
            
            error1='Error loading irradiance map: File format error'
            error2='error: Could not load irradiance map'
            for vrayLogLine in vrayLogList:
                if error1 in vrayLogLine:
                    self.RENDER_LOG.info('')
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------')
                    self.RENDER_LOG.info('[error]'+error1)
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------\r\n')
                    self.FEE_LOG.info('jobStatus='+error1)
                    DogUtil.killMax(self.RENDER_LOG)
                    
                    sys.exit(-1)
            
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
                return True
                #sys.exit(-5)
            else:
                self.RENDER_LOG.info('[MonitorLMU]....LMU NOT EXISTS...')
                return False
                
        except BaseException,e:
            print str(e)
            return False
            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorLMU-------------------------')    
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorLMU].checkProcess...')
            lmuChecked=self.checkProcess('LMU.exe')
            if lmuChecked:
                DogUtil.killMax(self.RENDER_LOG)
                DogUtil.restartWin(self.RENDER_LOG)
                sys.exit(-1)
                
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
        
    def getMaxInfo(self,cmd):
        print 'cmd='+cmd
        cpuStr=''
        memoryStr=''
        cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break   
            if buff!=None  and ('|' in buff):
                cpuMem=buff.strip().strip('\r').strip('\n')
                cpuMemArr = cpuMem.split('|')
                cpuStr = cpuMemArr[0]
                memoryStr=cpuMemArr[1]
        return cpuStr,memoryStr
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        
        self.RENDER_LOG.info('------------------------- Start MonitorMax -------------------------')
        
        
        tempTxt=os.path.join(self.WORK_CFG,'temp.txt').replace('\\','/')
        tempBat=os.path.join(self.WORK_CFG,'temp.bat').replace('\\','/')
        
        processExe=r'b:/tools/process_utility.exe'
        processExe2=r'c:/process_utility.exe'
        shutil.copy(processExe,processExe2)
        checkProcessCmd=processExe2+' "3dsmax.exe"'
        
        while not self.thread_stop:
            try:
                
                self.RENDER_LOG.info('[MonitorMax].___MonitorMaxThread____')
                #os.system('echo fvok----------->>'+tempTxt)
                
                if os.path.exists(tempBat):
                    self.RENDER_LOG.info('run temp.bat')
                    os.system(tempBat+'>>'+tempTxt)
                
                cpuInfo,memoryInfo=self.getMaxInfo(checkProcessCmd)
                self.RENDER_LOG.info('[MonitorMax].Cpu='+cpuInfo+'% Memory='+memoryInfo)
                self.RENDER_LOG.info('[MonitorMax].sleep...')
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
            

            