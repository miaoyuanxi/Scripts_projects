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

class RenderBase():

    def __init__(self,**paramDict):
        print 'Base.init...-------------------'
        
        self.G_LOG_WORK='C:/log/render'
        self.G_RENDER_WORK='C:/work/render'
        self.G_CFG_PY_NAME='py.cfg'
        self.G_CONVERTVBS_NAME='convertNew.vbs'
        self.G_PRE_PYNAME='pre.py'
        self.G_POST_PYNAME='post.py'
        
        self.G_USERID=paramDict['G_USERID']
        self.G_USERID_PARENT=paramDict['G_USERID_PARENT']
        self.G_TASKID=paramDict['G_TASKID']
        self.G_POOL=paramDict['G_POOL']
        # ��ʼ֡ 
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
        
        #self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_render'))
        self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'))
        
        self.G_RENDER_WORK_TASK=os.path.join(self.G_RENDER_WORK,self.G_TASKID)
        self.G_RENDER_WORK_TASK_CFG=os.path.join(self.G_RENDER_WORK,self.G_TASKID,'CFG')
        self.G_CFG_PYNAME=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_CFG_PY_NAME)#c:/renderwork/12343/renderbus/render.txt
        
        self.G_PRE_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_PRE_PYNAME)
        self.G_PRE_PY=self.G_PRE_PY.replace('\\','/')
        self.G_POST_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_POST_PYNAME)
        self.G_POST_PY=self.G_POST_PY.replace('\\','/')
        #log
        self.G_PROCESS_LOG=logging.getLogger('processlog')
        self.G_RENDER_LOG=logging.getLogger('renderlog')
        self.G_FEE_LOG=logging.getLogger('feeLog')
        
        self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK_TASK,'output')
        self.G_RENDER_WORK_OUTPUTBAK = os.path.join(self.G_RENDER_WORK_TASK,'outputbak')
        '''
        try:
            os.system('xcopy /y /v /f  "\\\\10.50.1.3\\p\\script\\py\\cleanNode.py" "c:/script/py/"')
            os.system('c:/python27/python.exe c:/script/py/cleanNode.py')
        except:
            print 'cleanNode Error'        
        '''
    def RBBackupPy(self): #
        print '[BASE.RBBackupPy.start.....]'
        # runPyPath = C:\agent\tmp\,runPyName= script_2014060400007_4
        runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
        tempRunPy=os.path.join(runPyPath,runPyName)
        if not os.path.exists(self.G_RENDER_WORK_TASK_CFG):
            os.makedirs(self.G_RENDER_WORK_TASK_CFG)
        workTaskRunPy=os.path.join(self.G_RENDER_WORK_TASK_CFG,runPyName)
        if not os.path.exists(workTaskRunPy):
            shutil.copyfile(tempRunPy,workTaskRunPy)
        #copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_RENDER_WORK_TASK_CFG+'/" '
        
        print '-----------===-----------------'
        print self.G_SYS_ARGVS
        for arg in self.G_SYS_ARGVS:
            print '------'+arg
        runBatName=os.path.basename(runPyName)+'.bat'
        runBat=os.path.join(self.G_RENDER_WORK_TASK_CFG,runBatName)
        #if  os.path.exists(runBat):
        #    os.remove(runBat)
        fileHandle=open(runBat,'w')
        batCmd='c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5]+'"'
        fileHandle.write(batCmd)
        fileHandle.close()
        print '[BASE.RBBackupPy.end.....]'
    '''
        ���ļ�
    '''
    def readFile(self,path):
        if os.path.exists(path):
            fileObject=open(path)
            line=fileObject.readlines()
            for r in line:
                print r
            return line
        pass
    
    '''
        ����py.cfg�ļ�
    '''
    def readPyCfg(self):
        self.argsmap={}         
        line=self.readFile(self.G_CFG_PYNAME)
        for l in line:
            if "=" in l:
                params=l.split("=")
                self.argsmap[(params[0]).replace('\r','').replace('\n','')]=params[1].replace('\n','').replace('\r','')
        pass
    '''
        net windows path
    '''
    def netPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mountFrom=self.argsmap['mountFrom']
        inputDataPath=self.argsmap['inputDataPath']
        cleanMountFrom='net use * /del /y'
        self.G_RENDER_LOG.info(cleanMountFrom)
        self.RBcmd(cleanMountFrom)
        s=eval(mountFrom)
        for key in s.keys():
            cmd='net use '+s[key]+' '+inputDataPath.replace('/','\\')+self.G_USERID_PARENT+key.replace('/','\\')
            self.G_RENDER_LOG.info(cmd)
            self.RBcmd(cmd)
        pluginPath=self.argsmap['pluginPath']
        cmd='net use B: '+pluginPath.replace('/','\\')
        self.RBcmd(cmd)       
    '''
        mount·������
    '''
    def mountPath(self):
        mountIp='192.168.0.199:/mnt/'
        mountFrom='{"worker_hhf":"Z:","worker":"A:"}'
        s=json.loads(mountFrom)
        for key in s.keys():
            print key
            print s[key]
            cmd='mount '+mountIp+key+' '+s[key]+''
            self.runCmd(cmd)
            pass
        pass    
    '''
        ���ϵͳ�̷�
    '''
    def CheckDisk(self):
        lpBuffer = ctypes.create_string_buffer(78)
        ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
        vol = lpBuffer.raw.split('\x00')
        for i in vol:
            if i:                             
                self.G_PROCESS_LOG.info('check CheckDisk='+str(i))
    '''
        �����ӽ�������cmd����
    '''
    def runCmd(self,cmd):
        print 'cmd='+cmd
        cmdp=subprocess.Popen(cmd,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)        
        while True:
            buff = cmdp.stdout.readline()
            if buff == '' and cmdp.poll() != None:
                break       
            print buff
            # self.G_RENDERCMD_LOGGER.info(buff)
            # self.G_PROCESS_LOGGER.info(buff)          
        resultCode = cmdp.returncode
        print 'resultCode='+str(resultCode) 
    '''
        ��ʼ����־
    '''
    def RBinitLog(self):#2
        processLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
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
        
        
        renderLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
        if not os.path.exists(renderLogDir):
            os.makedirs(renderLogDir)
        renderLogPath=os.path.join(renderLogDir,(self.G_JOB_NAME+'_render.txt'))
        self.G_RENDER_LOG.setLevel(logging.DEBUG)
        renderLogHandler=logging.FileHandler(renderLogPath)
        renderLogHandler.setFormatter(fm)
        self.G_RENDER_LOG.addHandler(renderLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_RENDER_LOG.addHandler(console)
        
        
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        self.G_FEE_LOG.setLevel(logging.DEBUG)
        if not os.path.exists(self.G_RENDER_WORK_TASK):
            os.makedirs(self.G_RENDER_WORK_TASK)
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        feeLogHandler=logging.FileHandler(feeTxt)
        #feeLogHandler.setFormatter(fm)
        self.G_FEE_LOG.addHandler(feeLogHandler)        
    
    def RBprePy(self):#pre custom
        self.G_PROCESS_LOG.info('[BASE.RBprePy.start.....]')
        self.G_PROCESS_LOG.info(self.G_PRE_PY)
        if os.path.exists(self.G_PRE_PY):
            sys.argv=[self.G_USERID,self.G_TASKID]
            #execfile(self.G_PRE_PY)
            os.system('c:/python27/python.exe ' + self.G_PRE_PY)
        self.G_PROCESS_LOG.info('[BASE.RBprePy.end.....]')        
    '''
        ����Ŀ¼
    '''       
    def RBmakeDir(self):#1
        self.G_PROCESS_LOG.info('[BASE.RBmakeDir.start.....]')
        
        #renderwork
        if not os.path.exists(self.G_RENDER_WORK_TASK):
            os.makedirs(self.G_RENDER_WORK_TASK)
        
        #renderwork/output
        if not os.path.exists(self.G_RENDER_WORK_OUTPUT):
            os.makedirs(self.G_RENDER_WORK_OUTPUT)
            
        #renderwork/outputbak
        if not os.path.exists(self.G_RENDER_WORK_OUTPUTBAK):
            os.makedirs(self.G_RENDER_WORK_OUTPUTBAK)

        #RB_small
        rbSamll = os.path.join(self.G_RENDER_WORK,self.G_TASKID,'RB_small')
        if not os.path.exists(rbSamll):
            os.makedirs(rbSamll)
        self.G_PROCESS_LOG.info('[BASE.RBmakeDir.end.....]')
            
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_PROCESS_LOG.info('[BASE.RBhanFile.start.....]')
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        self.RBcmd(copyVBSCmd)
        #"c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start C:\enfwork\\212869\output\*.*  /to=C:\enfwork\\212869\outputbak"
        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBcmd(moveOutputCmd)
        self.G_PROCESS_LOG.info('[BASE.RBhanFile.end.....]')
    '''
        copy�ļ�
    '''
    def RBcopyTempFile(self):
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.start.....]')
        #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
        self.RBcmd(copyPoolCmd)
        echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
        self.RBcmd(echoCmd,False,True)
        self.G_PROCESS_LOG.info('[BASE.RBcopyTempFile.end.....]')
    '''
        ��render.cfg�ļ�
    '''        
    def RBreadCfg(self):#4
        self.G_PROCESS_LOG.info('[BASE.RBreadCfg.start.....]')
    
        renderTxt=self.G_CFG_PYNAME
        txtFile=open(renderTxt, 'r')
        allLines=txtFile.readlines()
        for eachLine in allLines:
            if eachLine.startswith('#') or eachLine=='\n':
                continue
            execStr='self.'+eachLine.strip()
            print execStr
            exec(execStr)
        self.G_PROCESS_LOG.info('[BASE.RBreadCfg.end.....]')            
            
    def RBrenderConfig(self):#5
        self.G_PROCESS_LOG.info('[BASE.RBrenderConfig.start.....]')
        self.G_PROCESS_LOG.info('[BASE.RBrenderConfig.end.....]')        
    '''
        д�۷��ı�
    '''    
    def RBwriteConsumeTxt(self):#6
        self.G_PROCESS_LOG.info('[BASE.RBwriteConsumeTxt.start.....]')
        self.G_FEE_LOG.info('zone='+self.G_ZONE)
        self.G_FEE_LOG.info('nodeName='+self.G_NODE_NAME)
        if hasattr(self,'G_FIRST_FRAME'):
            self.G_FEE_LOG.info('firstFrame='+self.G_FIRST_FRAME)
        self.G_FEE_LOG.info('frames='+self.G_CG_START_FRAME)
        self.G_PROCESS_LOG.info('[BASE.RBwriteConsumeTxt.end.....]')
        
        
    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[BASE.RBrender.start.....]')
        self.G_PROCESS_LOG.info('[BASE.RBrender.end.....]')
    
    def RBpostPy(self):#pre custom
        self.G_PROCESS_LOG.info('[BASE.RBpostPy.start.....]')
        if os.path.exists(self.G_POST_PY):
            sys.argv=[self.G_USERID,self.G_TASKID]
            #execfile(self.G_POST_PY)
            os.system('c:/python27/python.exe ' + self.G_POST_PY)
        self.G_PROCESS_LOG.info('[BASE.RBpostPy.end.....]')
    def RvMakeDirs(self,path):
        print 'create dirs :'+path
        self.G_PROCESS_LOG.info('create dirs:'+str(path))
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            return path
        except Exception, e:
            print 'create dirs :'+path+'  failed'
            self.G_PROCESS_LOG.info('create dirs:'+str(path)+' failed')
    '''
        ת������ͼ
    '''
    def RBconvertSmallPic(self):    
        self.G_PROCESS_LOG.info('[BASE.RBconvertSmallPic.start.....]')
        smallSize='200'
        if self.G_KG=='1':
            smallSize='40'
            
        workSmallPath=os.path.join(self.G_RENDER_WORK_TASK,'small')        
        if not os.path.exists(workSmallPath):
            os.makedirs(workSmallPath)
            
        list_dirs = os.walk(self.G_RENDER_WORK_OUTPUT) 
        for root, dirs, files in list_dirs: 
            
            for name in files:
                smallFileName=name[name.rfind('.')+1:]
                self.G_PROCESS_LOG.info('smallFileName='+smallFileName)
                if smallFileName in 'vrmap' or  smallFileName in 'vrlmap':
                    continue    
                workBigPic =os.path.join(root, name)
                smallName=workBigPic.replace(self.G_RENDER_WORK_OUTPUT+'\\','')
                smallName=self.G_JOB_NAME+"_"+smallName.replace('\\','[_]').replace('.','[-]')+'.jpg'
                workSmallPic=os.path.join(workSmallPath,smallName)
                convertCmd='c:/ImageMagick/nconvert.exe  -out jpeg -ratio -resize '+smallSize+' 0 -overwrite -o "'+workSmallPic +'" "'+workBigPic+'"'
                #print workBigPic
                self.RBcmd(convertCmd,True,False)
                self.G_FEE_LOG.info('smallPic='+smallName)
                
                
        moveCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +workSmallPath.replace('/','\\')+'\*.*" /to="'+self.G_PATH_SMALL.replace('/','\\')+'"'
        self.RBcmd(moveCmd,True,False)    
        #convertCmd='cscript /nologo c:\\script\\vbs\\' + self.G_CONVERTVBS_NAME + '  '+self.G_USERID+' '+self.G_TASKID + ' "'+ self.G_JOB_NAME  +'" "'+self.G_PATH_SMALL +'\" '
        self.G_PROCESS_LOG.info('[BASE.RBconvertSmallPic.end.....]')
    '''
        �ϴ���Ⱦ�������־
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
        
        self.RBcmd(cmd1)
        self.RBcmd(cmd2)
        self.RBcmd(cmd3)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
    '''
        �ϴ���Ⱦ�������־
    ''' 
    def RBhanResult(self):#8
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.start.....]')        
        if hasattr(self,'argsmap'):
            # ֻ��Ⱦ����
            
            if self.argsmap.has_key('onlyphoton'):
                if self.argsmap['onlyphoton'] in 'true' and self.argsmap['kg'] != '102':
                    self.RBresultAction()
                    pass
                else:
                    if self.argsmap.has_key('currentTask'):
                        if self.argsmap['currentTask'] in 'photon':
                            uploadPath='A:/'+self.G_TASKID+'/photon/'
                            uploadCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
                            self.RvMakeDirs(uploadPath)
                            feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
                            feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
                            feeLogCmd='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
                            self.RBcmd(uploadCmd)
                            self.RBcmd(feeLogCmd)
                            pass
                        else:
                            self.RBresultAction()
                            pass
                        pass
                    else:
                        self.RBresultAction()                   
                    
            else:
                self.RBresultAction()
                pass   
        else:
            self.RBresultAction()
        
        
        
             
        # if hasattr(self,'G_KG'):
        #     if self.G_KG=='2' or self.G_KG=='3':#inc or animation 
            
        #         workMap=os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
        #         renderTemp=os.path.join(self.G_POOL,'temp',(self.G_FATHERID+'_render'))
        #         copyCmdStr='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+workMap.replace('/','\\')+'" /to="'+renderTemp.replace('/','\\')+'\\"'
        #         self.RBcmd(copyCmdStr)
                
        #         self.RBresultAction()
        #     elif self.G_KG=='4':#fast photon
        #         print 'fast photon'
        #         workMap = os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
        #         mergePoolTemp=os.path.join(self.G_POOL,'temp',(self.G_MERGE_TASKID+'_mergephoton'),'temp')
        #         cmdStr='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +workMap.replace('/','\\') +'" /to="'+mergePoolTemp+'"'
        #         self.RBcmd(cmdStr)
        #         frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        #         cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ mergePoolTemp+'"'
        #         cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
                
        #         feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        #         feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        #         cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
                
        #         self.RBcmd(cmd2)
        #         self.RBcmd(cmd3)
        #         self.RBcmd(cmd4)
        #         self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
        #     else:
        #         self.RBresultAction()
        # else:
        #     self.RBresultAction()
        
        self.G_PROCESS_LOG.info('[BASE.RBhanResult.end.....]')
    '''
        �����ӽ�������cmd����
    '''    
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

    def RBgetPluginDict(self):
        self.G_PROCESS_LOG.info('[Max.RVgetPluginDict start]')
        self.G_RAYVISION_PLUGINSCFG=os.path.join(self.G_RENDER_WORK_TASK,'cfg','plugins.cfg')
        self.G_PROCESS_LOG.info(self.G_RAYVISION_PLUGINSCFG)
        print self.G_RAYVISION_PLUGINSCFG
        plginInfoDict=None
        if  os.path.exists(self.G_RAYVISION_PLUGINSCFG):
            fp = open(self.G_RAYVISION_PLUGINSCFG)

            if fp:
                self.G_PROCESS_LOG.info('plugins file is exists')
                listOfplgCfg = fp.readlines()
                removeNL = [(i.rstrip('\n')) for i in listOfplgCfg]
                combinedText = ''.join(removeNL)
                plginInfoDict = eval('dict(%s)' % combinedText)
                print plginInfoDict
                self.G_PROCESS_LOG.info(plginInfoDict)
                for i in plginInfoDict.keys():
                    print i
                    print plginInfoDict[i]
        self.G_PROCESS_LOG.info('[Max.RVgetPluginDict end]')
        return plginInfoDict
        
    '''
        ��Ⱦ���̿��ƺ�����������Ը��Ƿ���
    '''    
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
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_PROCESS_LOG.info('[BASE.RBexecute.end.....]')