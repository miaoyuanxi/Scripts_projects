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
        self.LOCAL_FOLDER=os.path.join('c:\work\helper',self.G_TASKID,'max')
        print self.LOCAL_FOLDER
        self.tempFileFolder=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'),'max')
        self.packFileName=os.path.join(self.LOCAL_FOLDER,'max.full');
        self.fileCount=0
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

    def GetFileList(self,fileList,propath):
        projectPath=(self.G_PATH_USER_INPUT+propath).replace('/','\\')
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.projectPath.....]'+projectPath)
        sample_list=[]
        for parent,dirnames,filenames in os.walk(projectPath):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:                        #输出文件信息
                sample_list.append(os.path.join(parent,filename))
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.sample_list.....]'+os.path.join(parent,filename)+"---"+filename)
        pretxt='c:\\work\\helper\\'+self.G_TASKID

        if os.path.exists(pretxt):
            pass
        else:
            os.makedirs(pretxt)
        fh = open(pretxt+"\\pretxt.txt", 'w')
        for files in fileList:
            file1=(files.split('>>')[1]).replace('/','\\')                
            filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
            isExists=0
            if os.path.exists(filePath):
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filePath)
                fh.write(filePath+"\r\n") 
                self.fileCount=self.fileCount+1
                isExists=1
            else:
                filename=filePath[filePath.rfind("\\")+1:len(filePath)]
                for profilepath in sample_list:
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.profilepath.....]'+profilepath)
                    profilename=profilepath[profilepath.rfind("\\")+1:len(profilepath)]
                    if profilename==filename:
                        fh.write(profilepath+"\r\n")
                        self.fileCount=self.fileCount+1
                        isExists=1
                        break 
            if isExists==0:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+filePath+'...not  exists')
                return "-1"
            else:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+filePath+'...exists')
        fh.close()
        return pretxt+"\\pretxt.txt"


    def CopyFile(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.start.....]')
        fileList=[]
        textureKeyList=self.RENDER_CFG_PARSER.options('texture')
        
        propath= self.G_USERID_PARENT+"\\"+self.G_USERID+"\\"+self.G_PROJECT_NAME+"\\max";
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.propath.....]'+propath)
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
            commonCfg=self.RENDER_CFG_PARSER.options('common')#skipUpload
            skipUpload="0"
            if self.RENDER_CFG_PARSER.has_option('common','skipUpload'):
                skipUpload=self.RENDER_CFG_PARSER.get('common','skipUpload')
            self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.skipUpload.....]'+skipUpload)
            if skipUpload=="1":
                preFileTxt=self.GetFileList(fileList,propath)
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.preFileTxt.....]'+preFileTxt)
                if preFileTxt=="-1":
                    return -1;
                else:
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.fileCount.....]'+str(self.fileCount))
                    cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start /srcfile="'+preFileTxt+'" /to="'+self.LOCAL_FOLDER.replace('/','\\')+'"'
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                    if isinstance(cmd,unicode):
                        cmd.encode('utf-8')
                    else:
                        cmd.decode('gbk').encode('utf-8')
                    self.RBcmd(cmd)
            else:
                for files in fileList:
                    file1=(files.split('>>')[1]).replace('/','\\')     
                    filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filePath)
                    filedir=file1[file1.find(propath)+len(propath):file1.rfind("\\")]
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filedir)
                    #print os.path.exists(filePath)
                    #filePath=self.GetFileList(propath,filePath)
                    if os.path.exists(filePath):
                        cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+self.LOCAL_FOLDER.replace('/','\\')+filedir+'"'
                        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                        if isinstance(cmd,unicode):
                            cmd.encode('utf-8')
                        else:
                            cmd.decode('gbk').encode('utf-8')
                        self.RBcmd(cmd)
                    else:
                        return -1
                    
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
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]'+self.G_HELPER_WORK_TASK_CFG)
        renderCfg=os.path.join(self.G_HELPER_WORK_TASK_CFG,'render.cfg').replace('/','\\')
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        self.RENDER_CFG_PARSER.read(renderCfg)
        
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.end.....]')

    '''
        copy文件
    '''
    def RBcopyTempFile(self):
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.start.....]')
        #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_HELPER_WORK_TASK.replace('/','\\')+'"'
        self.RBcmd(copyPoolCmd)
        echoCmd = 'echo ...>>'+os.path.join(self.G_HELPER_WORK_TASK,'zzz.txt').replace('\\','/')
        self.RBcmd(echoCmd,False,True)
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.end.....]')

    '''
        解析py.cfg文件
    '''
    def readPyCfg(self):
        self.argsmap={}         
        line=self.readFile(self.G_HELPER_CFG_PYNAME)
        for l in line:
            if "=" in l:
                params=l.split("=")
                self.argsmap[(params[0]).replace('\r','').replace('\n','')]=params[1].replace('\n','').replace('\r','')
        pass
    
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
