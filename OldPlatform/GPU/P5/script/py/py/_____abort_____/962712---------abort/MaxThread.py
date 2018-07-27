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
from PIL import Image   
from PIL import ImageGrab
import PIL
import psutil

reload(sys)
sys.setdefaultencoding('utf-8')

class MaxThread(threading.Thread):

    def __init__(self,interval,taskId,jobName,nodeName,workTask,grabOutput,logObj):  
        threading.Thread.__init__(self)
        self.interval = interval  
        self.thread_stop = False
        self.RENDER_LOG=logObj
        self.TASK_ID=taskId
        self.JOB_NAME=jobName
        self.NODE_NAME=nodeName
        self.WORK_TASK=workTask
        self.GRAB_OUTPUT=grabOutput
        self.grabImgName='grabImg1.3.exe'
        #self.PLUGINS_MAX_SCRIPT='B:/plugins/max2'
        self.W=600
        self.H=600
        self.getWorkArea()
    def checkProcess(self,processName):
        '''
        getMaxCmd='tasklist /fi "imagename eq 3dsmax.exe"'
        cmdResult=self.cmd(getMaxCmd)
        self.RENDER_LOG.info(cmdResult)
        try:
            if '3dsmax.exe' in cmdResult:
                return True
            else:
                return False
        except:
            return False
            
        '''
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == processName.lower():
                    return True  # return if found one
            except psutil.AccessDenied:
                pass
            except psutil.NoSuchProcess:
                pass
        return False
        
    def getCPUstate(self,interval=1):  
        return  str(psutil.cpu_percent(interval))
         
    def getMemorystate(self):   
        phymem = psutil.virtual_memory()  
        line = str(phymem.percent)
        return line   
        
    def grabPic(self,grapImg):

        if self.checkProcess('3dsmax.exe'):
            print 'grab  workarea'
            im=ImageGrab.grab((0,0,self.W,self.H))
            im.save(grapImg)
            
    def getWorkArea(self):
        self.RENDER_LOG.info('[getWorkArea].start')
        workAreaExe='b:/tools/workarea.exe'
        try:
            if os.path.exists(workAreaExe):
                workArea=self.cmd(workAreaExe)
                print 'workArea...',workArea
                if workArea!=None and workArea!='':
                    arr=workArea.split(',')
                    if len(arr)==2:
                        self.W=int(arr[0].strip())
                        self.H=int(arr[1].strip())
        except Exception, e:
            self.RENDER_LOG.info(e)
        self.RENDER_LOG.info('[getWorkArea].end')
        
    def moveToServer(source,target):
        moveCmd=r'c:\fcopy\FastCopy.exe /cmd=move /speed=full /force_close /no_confirm_stop /force_start "'+source +'" /to="'+target+'"'
        self.cmd(moveCmd,False)
        
    def grabRun(self,nodeName,output):
        try:
           
            if not os.path.exists(output):
                os.makedirs(output)
            currentTime= time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
            cpu= self.getCPUstate()
            mem= self.getMemorystate()
            grapImgName=nodeName+'_'+currentTime+'_'+cpu+'_'+mem+'.jpg'
            grapImg=os.path.join(output,grapImgName)
            self.RENDER_LOG.info(grapImg)
            self.grabPic(grapImg.replace('\\','/'))
        except Exception, e:
            print 'grab exception'
            self.RENDER_LOG.info(e)

    def cmd(self,cmdStr,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print cmdStr
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        
        while cmdp.poll()!=None:
            resultLine = cmdp.stdout.readline().strip()
        resultStr = cmdp.stdout.read()
        #print resultStr
        resultCode = cmdp.returncode
        return resultStr
        
    def moveToServer(self,source,target):
        moveCmd=r'c:\fcopy\FastCopy.exe /cmd=move /speed=full /force_close /no_confirm_stop /force_start "'+source +'" /to="'+target+'"'
        self.cmd(moveCmd,False)
    
    def run(self): #Overwrite run() method, put what you want the thread do here  
        time.sleep(10)
        
        self.RENDER_LOG.info('start loop grab')
        while not self.thread_stop:
            try:
                self.RENDER_LOG.info('-------------------------grabimg start-------------------------')
                str='[MaxThread]_start.'+self.TASK_ID+'...'+self.JOB_NAME+'...'+self.GRAB_OUTPUT
                print str
                self.RENDER_LOG.info(str)
                workGrab=os.path.join(self.WORK_TASK,'grab')
                workGrabJob=os.path.join(workGrab,self.JOB_NAME).replace('\\','/')
                if not os.path.exists(workGrabJob):
                    os.makedirs(workGrabJob)
                
                self.grabRun(self.NODE_NAME,workGrabJob)
                sourcePath=os.path.join(workGrab,'*.*').replace('/','\\')
                targetPath=self.GRAB_OUTPUT.replace('/','\\')
                self.moveToServer(sourcePath,targetPath)
                
                self.RENDER_LOG.info('[Thread].sleep...'+str(self.interval))
                time.sleep(self.interval)
            except Exception, e:
                print '[Thread.err]'
                print e
                self.RENDER_LOG.info(e)
    def stop(self):  
        self.thread_stop = True
        self.RENDER_LOG.info('[Thread].stop...')
        try:
            print 'end'
            #os.system('taskkill /F /IM '+self.grabImgName+' /T')
        except Exception, e:
            print '[Thread.err]'
            print e