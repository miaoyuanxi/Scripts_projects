#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import logging
import time
import subprocess
import ConfigParser
import codecs
import sys
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
        self.G_PLUGINS_MAX_SCRIPT='B:/plugins/max/script'
        self.G_HELPER=r'c:\work\helper'
        self.G_HELPER_TASK=os.path.join(self.G_HELPER,self.G_TASKID)
        self.G_HELPER_TASK_MAX=os.path.join(self.G_HELPER_TASK,'max')
        self.G_HELPER_TASK_MAXBAK=os.path.join(self.G_HELPER_TASK,'maxbak')
        self.G_HELPER_TASK_CFG=os.path.join(self.G_HELPER_TASK,'cfg')
        print self.G_HELPER_TASK_MAX
        self.tempFileFolder=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'),'max')
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        #self.packFileName=os.path.join(self.G_HELPER_TASK_MAX,'max.full');
        self.fileCount=0
        pass
        

        
    def isScriptUpdateOk(self,flagUpdate):
        if self.RENDER_CFG_PARSER.has_option('common','update'):
            scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
            scriptupdate=int(scriptupdateStr)
            if scriptupdate>flagUpdate or scriptupdate==flagUpdate:
                return True
        return False
        

    '''
        预处理任务，根据配置文件的文件，添加预处理的压缩max文件
    '''
    def RBrender(self):
        self.G_FEE_LOG.info('startTime='+str(int(time.time())))
        self.G_FEE_LOG.info('endTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('startTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('endTime='+str(int(time.time())))
        self.readRenderCfg()
        
        #if  not self.RENDER_CFG_PARSER.get('common','projectSymbol').endswith('_rb_netRender'):
        netRenderTxt=os.path.join(self.G_PLUGINS_MAX_SCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        self.G_PROCESS_LOG.info('netRenderTxt-------'+netRenderTxt)
        if  os.path.exists(netRenderTxt):
            self.G_PROCESS_LOG.info('------Net render process--------')
            
        else:
            self.CopyFile()
            self.PackFile()


    def PackFile(self):
        self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.start.....]')
        
        if os.path.exists(self.G_HELPER_TASK_MAX):
            if self.RENDER_CFG_PARSER.has_section('max'):
                zipfileKeyList=self.RENDER_CFG_PARSER.options('max')
                for zipfileKey in zipfileKeyList:
                    cgFile=(self.RENDER_CFG_PARSER.get('max',zipfileKey))
                    cgFilePath,cgFileName=os.path.split(cgFile)
            
                    maxZip=os.path.join(self.G_HELPER_TASK_MAX,(cgFileName+'.7z'))
                    if os.path.exists(maxZip):
                        #cmd = "\"%s\" e \"%s\" -o\"%s\" -y" % (self.exe, zip_file, out)
                        #unPackMaxCmd=self.G_DRIVERC_7Z+' x "'+maxZip+'" -y -aos -o"'+self.G_HELPER_TASK_MAX+'"' 
                        unPackMaxCmd=self.G_DRIVERC_7Z+' e "'+maxZip+'" -o"'+self.G_HELPER_TASK_MAX+'" -y ' 
                        unPackMaxCmd=unPackMaxCmd.encode(sys.getfilesystemencoding())
                        self.RBcmd(unPackMaxCmd)
                        
                        moveToMaxBakCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "'+maxZip.replace('/','\\')+'" /to="'+self.G_HELPER_TASK_MAXBAK.replace('/','\\')+'"'
                        moveToMaxBakCmd=moveToMaxBakCmd.encode(sys.getfilesystemencoding())
                        self.RBcmd(moveToMaxBakCmd)
                    else:
                        break
                    
            #cmd='c:/exdupe.exe -t16f '+self.G_HELPER_TASK_MAX+' '+self.G_HELPER_TASK_MAX+'.full'
            cmd=r'"'+self.G_DRIVERC_7Z+'" a -t7z "'+self.G_HELPER_TASK_MAX+'.7z" "'+self.G_HELPER_TASK_MAX+'\*"  -mmt -r'
            self.G_PROCESS_LOG.info(cmd)
            #print cmd
            self.RBcmd(cmd)
        self.G_PROCESS_LOG.info('[PreprocessTasK.packFile.end....]')

    def GetFileList(self,fileList,propath):
        projectPath=(self.G_PATH_USER_INPUT+propath).replace('/','\\')
        self.G_PROCESS_LOG.info('[[--------project file list------]')
        self.G_PROCESS_LOG.info('[[PreprocessTasK.projectPath.....]'+projectPath)
        sample_list=[]
        for parent,dirnames,filenames in os.walk(projectPath):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:                        #输出文件信息
                ff=os.path.join(parent,filename).decode('gbk')
                sample_list.append(ff)
                self.G_PROCESS_LOG.info(ff)
                #self.G_PROCESS_LOG.info(type(ff))
                
        pretxt=self.G_HELPER+self.G_TASKID

        if os.path.exists(pretxt):
            pass
        else:
            os.makedirs(pretxt)
        fh = open(pretxt+"\\pretxt.txt", 'w')
        notExistFileList=[]
        for files in fileList:
            #self.G_PROCESS_LOG.info(type(files))
            file1=(files.split('>>')[1]).replace('/','\\')
            if file1=="":
                self.G_PROCESS_LOG.info('files----'+files+"---false")
                sys.exit(-1)                  
            filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
            isExists=0
            if os.path.exists(filePath):
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.renderFilePath.....]'+file1.encode('gbk'))
                fh.write(filePath+"\r\n") 
                self.fileCount=self.fileCount+1
                isExists=1
            else:
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.checkProFileName-----]'+file1.encode('gbk'))
                filename=filePath[filePath.rfind("\\")+1:len(filePath)]
                for profilepath in sample_list:
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.fileName.....]'+profilepath)
                    profilename=profilepath[profilepath.rfind("\\")+1:len(profilepath)]
                    if profilename.lower()==filename.lower():
                        fh.write(profilepath+"\r\n")
                        self.fileCount=self.fileCount+1
                        isExists=1
            if isExists==0:
                notExistFileList.append(file1.encode('gbk'))
                #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+filePath.encode('utf-8')+'...[not  exists]')
            else:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+file1.encode('gbk')+'...[exists]')
        if len(notExistFileList)>0:
            for f in notExistFileList:
                self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.file.....]'+f+'...[not  exists]')
            return '-1'

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
                    sys.exit(-1)
                else:
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.fileCount.....]'+str(self.fileCount))
                    cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start /srcfile="'+preFileTxt+'" /to="'+self.G_HELPER_TASK_MAX.replace('/','\\')+'"'
                    self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                    if isinstance(cmd,unicode):
                        cmd.encode('utf-8')
                    else:
                        cmd.decode('gbk').encode('utf-8')
                    self.RBcmd(cmd)
            else:
                for files in fileList:
                    file1=(files.split('>>')[1]).replace('/','\\') 
                    if file1=="":
                        self.G_PROCESS_LOG.info('files----'+files+"---false")
                        sys.exit(-1)   
                    filePath=(self.G_PATH_USER_INPUT+file1[1:len(file1)]).replace('/','\\')
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filePath)
                    filedir=file1[file1.find(propath)+len(propath):file1.rfind("\\")]
                    #self.G_PROCESS_LOG.info('[[PreprocessTasK.packFile.filePath.....]'+filedir)
                    #print os.path.exists(filePath)
                    #filePath=self.GetFileList(propath,filePath)
                    if os.path.exists(filePath):
                        if self.isScriptUpdateOk(20160301):
                            self.G_PROCESS_LOG.info('unicode')
                            cmd=u'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+self.G_HELPER_TASK_MAX.replace('/','\\')+filedir+'"'
                            self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd.encode(sys.getfilesystemencoding()))
                            self.RBcmd(cmd.encode(sys.getfilesystemencoding()))
                        else:
                            self.G_PROCESS_LOG.info('un unicode')
                            cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+filePath+'" /to="'+self.G_HELPER_TASK_MAX.replace('/','\\')+filedir+'"'
                            self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.cmd.....]'+cmd)
                            if isinstance(cmd,unicode):
                                cmd.encode('utf-8')
                            else:
                                cmd.decode('gbk').encode('utf-8')
                            self.RBcmd(cmd)
                        
                    else:
                        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.filePath.....]'+filePath.encode(sys.getfilesystemencoding())+"not exists")
                        sys.exit(-1)
                        #break
                
                    
        self.G_PROCESS_LOG.info('[PreprocessTasK.copyFile.end.....]')

    def RBrenderConfig(self):
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.start.....]')
        self.G_PATH_USER_INPUT=self.argsmap['inputDataPath']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_PROJECT_NAME=self.argsmap['projectSymbol']
        self.G_TEMP=self.argsmap['tempPath']
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.end.....]')
        pluginPath=self.argsmap['pluginPath']
        zip=os.path.join(pluginPath,'tools','7-Zip')
        copy7zCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+zip.replace('/','\\')+'" /to="c:\\"'
        self.RBcmd(copy7zCmd)
        self.G_PROCESS_LOG.info('[PreprocessTasK.RBrenderConfig.end.....]')
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        tempFolder=os.path.join(self.G_TEMP,self.G_TASKID).replace('/','\\')
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)
        #RB_small
        if not os.path.exists(self.tempFileFolder):
            os.makedirs(self.tempFileFolder)
        cmd='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_HELPER_TASK_MAX+'.7z" /to="'+os.path.join(self.G_TEMP,self.G_TASKID).replace('/','\\')+'"'
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
        
        netRenderTxt=os.path.join(self.G_PLUGINS_MAX_SCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        if not os.path.exists(netRenderTxt):
            self.RBcmd(cmd)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]'+self.G_HELPER_TASK_CFG)
        renderCfg=os.path.join(self.G_HELPER_TASK_CFG,'render.cfg').replace('/','\\')
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        
        try:
            self.G_PROCESS_LOG.info('read rendercfg by utf16')
            self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-16"))
            
        except Exception, e:
            self.G_PROCESS_LOG.info(e)
            try:
                self.G_PROCESS_LOG.info('read rendercfg by  utf8')
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-8"))
                
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r"))
                self.G_PROCESS_LOG.info('read rendercfg by default')
        #self.RENDER_CFG_PARSER.read(renderCfg)
        
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
        
        self.netPath()        
        self.CheckDisk()
        # self.RBreadCfg()
        #self.RBhanFile()
        self.RBrenderConfig()
        self.RBrender()
        # self.RBconvertSmallPic()
        self.RBresultAction()
        self.RBpostPy()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')
