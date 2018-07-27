#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import logging
import time
import subprocess
import ConfigParser
from RenderBase import RenderBase
#update20151013\\10.50.8.15\p5\script\py\newpy\962712
class Preprocess(RenderBase):

    '''
        初始化构造函数
    '''
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        self.tempMark=0
        print 'PreprocessTasK init'
        self.LOCAL_FOLDER=os.path.join('c:\work\pre',self.G_TASKID,'max')
        print self.LOCAL_FOLDER
        self.tempFileFolder=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'),'max')
        self.packFileName=os.path.join(self.LOCAL_FOLDER,'max.full');
        
        pass
    '''
        预处理任务，根据配置文件的文件，添加预处理的压缩max文件
    '''
    def RBrender(self):
        self.G_FEE_LOG.info('startTime='+str(int(time.time())))
        self.G_FEE_LOG.info('endTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('startTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('endTime='+str(int(time.time())))
        self.readRenderCfg()
        self.CopyFile()
        self.PackFile()


    def PackFile(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.start.....]')
        if os.path.exists(self.LOCAL_FOLDER):
            cmd='c:/exdupe.exe -t16f '+self.LOCAL_FOLDER+' '+self.LOCAL_FOLDER+'.full'
            #print cmd
            self.RBcmd(cmd)
        self.G_PROCESS_LOG.info('[PreprocessTasK.packFile.end....]')

    def CopyFile(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.start.....]')
        fileList=[]
        textureKeyList=self.RENDER_CFG_PARSER.options('texture')
        
        #self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.textureKeyList]')
        if self.RENDER_CFG_PARSER.has_section('texture'):
            for textureKey in textureKeyList:
                fileList.append(self.RENDER_CFG_PARSER.get('texture',textureKey))
        if self.RENDER_CFG_PARSER.has_section('customfile'):
            customfileList=self.RENDER_CFG_PARSER.options('customfile')
            for customfileKey in customfileList:
                fileList.append(self.RENDER_CFG_PARSER.get('customfile',customfileKey))
        #self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.start.fileList.....]'+self.G_PATH_USER_INPUT)
        if fileList:
            for files in fileList:
                file1=(files.split('>>')[1]).replace('/','\\')
                         
                filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filePath)
                filedir=file1[file1.rfind(self.G_PROJECT_NAME)+len(self.G_PROJECT_NAME)+4:file1.rfind("\\")] 
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filedir)
                print os.path.exists(filePath)
                if os.path.exists(filePath):
                    cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+self.LOCAL_FOLDER.replace('/','\\')+filedir+'"'
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                    if isinstance(cmd,unicode):
                        cmd.encode('utf-8')
                    else:
                        cmd.decode('gbk').encode('utf-8')
                    self.RBcmd(cmd)
                    pass
            pass
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.end.....]')

    def RBrenderConfig(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.start.....]')
        self.G_PATH_USER_INPUT=self.argsmap['inputDataPath']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_PROJECT_NAME=self.argsmap['projectSymbol']
        self.G_TEMP=self.argsmap['tempPath']
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.end.....]')
   
        
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.tempFileFolder):
            os.makedirs(self.tempFileFolder)
        cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+self.LOCAL_FOLDER+'.full" /to="'+os.path.join(self.G_TEMP,self.G_TASKID).replace('/','\\')+'"'
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
        self.RBcmd(cmd)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]'+self.G_RENDER_WORK_TASK_CFG)
        renderCfg=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.cfg').replace('/','\\')
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        self.RENDER_CFG_PARSER.read(renderCfg)
        
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.end.....]')

    def RBexecute(self):#total    
        self.RBBackupPy()
        self.RBinitLog()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.start.....]')        
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.readPyCfg()       
        self.CheckDisk()
        # self.RBreadCfg()
        #self.RBhanFile()
        self.RBrenderConfig()
        self.RBrender()
        # self.RBconvertSmallPic()
        self.RBresultAction()
        self.RBpostPy()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')
