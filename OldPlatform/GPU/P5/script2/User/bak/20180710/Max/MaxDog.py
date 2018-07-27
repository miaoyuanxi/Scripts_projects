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
            DogUtil.RBLog(buff,myLog)
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
        
    #kill 3dsmax.exe,3dsmaxcmd.exe,vrayspawner*.exe
    @staticmethod
    def killMaxVray(progressLog):
        progressLog.info('[killMaxVray start]')
        try:
            os.system('taskkill /F /FI "IMAGENAME eq vrayspawner*" /T')
        except Exception as e:
            progressLog.info('kill vrayspawner*.exe exception')
            progressLog.info(e)
        try:
            os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
        except Exception as e:
            progressLog.info('kill 3dsmaxcmd.exe exception') 
            progressLog.info(e)
        try:
            os.system('taskkill /F /IM 3dsmax.exe /T')
        except  Exception as e:
            progressLog.info('kill 3dsmax.exe exception') 
            progressLog.info(e)
        progressLog.info('[killMaxVray end]')
        
    @staticmethod
    def killMaxadapter(progressLog):
        progressLog.info('MaxLogDEBUG_TASKKILL_MAXADAPTER')            
        try:
            os.system('taskkill /F /IM maxadapter.adp.exe /T')
        except  Exception, e:
            progressLog.info('MaxLog2taskkill maxadapter.adp.exe exeception')  
            progressLog.info(e) 
        
class MaxLog():
    def __init__(self,taskId,cgVersion,logObj,logWork,jobName): 
              
            self.thread_stop = False
            self.RENDER_LOG=logObj
            
            userProFile=os.environ["userprofile"]
            userTempFile=os.environ["temp"]
            
            self.MAX_LOG=userProFile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+cgVersion.replace('3ds Max ','')+' - 64bit\\enu\\Network\\Max.log'
            self.VRAY_LOG=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
            
            renderLogDir=os.path.join(logWork,taskId)
            self.WORK_VRAY_LOG=os.path.join(renderLogDir,(jobName+'_vray2.txt'))
            self.WORK_MAX_LOG=os.path.join(renderLogDir,(jobName+'_max2.txt'))
            self.WORK_NEW_RENDER_LOG=os.path.join(renderLogDir,(jobName+'_render.log'))
            
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
            self.writeFile(self.WORK_NEW_RENDER_LOG,["\n\n======================================================================maxlog======================================================================\n\n"],'w')
            self.writeFile(self.WORK_NEW_RENDER_LOG,maxLoglist,'a+')
            
        if os.path.exists(self.VRAY_LOG):
            self.RENDER_LOG.info('[MonitorLog].handle vraylog...')
            vrayLogList=self.readFile(self.VRAY_LOG)
            self.writeFile(self.WORK_VRAY_LOG,vrayLogList,'w')
            self.writeFile(self.WORK_NEW_RENDER_LOG,["\n\n======================================================================vraylog======================================================================\n\n"],'a+')
            self.writeFile(self.WORK_NEW_RENDER_LOG,vrayLogList,'a+')
            
                    
        self.RENDER_LOG.info('[MonitorLog].sleep...')
        return maxLoglist,vrayLogList
        
    
    
