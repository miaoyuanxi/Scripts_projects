#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import ctypes
import json

class MunuBase():

    def __init__(self,**paramDict):
        print 'Base.init...-------------------'
        
        self.G_LOG_WORK='C:/log/render'
        self.G_RENDER_WORK='C:/work/render'
        self.G_CFG_PY_NAME='py.cfg'
        self.G_CONVERTVBS_NAME='convertNew.vbs'
        self.G_PRE_PYNAME='pre.py'
        self.G_POST_PYNAME='post.py'



        self.G_SCENE=paramDict['G_SCENE']
        self.G_SCENE_PROJECT=paramDict['G_SCENE_PROJECT']
        self.G_OUTPUT=paramDict['G_OUTPUT']
        
        self.G_CG_START_FRAME=paramDict['G_CG_START_FRAME']
        self.G_CG_END_FRAME=paramDict['G_CG_END_FRAME']
        self.G_CG_BY_FRAME=paramDict['G_CG_BY_FRAME']
        self.G_CG_LAYER_NAME=paramDict['G_CG_LAYER_NAME']
        self.G_CG_OPTION=paramDict['G_CG_OPTION']
        if 'G_CONFIG' in paramDict:
            self.G_CONFIG = paramDict['G_CONFIG']
        if 'G_PLUGINS' in paramDict:
            self.G_PLUGINS = paramDict['G_PLUGINS']

        self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
        self.G_JOB_NAME=self.G_SYS_ARGVS[3]
        self.G_NODE_NAME=self.G_SYS_ARGVS[5]
        
        #log
        self.G_PROCESS_LOG=logging.getLogger('processlog')

    
    def RBinitLog(self):#2
        processLogDir=os.path.join(self.G_LOG_WORK)
        if not os.path.exists(processLogDir):
            os.makedirs(processLogDir)
            
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        #feeFm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        processLogPath=os.path.join(processLogDir,(self.G_JOB_NAME+'_process.txt'))
        self.G_PROCESS_LOG.setLevel(logging.DEBUG)
        processLogHandler=logging.FileHandler(processLogPath)
        processLogHandler.setFormatter(fm)
        self.G_PROCESS_LOG.addHandler(processLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_PROCESS_LOG.addHandler(console)
        
        
            
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_PROCESS_LOG.info('[BASE.RBhanFile.start.....]')

        self.G_PROCESS_LOG.info('[BASE.RBhanFile.end.....]')
    
    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[BASE.RBrender.start.....]')
        
        self.G_PROCESS_LOG.info('[BASE.RBrender ]G_SCENE='+self.G_SCENE)
        self.G_PROCESS_LOG.info('[BASE.RBrender ]G_SCENE_PROJECT='+self.G_SCENE_PROJECT)
        self.G_PROCESS_LOG.info('[BASE.RBrender ]G_OUTPUT='+self.G_OUTPUT)
        renderCmd=''
        self.RBcmd(renderCmd)
        self.G_PROCESS_LOG.info('[BASE.RBrender.end.....]')
    
    def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_PROCESS_LOG.info('cmd...'+cmdStr)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                self.G_PROCESS_LOG.info(resultLine)
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.G_PROCESS_LOG.info('resultStr...'+resultStr)
        self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr

        
    def RBexecute(self):#total
    
        self.RBinitLog()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.start.....]')
        self.RBhanFile()
        self.RBrender()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')
        