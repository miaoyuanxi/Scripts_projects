#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import logging
import time
import subprocess
import sys
from RenderBase import RenderBase
#update20151013\\10.50.8.15\p5\script\py\newpy\962712
class Merge(RenderBase):

    '''
        初始化构造函数
    '''
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        self.tempMark=0
        print 'Merge init'
        pass
    '''
        合并光子入口
    '''
    def RBrender(self):
        self.G_RENDER_LOG.info('[Merge.RYrender start]')
        outputFiles=False
        if self.argsmap.has_key('onlyphoton'):
            if self.argsmap['onlyphoton'] in 'true':
                pass
                # self.G_OSS_OUTPUT_DIR=self.RvOssOutputRoot()+'d/output/'+self.RvUnionUserIdAndTaskId()
        self.G_FEE_LOG.info('startTime='+str(int(time.time())))
        self.G_FEE_LOG.info('endTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('startTime='+str(int(time.time())))
        self.G_RENDER_LOG.info('endTime='+str(int(time.time())))
        # 调用合并光子方法
        photonPath='A:/photon/'+self.G_TASKID+'/'
        self.G_RENDER_LOG.info('photonPath ='+str(photonPath))
        self.showPathFile(photonPath)
        self.mergePhoton(photonPath)
        # self.G_RENDER_LOG.info.info(framenum['status'])
        # outputFiles=self.getDirFileSize(self.G_RENDER_WORK_OUTPUT)
        # self.G_RENDER_LOG.info.info('outputFiles ='+str(outputFiles))
        # if outputFiles == True:
        # 	if framenum['status'] != '':
        # 		self.G_FEE_LOG.info('status='+framenum['status'])
        # 		self.G_RENDER_STATUS=False
        # 	else:
        # 		self.G_FEE_LOG.info('status=Success')
        # 		self.G_RENDER_STATUS=True
        # else:
        # 	self.G_RENDER_LOG.info.info('Render Failed ,Begin writeFee to mark Failed')
        # 	self.G_FEE_LOG.info('status=Failed')
        # 	self.G_RENDER_STATUS=False
        # self.G_RENDER_LOG.info.info('Merge.RYrender end')
        pass	
    def RBrenderConfig(self):
        self.G_PROCESS_LOG.info('[Merge.RBrenderConfig.start.....]')
        self.G_PLATFORM=self.argsmap['platform']
        self.G_KG=self.argsmap['kg']
        self.G_PATH_SMALL=self.argsmap['smallPath']
        self.G_SINGLE_FRAME_CHECK=self.argsmap['singleFrameCheck']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_FIRST_FRAME=self.argsmap['firstFrame']

        self.G_ZONE=self.argsmap['zone']
        self.G_PATH_USER_OUTPUT=self.argsmap['output']
        self.G_CG_VERSION=self.argsmap['cgv']
        self.G_CG_RENDER_VERSION=self.argsmap['renderVersion']
        self.G_PROCESS_LOG.info('[Merge.RBrenderConfig.end.....]')
    '''
        调用子进程合成光子
    '''
    def RVCmd(self,cmd):
        self.G_RENDER_LOG.info('cmd='+cmd)
        # self.G_RENDERCMD_LOGGER.info('cmd='+cmd)
        cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break
            # self.G_RENDERCMD_LOGGER.info(buff)
            # self.G_RENDER_LOG.info.info(buff)
        resultCode = cmdp.returncode
        self.G_RENDER_LOG.info('resultCode='+str(resultCode))
        
    '''	
        合成光子函数，参数说明：path光子所在路径
    '''
    def mergePhoton(self,path):
        self.tempMark=self.tempMark+1
        self.G_RENDER_LOG.info('photon path tempMark='+str(self.tempMark))
        self.temp=os.path.join(self.G_RENDER_WORK_TASK,'photon/temp/')
        self.G_RENDER_LOG.info('photon path temp='+self.temp)
        self.RvMakeDirs(self.temp)
        self.output=self.RvMakeDirs(self.temp+str(self.tempMark))
        self.RvMakeDirs(self.output)
        self.G_RENDER_LOG.info('photon output path='+self.output)
        self.renderOutPut=self.G_RENDER_WORK_OUTPUT
        self.RvMakeDirs(self.renderOutPut)
        self.G_RENDER_LOG.info('render outpath='+self.renderOutPut)
        oldRenderer=self.argsmap['render']
        self.G_RENDER_LOG.info('oldRenderer='+oldRenderer)
        standRender=oldRenderer.lower().replace("v-ray", "vray").replace("v_ray", "vray").replace("_adv__", "").replace("_adv_", "").replace("_",".").replace("demo ", "").replace(" ", "")
        self.G_RENDER_LOG.info('standRender='+standRender)
        vray='b:/plugins/max/imv/'+standRender+'/imapviewer.exe'
        self.G_RENDER_LOG.info('vray='+vray)
        fileArray=self.filterPhotonFile(path)
        fileArray.sort()
        print fileArray
        number=len(fileArray)
        print 'number='+str(number)
        if number<=10:
            cmd='"'+vray+'"'
            for p in fileArray:
                cmd=cmd+' -load '+path+'/'+p
                pass
            cmd=cmd+' -save '+self.renderOutPut+'/'+self.G_TASKID+'_irrmap.vrmap -nodisplay '
            self.RVCmd(cmd)	
            self.showPathFile(self.renderOutPut)
            pass
        elif number>10:
            j=0
            k=0
            while j<number:
                k=k+1
                i=0
                cmd='"'+vray+'"'
                while i<10:
                    
                    if j==number:
                        break
                    print 'fileArray['+str(j)+']='+fileArray[j]
                    cmd=cmd+' -load '+path+'/'+fileArray[j]
                    i=i+1
                    j=j+1
                    pass
                cmd=cmd+' -save '+self.output+'/'+str(k)+'.vrmap '+' -nodisplay'
                self.RVCmd(cmd)
            print 'j='+str(j)
            self.showPathFile(self.output)
            self.mergePhoton(self.output)
        pass
    '''
        过滤tga vrlmap扩展名的文件，这些文件不进行合并光子
    '''
    def filterPhotonFile(self,path):
        fileArray=os.listdir(path)
        tempArray=[]
        for nameStr in fileArray:
            
            if nameStr.endswith('.vrmap'):
                self.G_RENDER_LOG.info('nameStr='+nameStr)
                tempArray.append(nameStr)
        return tempArray
    def showPathFile(self,path):
        for p in os.listdir(path):
            self.G_RENDER_LOG.info('file='+path+'/'+p)
            # self.G_RENDERCMD_LOGGER.info('file='+path+'/'+p)
    '''
        上传渲染结果和日志
    '''
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.G_PATH_SMALL):
            os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+self.G_PATH_USER_OUTPUT+'"'
        cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ self.G_PATH_USER_OUTPUT+'"'
        cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'

        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
        cmd1=cmd1.encode(sys.getfilesystemencoding())
        cmd2=cmd2.encode(sys.getfilesystemencoding())
        self.RBcmd(cmd1)
        self.RBcmd(cmd2)
        self.RBcmd(cmd3)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
    '''
        上传渲染结果和日志
    ''' 
    def RBhanResult(self):#8
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.start.....]')
        # 只渲染光子
        if self.argsmap.has_key('onlyphoton'):
            if self.argsmap['onlyphoton'] in 'true':
                self.RBresultAction()
                pass
            else:
                if self.argsmap['currentTask'] in 'photon':
                    uploadPath='A:/photon/'+self.G_TASKID+'/'
                    uploadCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
                    feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
                    feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
                    cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
                    self.RvMakeDirs(uploadPath)
                    self.RBcmd(uploadCmd)
                    self.RBcmd(cmd4)
                    pass
                else:
                    self.RBresultAction()
                    pass
                pass
        else:
            self.RBresultAction()
            pass
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.end.....]')
    '''
        get dir size
    '''
    def getDirFileSize(self,path):
        list_dirs = os.walk(path)
        fileNum=len(os.listdir(path))
        fileSizeSum=0L
        fileSizeArray=[]
        flag=True
        for root, dirs, files in list_dirs:   
            for name in files:
                absolutePathFiles=os.path.join(root,name)
                size=os.path.getsize(absolutePathFiles)
                fileSizeSum=fileSizeSum+size
                fileSizeArray.append(size)
                self.G_PROCESS_LOG.info("filename="+absolutePathFiles)
                self.G_PROCESS_LOG.info("filesize="+str(size)) 
        self.G_PROCESS_LOG.info("fileNum="+str(fileNum))
        self.G_PROCESS_LOG.info("fileSizeSum="+str(fileSizeSum))
        if len(fileSizeArray)<=0:
            flag=False
        else:
            for f in fileSizeArray:
                if float(f) <=0:
                    flag=False
                    break
                pass
        self.G_PROCESS_LOG.info("flag="+str(flag))
        return flag
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
        self.RBwriteConsumeTxt()
        self.RBrender()
        # self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')