class MonitorLog(threading.Thread):
    def __init__(self,interval,taskId,cgVersion,logObj,feeLog,logWork,jobName,munuTaskId,munuJobId,monitorLogList,feeDir,**kwargs): 
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.FEE_LOG=feeLog
        self.TASK_ID=taskId
        self.MUNU_TASK_ID = munuTaskId
        self.MUNU_JOB_ID = munuJobId
        self.LOG_LIST = monitorLogList
        self.FEE_DIR = feeDir
        self.MAX_VRAY_DISTRIBUTE = False  
        if kwargs.has_key('max_vray_distribute'):
            self.MAX_VRAY_DISTRIBUTE = kwargs['max_vray_distribute']
        self.RENDER_WORK_TASK = os.path.join('C:/work/render', self.TASK_ID)
        if kwargs.has_key('render_work_task'):
            self.RENDER_WORK_TASK = kwargs['render_work_task']
        self.maxLog = MaxLog(taskId,cgVersion,logObj,logWork,jobName)
            

            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorLog-------------------------')    
        
            
        
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorLog].start...')
            maxLogList,vrayLogList=self.maxLog.do()
            
            error1='Error loading irradiance map: File format error'
            error2='error: Could not load irradiance map'
            # error3='warning: Could not connect to host'
            error4='warning: Error loading irradiance map: Error opening file'
            error5='Connection timeout'
            error6='No connection could be made because the target machine actively refused it'
            error7='is not responding'
            for vrayLogLine in vrayLogList:
                if error1 in vrayLogLine:
                    self.RENDER_LOG.info('')
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------')
                    self.RENDER_LOG.info('[error]'+error1)
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------\r\n')
                    self.FEE_LOG.info('jobStatus='+error1)
                    DogUtil.killMax(self.RENDER_LOG)
                    
                    sys.exit(-1)
                    
                # if error3 in vrayLogLine:
                    # self.RENDER_LOG.info('')
                    # self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------')
                    # self.RENDER_LOG.info('[error]'+error3)
                    # self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------\r\n')
                    # self.FEE_LOG.info('jobStatus='+error3)
                    # DogUtil.killMax(self.RENDER_LOG)
                    
                    # sys.exit(-1)
                
                if error4 in vrayLogLine:
                    self.RENDER_LOG.info('')
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------')
                    self.RENDER_LOG.info('[error]'+error4)
                    self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------\r\n')
                    self.FEE_LOG.info('jobStatus='+error4)
                    DogUtil.killMax(self.RENDER_LOG)
                    
                    sys.exit(-1)
                
                if self.MAX_VRAY_DISTRIBUTE and False:  # it doesn't exit the task, even if a node is dropped
                    if error5 in vrayLogLine:
                        error_message = error5
                    elif error6 in vrayLogLine:
                        error_message = error6
                    elif error7 in vrayLogLine:
                        error_message = error7
                    else:
                        error_message = ''
                    if error_message:
                        self.LOG_LIST.append(vrayLogLine)  #for main thread exit
                        #write flag
                        #### flag_dir = ur'B:\plugins\max\distribute_problem'
                        ###flag_dir = os.path.join(self.FEE_DIR,'distribute_problem')
                        ###if not os.path.exists(flag_dir):
                        ###    os.makedirs(flag_dir)
                        ###flag_name = self.TASK_ID + '_'+self.MUNU_TASK_ID + '_'+self.MUNU_JOB_ID + '_' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '_' + error_message + '.log'
                        ###flag_file = os.path.normpath(os.path.join(flag_dir,flag_name))
                        ###with codecs.open(flag_file,'w','utf-8') as f:
                        ###    f.write(vrayLogLine)
                        
                        # flag_dir = ur'C:\work\render\<task_id>'
                        flag_dir = self.RENDER_WORK_TASK
                        if not os.path.exists(flag_dir):
                            os.makedirs(flag_dir)
                        flag_name = self.TASK_ID + '_'+self.MUNU_TASK_ID + '_'+self.MUNU_JOB_ID + '_' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '_' + error_message + '.log'
                        flag_file = os.path.normpath(os.path.join(flag_dir,flag_name))
                        with codecs.open(flag_file,'w','utf-8') as f:
                            f.write(vrayLogLine)
                            
                        self.RENDER_LOG.info('')
                        self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------')
                        self.RENDER_LOG.info('[error]'+error_message)
                        self.RENDER_LOG.info('-------------------------------------------------------------------------------------------------\r\n')
                        self.FEE_LOG.info('jobStatus='+error_message)
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
            
            
class MonitorMaxadapter(threading.Thread):
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
                self.RENDER_LOG.info('[MonitorMaxadapter]....Maxadapter EXISTS...')
                return True
                #sys.exit(-5)
            else:
                self.RENDER_LOG.info('[MonitorMaxadapter]....Maxadapter NOT EXISTS...')
                return False
                
        except BaseException,e:
            print str(e)
            return False
            
    def run(self): #Overwrite run() method, put what you want the thread do here 
        self.RENDER_LOG.info('------------------------- start MonitorMaxadapter-------------------------')    
        while not self.thread_stop:
            self.RENDER_LOG.info('[MonitorMaxadapter].checkProcess...')
            maxadapterChecked=self.checkProcess('maxadapter.adp.exe')
            if maxadapterChecked:
                DogUtil.killMaxadapter(self.RENDER_LOG)
                # sys.exit(-1)
                
            self.RENDER_LOG.info('[MonitorMaxadapter].sleep...')
            time.sleep(self.interval)
        self.RENDER_LOG.info('------------------------- end MonitorMaxadapter-------------------------')   
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[MonitorMaxadapter].stop...')
        try:
            print 'end'
            
        except Exception, e:
            print '[MonitorMaxadapter.err]'
            print e
            