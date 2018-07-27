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
import codecs
import ConfigParser
import threading
import time
import json
import re
from socket import *

reload(sys)
sys.setdefaultencoding('utf-8')
from RenderBase import RenderBase
from NodeHelper import NodeHelper

from MaxDog import MonitorMaxThread
from MaxDog import MonitorMaxadapter
from MaxDog import MonitorLMU
from MaxDog import MonitorLog
from MaxDog import MaxLog
from MaxDog import DogUtil
from MaxPlugin import MaxPlugin                               

from CommonUtil import Common

pySitePackagesNode=r'c:\script\pySitePackages'
if os.path.exists(pySitePackagesNode):
    sys.path.append(pySitePackagesNode)
    from MaxThread import MaxThread
     
#---------------------calss maxclient--------------------
class MaxClient(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print 'Max.init...'
        self.G_MAXBAT_NAME='max.bat'
        self.G_RENDERBAT_NAME='crender.bat'        
        self.G_PLUGINBAT_NAME='plugin.bat'
        self.G_SCRIPT_NAME='crender.ms'
        self.G_RENDER_WORK_TASK_MAX=os.path.join(self.G_RENDER_WORK,self.G_TASKID,'max')
        self.G_CG_FILE=self.G_TASKID+'.max'
        self.G_DRIVERC_7Z='d:/7-Zip/7z.exe'
        #self.PLUGINS_MAX_SCRIPT='B:/plugins/max/script/user'
        
        if paramDict.has_key('G_JOB_ID'):
            self.G_JOB_NAME=paramDict['G_JOB_ID']
            
        if paramDict.has_key('G_SCHEDULER_CLUSTER_NODES'):
            self.G_SCHEDULER_CLUSTER_NODES = paramDict['G_SCHEDULER_CLUSTER_NODES']
            
        self.G_VRAY_LICNESE = '1'  # 1:old vray     2:copyrighted vray
        if paramDict.has_key('G_VRAY_LICNESE'):
            self.G_VRAY_LICNESE=paramDict['G_VRAY_LICNESE']
   
        self.G_MUNU_ID=self.G_SYS_ARGVS[1]
        self.G_JOB_ID=self.G_SYS_ARGVS[2]
        
        print '--------------jobid-------------'
        print type(self.G_JOB_NAME)
        self.G_JOB_NAME_STR=self.G_JOB_NAME
        self.G_JOB_NAME=self.G_JOB_NAME.encode(sys.getfilesystemencoding())
        print type(self.G_JOB_NAME)
        
        
        self.HOST='127.0.0.1'#'192.168.0.49'
        self.PORT=10100 
        self.BUFSIZ=1024
        self.ADDR=(self.HOST, self.PORT)
        
        
        #----------------------qsy20160712-----------------------
        self.G_MAX_B='B:/plugins/max'
        self.G_MAXSCRIPT=self.G_MAX_B+'/script'
        self.G_MAXSCRIPT_NAME='renderu.ms'#max2013,max204,max2015
        self.G_CUSTOM_BAT_NAME='custom.bat'
        self.G_USER_HOST_NAME='hosts.txt'
        self.G_PROGRAMFILES='C:/Program Files'

        #____________________custom________________________
        self.ASSET_WEB_COOLECT_BY_PATH=False
        self.MAX_CMD_RENDER=False
        self.MAX_VRAY_DISTRIBUTE=False
        self.RUN_RENDER_CMD_TIME = 1
        self.RENDER_MODE='location'
        #------------------------------------------------
        
        #sys.exit(-1)
        print '-----------tile....................'
        if self.G_CG_TILECOUNT==None or self.G_CG_TILECOUNT=='':
            self.G_CG_TILECOUNT='1'
        if self.G_CG_TILE==None or self.G_CG_TILE=='':
            self.G_CG_TILE='0'    
    def isScriptUpdateOk(self,flagUpdate):
        if self.RENDER_CFG_PARSER.has_option('common','update'):
            scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
            scriptupdate=int(scriptupdateStr)
            if scriptupdate>flagUpdate or scriptupdate==flagUpdate:
                return True
        return False
        
    def getPluginPath(self):
        pluginPathStr = self.argsmap['pluginPath'].replace('/','\\').replace("10.60.100.151","10.60.100.152")
        #pluginPathStr=r'\\10.60.96.110\td,\\10.60.100.152\td'
        pluginPathList = pluginPathStr.split(',')
        pluginPathListCount = len(pluginPathList)
        print 'getPluginPath----------------------------------'
        print str(pluginPathListCount)
        index = int(self.G_TASKID)%pluginPathListCount
        print str(index)
        pluginPath = pluginPathList[index]
        
        return pluginPath
        
        


    def RBhanFile(self):#3 copy script,copy max ,texture,cache,vrmap,#unpack
        self.RBlog('文件拷贝处理','start')
        self.G_PROCESS_LOG.info('[Max.RBhanFile.start.....]')
        
        
        # self.vrayDistributeNode()    
        
            
        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBlog(moveOutputCmd)
        self.RBcmd(moveOutputCmd,myLog=True)
        
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        self.RBlog(copyVBSCmd)
        self.RBcmd(copyVBSCmd,myLog=True)
        
        zip=os.path.join(self.PLUGIN_PATH,'tools','7-Zip')
        copy7zCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+zip.replace('/','\\')+'" /to="d:\\"'
        self.RBlog(copy7zCmd)
        self.RBcmd(copy7zCmd,myLog=True)
        
        #___________________grab__________________
        
        grabServer=r'C:/work/munu_client/grab_service/grab_service.exe'
        self.G_PROCESS_LOG.info(grabServer)
        
        if os.path.exists(grabServer) and DogUtil.checkProcess('grab_service'):
            self.G_PROCESS_LOG.info('start grab_service')
            os.system('start '+grabServer)
        '''
        try:
            os.system('taskkill /F /IM grab_service.exe /T')
        except Exception,e:
            pass
            
        
        grabServer=r'c:/grab/grab_service.exe'
        grab=os.path.join(self.PLUGIN_PATH,'tools','grab','*')
        copyGrabCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+grab.replace('/','\\')+'" /to="c:\\grab\\"'
        self.RBlog(copyGrabCmd)
        self.RBcmd(copyGrabCmd)
        
                                                    
        self.G_PROCESS_LOG.info(grabServer)
        if os.path.exists(grabServer):
            os.system('start '+grabServer)
        else:
            self.G_PROCESS_LOG.info('grab exe not exists')
            sys.exit(-1)
        '''
        
        #if  not self.RENDER_CFG_PARSER.get('common','projectSymbol').endswith('_rb_netRender'):
        
        #max.7z
        print 'tile------------------'
        print '..',self.G_CG_TILE,'--'
        print '..',self.G_CG_TILECOUNT,'--'
        
        tempPath=self.argsmap['tempPath']
        #tempPath=r'\\10.60.200.101\d\temp'
        if int(self.G_CG_TILECOUNT)>1 and self.G_CG_TILECOUNT==self.G_CG_TILE:#merge Pic
            self.G_RENDER_WORK_TASK_BLOCK=os.path.join(self.G_RENDER_WORK_TASK,'block').replace('/','\\')
        
            blockPath1=os.path.join(tempPath,self.G_TASKID,'block').replace('/','\\')
            self.RBlog(blockPath1)
            self.G_PROCESS_LOG.info(blockPath1)
            if os.path.exists(blockPath1):
                copyBlockCmd='c:\\fcopy\\FastCopy.exe   /speed=full /force_close  /no_confirm_stop /force_start "'+blockPath1+'\\*.*" /to="'+self.G_RENDER_WORK_TASK_BLOCK.replace('/','\\')+'"'
                copyBlockCmd=copyBlockCmd.encode(sys.getfilesystemencoding())
                self.RBlog(copyBlockCmd)
                self.RBcmd(copyBlockCmd,myLog=True)
            
        else:

            netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
            self.G_PROCESS_LOG.info(netRenderTxt)
            #if not os.path.exists(netRenderTxt):
            
            max7z=os.path.join(self.G_RENDER_WORK_TASK_MAX,'max.7z').replace('\\','/')
            max7z2=os.path.join(self.G_RENDER_WORK_TASK_MAX,'max.7z.001').replace('\\','/')
            self.RBlog('max7z------------'+max7z)
            self.RBlog('max7z2------------'+max7z2)
            #if os.path.exists(max7z):
            #    self.RBlog('del------------'+max7z)
            #    os.remove(max7z)
               
            temp_task= os.path.join(tempPath,self.G_TASKID)       
            tempFull2=os.path.join(temp_task,'max.7z')
            self.RBlog('temp_task------------'+temp_task) 
            self.RBlog('ZONE='+self.G_ZONE)
            if os.path.exists(temp_task):
                copyPoolCmd2='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull2.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK_MAX.replace('/','\\')+'"'
                #if self.G_ZONE=='1':
                copyPoolCmd2='xcopy  /e /y /q /v /f /d "' +temp_task.replace('/','\\') +'" "'+self.G_RENDER_WORK_TASK_MAX.replace('\\','/')+'"'
                    #xcopy /e /y /q /v /f "\\10.60.100.102\d\temp\9555472" "C:/work/render/9555472/max"
                self.RBlog(tempFull2)
                self.RBlog(copyPoolCmd2)
                try:
                    self.RBTry3cmd(copyPoolCmd2)
                except Exception, e:
                    self.G_PROCESS_LOG.info(e)
                
                self.vrayDistributeNode()
                
                # zzzExdupe=os.path.join(self.G_RENDER_WORK_TASK_CFG,'zzz.exdupe')
                # if not os.path.exists(zzzExdupe):
                
                
                self.RBlog(max7z)
                if os.path.exists(max7z):
                    self.G_PROCESS_LOG.info('unpack 7z...')
                    unpackCmd=self.G_DRIVERC_7Z+' x "'+max7z+'" -y -aos -o"'+self.G_RENDER_WORK_TASK_MAX+'"' 
                    self.RBlog(unpackCmd)
                    self.RBcmd(unpackCmd,myLog=True)
                
                if os.path.exists(max7z2):
                    self.G_PROCESS_LOG.info('unpack 7z.001...')
                    unpackCmd=self.G_DRIVERC_7Z+' x "'+max7z2+'" -y -aos -o"'+self.G_RENDER_WORK_TASK_MAX+'"' 
                    self.RBlog(unpackCmd)
                    self.RBcmd(unpackCmd,myLog=True)
                    
                
            self.RBcopyPhoton()
        self.RBlog('done','end')
        
        

        
    def checkNode(self):
        NH=NodeHelper(self.G_PROCESS_LOG)
        NH.run()
        
    def RBcopyTempFile(self):#copy render.cfg,plugins.cfg,pre.cfg,py.cfg
        self.RBlog('拷贝cfg配置文件','start')
        self.RBlog('render.cfg,plugins.cfg,pre.cfg,py.cfg...')
        self.G_PROCESS_LOG.info('[Max.CFG.start.....]')
        
        self.checkNode()
        
        
        try:
            workAreaExe='b:/tools/workarea.exe'
            if os.path.exists(workAreaExe):
                self.RBcmd(workAreaExe,myLog=True)
        except Exception, e:
            self.G_PROCESS_LOG.info(e)
        
        #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
        self.RBlog(tempFull)
        self.RBcmd(copyPoolCmd,myLog=True)
        
        


        '''
        unpackCmd='c:\\exdupe.exe -Rf "'+ os.path.join(self.G_RENDER_WORK_TASK,'temp.full')+ '" "' + self.G_RENDER_WORK_TASK +'/" '
        self.RBcmd(unpackCmd,True)
        oldMax=os.path.join(self.G_RENDER_WORK_TASK,'submit.max')
        newMax=os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
        #if  os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        if  os.path.exists(oldMax) and not os.path.exists(newMax):
            oldMax = oldMax.replace('\\','/')
            newMax = newMax.replace('\\','/')
            print oldMax
            print newMax
            os.rename(oldMax,newMax)
            
        delPackCmd='del /q /f "'+os.path.join(self.G_RENDER_WORK_TASK,'temp.full').replace('\\','/')+'"'
        os.remove(os.path.join(self.G_RENDER_WORK_TASK,'temp.full'))
        echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
        self.RBcmd(echoCmd,False,True)
        '''
        self.G_PROCESS_LOG.info('[Max.CFG.end.....]')
        self.RBlog('done','end')
        
    def RBcopyPhoton(self):
        
        if  self.G_KG=='100' or self.G_KG=='101' or self.G_KG=='102':#inc
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask']=='picture':
                photonProjectPath1=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"+self.RENDER_CFG_PARSER.get('common','projectSymbol')+"/max/photon/"+self.G_TASKID
                photonWorkPath=self.G_RENDER_WORK_TASK_MAX+'/photon'
                photonProjectPath2=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/photon/"+self.G_TASKID
                self.RBlog(photonProjectPath1.replace('/','\\'))
                self.RBlog(photonProjectPath2.replace('/','\\'))
                if os.path.exists(photonProjectPath1.replace('/','\\')):
                    copyPhotonCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+photonProjectPath1.replace('/','\\')+'\\*.*" /to="'+photonWorkPath.replace('/','\\')+'"'
                    self.RBlog(copyPhotonCmd)
                    self.RBcmd(copyPhotonCmd,myLog=True)
                    
                if os.path.exists(photonProjectPath2.replace('/','\\')):
                    copyPhotonCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+photonProjectPath2.replace('/','\\')+'\\*.*" /to="'+photonWorkPath.replace('/','\\')+'"'
                    self.RBlog(copyPhotonCmd)
                    self.RBcmd(copyPhotonCmd,myLog=True)

    def readFileByCode(self,path,code):
        print 'line----'
        if os.path.exists(path):
            pycfgObject=codecs.open(path,encoding=code)
            line=pycfgObject.readlines()
            pycfgObject.close()
            print line
            return line
        pass
        
    def readPyCfg(self):
        self.RBlog('读py.cfg配置文件','start')
        
        pypath=self.G_CFG_PYNAME
        print pypath
        if os.path.exists(self.G_CONFIG):
            pypath=self.G_CONFIG
        self.RBlog(pypath)
        self.argsmap={}
        try:
            line=self.readFileByCode(pypath,'UTF-8')
        except Exception, e:
            try:
                line=self.readFileByCode(pypath,'gbk')
            except Exception, e:
                line=self.readFileByCode(pypath,'UTF-16')
        
        print '\r\n\r\n+++++++++++++++++++++++++++++++'
        for l in line:
            if "=" in l:
                params=l.split("=")
                key=(params[0]).replace('\r','').replace('\n','')
                val=''
                for i in range(1,len(params)):
                    if i==1:
                        val=val+params[i]
                    else:
                        val=val+'='+params[i]
                    
                    
                
                val=val.replace('\n','').replace('\r','')
                self.argsmap[key]=val
                print key,val
                #self.argsmap[(params[0]).replace('\r','').replace('\n','')]=params[1].replace('\n','').replace('\r','')
        
        if not self.argsmap.has_key('onlyphoton'):
            self.argsmap['onlyphoton']='false'
        
        self.CURRENT_TASK='picture'
        
        self.G_PLATFORM=self.argsmap['platform']
        self.G_KG=self.argsmap['kg']
        self.G_PATH_SMALL=self.argsmap['smallPath']
        self.G_SINGLE_FRAME_CHECK=self.argsmap['singleFrameCheck']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_FIRST_FRAME=self.argsmap['firstFrame']

        self.G_ZONE=self.argsmap['zone']
        self.G_PATH_USER_OUTPUT=self.argsmap['output']
        
        #self.G_CG_RENDER_VERSION=self.argsmap['renderVersion']
        
        self.G_PATH_GRAB=self.argsmap['smallPath']
        
        self.PLUGIN_DICT=self.RBgetPluginDict()
        self.G_CG_VERSION=self.argsmap['cgv']
        self.G_CG_VERSION=self.PLUGIN_DICT['renderSoftware']+' '+self.PLUGIN_DICT['softwareVer']
        userInput=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"
        self.RBlog('user_input='+userInput.replace('/','\\'))
        self.RBlog('user_output='+self.G_PATH_USER_OUTPUT.replace('/','\\'))
        self.RBlog('user_small='+self.G_PATH_SMALL.replace('/','\\'))
        
        if self.argsmap.has_key('grabPath'):
            self.G_PATH_GRAB=self.argsmap['grabPath']
            self.RBlog('user_grab='+self.G_PATH_GRAB.replace('/','\\'))
        self.RBlog('done','end')
        
    def readRenderCfg(self):
        self.RBlog('读render.cfg配置文件','start')
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]')
        renderCfg=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.cfg')
        self.RBlog(renderCfg)
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        #self.RENDER_CFG_PARSER.read(renderCfg)
        
        codeList=['UTF-16','UTF-16-be','UTF-16-le','UTF-8','gbk','']
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        parseResult=False
        if os.path.exists(renderCfg):
            self.G_PROCESS_LOG.info('-----RENDER_CFG_PARSER-----')
            self.G_PROCESS_LOG.info(renderCfg)
            for code in codeList:
                try:
                    print code
                    self.G_PROCESS_LOG.info(code)
                    if code=='':
                        self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r"))
                        parseResult=True
                        break
                    else:
                        self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r",code))
                        parseResult=True
                        break
                except Exception, e:
                    print 'exception...',code
                    pass
        
        if self.RENDER_CFG_PARSER.has_option('vray','distribute') and self.RENDER_CFG_PARSER.get('vray','distribute')=='true':
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask']=='picture':
                self.MAX_VRAY_DISTRIBUTE=True
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.end.....]')
        self.RBlog('done','end')

    def InterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return False
            return True
        
    def parseInterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return ''
            
            return p[:index],p[index:]

    def getMaxFile(self,sourceMaxFile):
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            return self.getMaxFileWeb(sourceMaxFile)
        else:
            return self.getMaxFileClient(sourceMaxFile)
            
            
    def getMaxFileWeb(self,sourceMaxFile):
        self.G_PROCESS_LOG.info('\r\n\r\n\r\n-----------[-getMaxFileWeb-]--------------\r\n\r\n\r\n')
        if self.MAX_CMD_RENDER:
            self.RBlog('cmd render web')
            maxFilePathWeb=os.path.join(self.G_RENDER_WORK_TASK_MAX,(self.G_TASKID+r'.max')).replace('\\','/')
            self.RBlog(maxFilePathWeb)
            return maxFilePathWeb
        
        if self.ASSET_WEB_COOLECT_BY_PATH:
            resultMaxFile = sourceMaxFile
            userInput=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"
            userInput=userInput.replace('/','\\')
            sourceMaxFile=sourceMaxFile.replace('/','\\').replace(userInput,'')
            
            self.G_PROCESS_LOG.info(sourceMaxFile)
            if sourceMaxFile.startswith('__'):
                resultMaxFile = self.G_RENDER_WORK_TASK_MAX+'/'+sourceMaxFile
            elif sourceMaxFile.startswith('a') or sourceMaxFile.startswith('b') or sourceMaxFile.startswith('c') or sourceMaxFile.startswith('d'):
                resultMaxFile = self.G_RENDER_WORK_TASK_MAX+'/'+sourceMaxFile
            else:
                resultMaxFile=sourceMaxFile[0]+':'+sourceMaxFile[1:]
            
            resultMaxFile=resultMaxFile.replace('\\','/')
            self.G_PROCESS_LOG.info(resultMaxFile)
            return resultMaxFile
        else:
            resultMaxFile = self.G_RENDER_WORK_TASK_MAX+'/'+os.path.basename(sourceMaxFile)
            return resultMaxFile
        
    def getMaxFileClient(self,sourceMaxFile):
        self.RBlog('-----getMaxFileClient-----')
        self.RBlog(sourceMaxFile)
        netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        self.RBlog(netRenderTxt)
        if  self.MAX_CMD_RENDER:
            self.RBlog('cmd render')
            maxFilePath=os.path.join(self.G_RENDER_WORK_TASK_MAX,(self.G_TASKID+r'.max')).replace('\\','/')
            self.RBlog(maxFilePath)
            return maxFilePath
            
        if  os.path.exists(netRenderTxt):
            self.RBlog('net render')
            # cgFileName=os.path.basename(sourceMaxFile)
            cgFileName = sourceMaxFile.replace(':','')
            cgFile=os.path.join(self.G_RENDER_WORK_TASK_MAX,cgFileName).replace('\\','/')
            self.RBlog(cgFile)
            return cgFile
            
        absPath=[['a:/','/a/'],
            ['b:/','/b/'],
            ['c:/','/c/'],
            ['d:/','/d/']]
            
        resultMaxFile = sourceMaxFile
        src_max_lowercase = os.path.normpath(sourceMaxFile.lower()).replace('\\', '/')
        is_abcd_path = False;
        is_InterPath = False;
       
        for prefix in absPath:
            if src_max_lowercase.startswith(prefix[0]):
                is_abcd_path = True
                resultMaxFile = self.G_RENDER_WORK_TASK_MAX + src_max_lowercase.replace(prefix[0], prefix[1])
                break;
            
        if not is_abcd_path:
            if self.InterPath(src_max_lowercase):
                start,rest = self.parseInterPath(src_max_lowercase)
                resultMaxFile= self.G_RENDER_WORK_TASK_MAX + '/net' + start.replace('//', '/') + rest.replace('\\', '/') 
            else:
                resultMaxFile= sourceMaxFile.replace('\\', '/') 

        return os.path.normpath(resultMaxFile)

        
    '''
    def copyRenderFile(self):
        self.G_PROCESS_LOG.info('[Max.createFileList.start.....]')
        fileList=[]
        tempFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,'fileList.txt')
        tempFileObject=codecs.open(tempFile,'w')
        textureKeyList=self.RENDER_CFG_PARSER.options('texture')
        
        for textureKey in textureKeyList:
            fileList.append(self.RENDER_CFG_PARSER.get('texture',textureKey))
        if self.RENDER_CFG_PARSER.has_section('customfile'):
            customfileKeyList=self.RENDER_CFG_PARSER.options('customfile')
            for customfileKey in customfileKeyList:
                fileList.append(self.RENDER_CFG_PARSER.get('customfile',customfileKey))
        inputDataPath=self.argsmap['inputDataPath']
        print ('inputdatapath....'+inputDataPath)
        for file in fileList:
            subPath=file.split('>>')[1]
            file2=inputDataPath+subPath
            #print file2
            if isinstance(file2,unicode):
                file2=file2.encode('utf-8')
            else:
                file2=file2.decode('gbk').encode('utf-8')
            tempFileObject.write(file2.replace('/','\\'))
            tempFileObject.write('\r\n')
        tempFileObject.close()
        fcopyCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start /srcfile='+tempFile.replace('/','\\')+' /to='+self.G_RENDER_WORK_TASK.replace('/','\\')
        self.G_PROCESS_LOG.info('[Max.createFileList.]'+fcopyCmd)
        self.RBcmd(fcopyCmd) 
        self.G_PROCESS_LOG.info('[Max.createFileList.end.....]')
        return tempFile
    '''

    def substPath(self):
        
        self.G_PROCESS_LOG.info('[Max.substPath start]')
        batStr='net use * /del /y \r\n'
        batStr=batStr+'net use B: '+self.PLUGIN_PATH+' \r\n'
        substDriver='efghijklmnopqrstuvwxyz'
        for dd in substDriver:
            batStr=batStr+'subst '+dd+': /d\r\n'
        for fileName in os.listdir(self.G_RENDER_WORK_TASK_MAX):
            self.G_PROCESS_LOG.info(fileName)
            if os.path.isfile(os.path.join(self.G_RENDER_WORK_TASK_MAX,fileName)):
                continue
            dirName=fileName.lower()
            dirPath=os.path.join(self.G_RENDER_WORK_TASK_MAX,fileName).lower()
            print dirName        
            if dirName=='net':
                continue
            if dirName=='default':
                continue
            
            if self.isScriptUpdateOk(20160900):
                if dirName=='b' or dirName=='c' or dirName=='d':
                    continue
            else:
                if dirName=='a' or dirName=='b' or dirName=='c' or dirName=='d':
                    continue
            #e,f,g...
            if len(dirName)==1:
                # substCmd='subst '+dirName+': '+dirPath
                substCmd='subst '+dirName+': "'+dirPath+'"'
                self.RBlog(substCmd)
                self.G_PROCESS_LOG.info(substCmd)
                os.system(substCmd)
                batStr=batStr+substCmd+'\r\n'
        batFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('substDriver.bat')).replace('\\','/')
        self.writeBat(batFile,batStr)
        self.G_PROCESS_LOG.info('[Max.substPath end]')
        
    def netPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        self.RBlog('net映射','start')
        
        self.PLUGIN_PATH = self.getPluginPath()
        self.G_PROCESS_LOG.info('pluginPath='+self.PLUGIN_PATH)
        
        print '----------------net----------------'
        self.RBlog('[path config]') 
        inputDataPath=self.argsmap['inputDataPath']
        mountFrom=self.argsmap['mountFrom']
        
        cleanMountFrom='c:/try3.exe net use * /del /y'
        self.RBlog(cleanMountFrom)
        self.RBcmd(cleanMountFrom,myLog=True)
        
        self.delSubst()
        
                                             
        if not os.path.exists(r'B:\plugins'):
            cmd='c:/try3.exe net use B: '+self.PLUGIN_PATH
            self.RBlog(cmd)
            self.RBcmd(cmd,myLog=True)
        

        maxCmdTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'maxcmd.txt').replace('\\','/')
        if os.path.exists(maxCmdTxt):
            self.MAX_CMD_RENDER=True
        if self.RENDER_CFG_PARSER.has_option('common','rendertype') and self.RENDER_CFG_PARSER.get('common','rendertype')=='maxcmd':
            self.MAX_CMD_RENDER=True
        # print 'MAX_CMD_RENDER=' + str(self.MAX_CMD_RENDER)
        # pluginInfoDict = Common.GetPluginDict(self.G_RAYVISION_PLUGINSCFG)
        # with open(r'B:\plugins\max\ini\config\maxcmd_plugin.json','r') as pl:
            # pl_dict = json.load(pl)
            # print pl_dict
            # pl_list = pl_dict["maxcmd_plugin"]
            # print pl_list
            # if pluginInfoDict.has_key('plugins'):            
                # for pluginsKey in pluginInfoDict['plugins'].keys():
                    # pluginStr = pluginsKey + pluginInfoDict['plugins'][pluginsKey]
                    # if pluginStr in pl_list:
                        # self.MAX_CMD_RENDER=True
                        # break
        print 'MAX_CMD_RENDER=' + str(self.MAX_CMD_RENDER)
        
        if not self.isScriptUpdateOk(20160900):
        
            projectPath=os.path.join(inputDataPath,self.G_USERID_PARENT,self.G_USERID,self.RENDER_CFG_PARSER.get('common','projectSymbol'),'max')
            projectPath=projectPath.replace('/','\\')
            #self.RBlog(projectPath)
            self.G_PROCESS_LOG.info(projectPath)
            if not os.path.exists(projectPath):
                os.makedirs(projectPath)
            
            cmd='c:/try3.exe net use A: '+projectPath
            self.RBlog(cmd) 
            self.RBcmd(cmd,myLog=True)
        self.RBlog('done','end')
            
    def RBconfigHost(self,userHostFile):
        self.RBlog('用户自定制HOSTS操作：如果用户自定制的hosts文件存在，则会在渲染前把hosts配置文件的内容追加写到节点机hosts文件中')
        self.RBlog('用户自定制的hosts文件路径：')
        self.RBlog(userHostFile)
        self.G_PROCESS_LOG.info('[Max.RBconfigHost.start.....]')
        
        if os.path.exists(userHostFile):
            userHostObj=open(userHostFile)
            userHostList=userHostObj.readlines()
            userHostObj.close()
            
            winHostFile=r'C:\Windows\system32\drivers\etc\hosts'
            self.RBlog('节点机的hosts文件路径：')
            self.RBlog(winHostFile)
            winHostObj=open(winHostFile,'a+')
            winHostList=winHostObj.readlines()
            for lines in userHostList:
                if lines not in winHostList:
                    winHostObj.writelines('\n'+lines)
                    print 'Add mapPath Success!'

            winHostObj.close()
        self.G_PROCESS_LOG.info('[Max.RBconfigHost.end.....]')
        
    def checkConfigFile(self,configFileList):
        self.RBlog('相关配置文件')
        for configFile in configFileList:
            if os.path.exists(configFile):
                self.RBlog(configFile+'[exists]')
            else:
                self.RBlog(configFile+'[missing]')
    

    
                
    def RBrenderConfig(self):#5
        self.RBlog('渲染配置','start')
        
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.start.....]')
                     

        #kill 3dsmax.exe,3dsmaxcmd.exe,vrayspawner*.exe
        DogUtil.killMaxVray(self.G_SIMPLE_LOG)
        
        cgFile=self.RENDER_CFG_PARSER.get('max','max').replace('\\','/')
        self.MAX_FILE=self.getMaxFile(cgFile)
        self.RBlog('MAX_FILE='+self.MAX_FILE)
        
        
        
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            self.G_MAXSCRIPT_NAME='rendera1.3.ms'
        else:
            self.G_MAXSCRIPT_NAME='renderu1.3.ms'
            
        if self.G_PLATFORM=='2001':
            self.G_MAXSCRIPT_NAME=self.G_MAXSCRIPT_NAME.replace('.ms','.mse')
            
            
        self.G_PROCESS_LOG.info('maxscriptName------'+self.G_MAXSCRIPT_NAME)
        
        customerScriptPath=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID).replace('\\','/')
        customerMs=os.path.join(customerScriptPath,self.G_MAXSCRIPT_NAME).replace('\\','/')
        customBat=os.path.join(customerScriptPath,self.G_CUSTOM_BAT_NAME).replace('\\','/')
        maxIni=os.path.join(self.G_MAX_B,'ini/3dsmax',self.G_CG_VERSION,'3dsmax.ini').replace('\\','/')
        maxUserIni=os.path.join(self.G_MAX_B,'ini/3dsmax',self.G_USERID,self.G_CG_VERSION,'3dsmax.ini').replace('\\','/')
        userHostFile=os.path.join(customerScriptPath,self.G_USER_HOST_NAME).replace('\\','/')
        netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        
        configFileList=[customerScriptPath,customerMs,customBat,maxIni,maxUserIni,userHostFile,netRenderTxt]
        self.checkConfigFile(configFileList)
        
        #----------load max plugin----------
        self.RBlog('插件配置')
        #maxPlugin=MaxPlugin(self.G_PROCESS_LOG,self.G_MAX_B,self.G_CG_VERSION,self.PLUGIN_DICT,self.G_PROGRAMFILES,self.G_SIMPLE_LOG)
        #maxPlugin.config()
        pluginCfg=os.path.join(self.G_RENDER_WORK_TASK,'cfg','plugins.cfg')
        self.G_PROCESS_LOG.info('pluginCfg------'+pluginCfg)
        maxPlugin=MaxPlugin(pluginCfg,self.G_PROCESS_LOG,vray_license=self.G_VRAY_LICNESE)
        maxPlugin.config()
        #self.vrayDistribute()
        if int(self.G_CG_TILECOUNT)>1 and self.G_CG_TILECOUNT==self.G_CG_TILE:#merge Pic
            pass
        else:
            self.vrayDistributeRoot()
        
        if  os.path.exists(netRenderTxt):
            self.RENDER_MODE='net'
            
        if not os.path.exists(netRenderTxt):
            self.substPath()

        if self.argsmap.has_key('currentTask'):
            self.CURRENT_TASK=self.argsmap['currentTask']

        self.G_PROCESS_LOG.info('customBat------'+customBat)
        
        #-----------render.ms--------
        self.G_RAYVISION_MAXMS=os.path.join(self.G_MAXSCRIPT,self.G_MAXSCRIPT_NAME).replace('\\','/')
        if os.path.exists(customerMs):
            self.G_RAYVISION_MAXMS=customerMs
            
            

        #----------delete max log----------
        userprofile=os.environ["userprofile"]
        maxEnu=userprofile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu'
        maxlog=maxEnu+'\\Network\\Max.log'
        self.RBlog(maxlog)
        if os.path.exists(maxlog):
            try:
                os.remove(maxlog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
        
        #----------delete vary log----------
        userTempFile=os.environ["temp"]
        myTempVrayLog=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
        self.RBlog(myTempVrayLog)
        if os.path.exists(myTempVrayLog):
            try:
                os.remove(myTempVrayLog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
                
        #----------Customer 3dsmax.ini----------
        try:
            
            if os.path.exists(maxIni) and os.path.exists(maxEnu) :
                copyMaxiniCmd='xcopy /y /v /f "'+maxIni +'" "'+maxEnu.replace('\\','/')+'/"' 
                self.RBlog(copyMaxiniCmd)
                self.RBcmd(copyMaxiniCmd,myLog=True)
            
            if os.path.exists(maxUserIni) and os.path.exists(maxEnu) :
                copyMaxiniCmd='xcopy /y /v /f "'+maxUserIni +'" "'+maxEnu.replace('\\','/')+'/"' 
                self.RBlog(copyMaxiniCmd)
                self.RBcmd(copyMaxiniCmd,myLog=True)
        except Exception, e:
            self.G_PROCESS_LOG.info('[err].3dsmaxIni Exception')
            self.G_PROCESS_LOG.info(e)
            
        
        #------------CurrentDefaults.ini----------
        defaultMax=os.path.join(maxEnu,'en-US/defaults/MAX').replace('\\','/')+'/'
        if self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2012':
            defaultMax=os.path.join(maxEnu,'defaults/MAX').replace('\\','/')+'/'
        if self.RENDER_CFG_PARSER.has_option('renderSettings','gamma'):
            currentDefaultsIniGamma=os.path.join(self.G_MAX_B,'ini/3dsmaxDefault/gammaOn',self.G_CG_VERSION,'CurrentDefaults.ini').replace('\\','/')
            if self.RENDER_CFG_PARSER.get('renderSettings','gamma')=='off':
                currentDefaultsIniGamma=os.path.join(self.G_MAX_B,'ini/3dsmaxDefault/gammaOff',self.G_CG_VERSION,'CurrentDefaults.ini').replace('\\','/')
            
            self.G_PROCESS_LOG.info('---currentDefaultsIniGamma---')
            self.G_PROCESS_LOG.info(currentDefaultsIniGamma)
            if os.path.exists(currentDefaultsIniGamma):
                copyDefaultMaxiniCmd='xcopy /y /v /f "'+currentDefaultsIniGamma +'" "'+defaultMax+'"' 
                self.RBlog(copyDefaultMaxiniCmd)
                self.RBcmd(copyDefaultMaxiniCmd,myLog=True)

        #------------custom.bat----------
        if os.path.exists(customBat):
            customCmd=customBat+' "'+self.G_USERID+'" "'+self.G_TASKID+'" '
            self.RBlog('执行custom.bat定制脚本')
            self.RBcmd(customCmd,myLog=True)
            
        #------------host----------
        self.RBconfigHost(userHostFile)
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.end.....]')
        self.RBlog('done','end')
        
        #------------red shift license----------
        try:
            # self.RBlog('environ redshift_license 5053@10.50.10.231')
            # os.environ['redshift_license']='5053@10.50.10.231'
            self.RBlog('environ redshift_license')
            pluginInfoDict2 = Common.GetPluginDict(self.G_RAYVISION_PLUGINSCFG)
            with open(r'B:\plugins\max\ini\config\license_env.json','r') as pl:
                pl_dict = json.load(pl)
                print pl_dict
                if pluginInfoDict2.has_key('plugins'):
                    for pluginsKey in pluginInfoDict2['plugins'].keys():
                        pluginStr = pluginsKey + pluginInfoDict2['plugins'][pluginsKey]
                        if pl_dict.has_key(pluginStr):
                            if pl_dict[pluginStr].has_key('env_name'):
                                env_name = pl_dict[pluginStr]["env_name"]
                                env_value = pl_dict[pluginStr]["env_value"]
                                os.environ[env_name]=env_value
                            else:
                                for key,value in pl_dict[pluginStr].items():
                                    os.environ[key]=value
        except Exception, e:
            self.G_PROCESS_LOG.info('[err].red shift license env')
            self.G_PROCESS_LOG.info(e)

        
        self.G_PROCESS_LOG.info(os.environ)
        
        #------------Wait vrayspawner*.exe service to start ----------
        if int(self.G_CG_TILECOUNT)>1 and self.G_CG_TILECOUNT==self.G_CG_TILE:#merge Pic
            pass
        else:
            self.waitDistributeNode()
        
        
    def writeBat(self,batFile,cmdStr):
        #subst
        #batFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('render'+renderFrame+'_notrender.bat')).replace('\\','/')
        batFileObject=codecs.open(batFile,'w',"utf-8")
        batFileObject.write(cmdStr+'\r\n')
        batFileObject.close()
    
    def writeMsFile(self,sceneFile,renderOutput,renderFrame):
        msFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('render'+renderFrame+'.ms')).replace('\\','/')
        msFileNotRender=msFile.replace('.ms','_notrender.ms')
        self.RBlog(msFile)
        self.RBlog(msFileNotRender)
        
        self.writeMsFile2(msFile,sceneFile,renderOutput,renderFrame,'false')
        self.writeMsFile2(msFileNotRender,sceneFile,renderOutput,renderFrame,'true')#_notrender.ms
        return msFile
    def writeMsFile2(self,msFile,sceneFile,renderOutput,renderFrame,notRender):

        self.G_PROCESS_LOG.info('[Max.writeMsFile.start.....]')
        #C:\users\enfuzion\AppData\Roaming\RenderBus\Profiles\users\cust\enfuzion\maxscript
        
        # cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_RAYVISION_USER_ID+'\\" \\"'+self.G_RAYVISION_TASK_ID+'\\" \\"0\\" \\"'+framenum['startFrame']+'\\" \\"0\\" \\"'+self.G_RAYVISION_STARTFRAME+'\\" \\"'+sceneFile+'\\" \\"'+output+'\\" "'
        #sceneFile=sceneFile.decode('utf-8').encode('gbk')
        msFileObject=codecs.open(msFile,'w',"utf-8")
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            msFileObject=codecs.open(msFile,'w',"gbk")
        
        
        msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
        msFileObject.write('filein @"'+self.G_RAYVISION_MAXMS+'"\r\n')
        
        
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            myCamera= self.RENDER_CFG_PARSER.get('common','renderablecamera')
            myCamera=myCamera.strip('[,]')
            if '[,]' in myCamera:
                myCamera=self.G_CG_OPTION
            webArrayStr = '#("'+self.G_USERID+'","'+self.G_TASKID+'","'+notRender+'","'+renderFrame+'","'+self.G_CG_TILE+'","'+self.G_CG_TILECOUNT+'","'+self.G_KG+'","'
            webArrayStr=webArrayStr+self.G_JOB_NAME_STR+'","'+renderOutput+'/","'+self.G_PLATFORM+'","'+myCamera+'","'+self.CURRENT_TASK+'","web","'+sceneFile+'") \r\n'
            mystr='fastRender ' +webArrayStr #+self.G_USERID+'" "'+self.G_TASKID+'" "'+notRender+'" "'+renderFrame+'" "'+self.G_CG_TILE+'" "'+self.G_CG_TILECOUNT+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'"  "'+renderOutput+'/" '+arrayStr+' "'+self.CURRENT_TASK+'" "web" "'+sceneFile+'" \r\n'
        else:
            myCamera= self.RENDER_CFG_PARSER.get('renderSettings','renderablecamera')
            myCamera=myCamera.strip('[,]')
            if self.RENDER_CFG_PARSER.has_option('renderSettings','renderablecameras'):
                renderableCameraStr = self.RENDER_CFG_PARSER.get('renderSettings','renderablecameras')
                renderableCameraStr=renderableCameraStr.strip('[,]')
                if '[,]' in renderableCameraStr: 
                    myCamera=self.G_CG_OPTION
            if '[,]' in myCamera:
                myCamera=self.G_CG_OPTION
                
            clientArrayStr= '#("'+self.G_USERID+'","'+self.G_TASKID+'","'+notRender+'","'+renderFrame+'","'+self.G_CG_TILE+'","'+self.G_CG_TILECOUNT+'","'+self.G_KG+'","'
            clientArrayStr=clientArrayStr+self.G_JOB_NAME_STR+'","'+renderOutput+'/","'+self.G_PLATFORM+'","'+myCamera+'","'+self.CURRENT_TASK+'","client")\r\n'
            mystr='rvRender '+clientArrayStr#+self.G_USERID+'" "'+self.G_TASKID+'" "'+notRender+'" "'+renderFrame+'" "'+self.G_CG_TILE+'" "'+self.G_CG_TILECOUNT+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'"  "'+renderOutput+'/" '+arrayStr+' "'+self.CURRENT_TASK+'"\r\n'
            
        
        
        self.RBlog('--------ms-------')
        self.RBlog(mystr)
        
        
        
        if notRender=='true':
            msFileObject.write(mystr)
        else:
            msFileObject.write('fn renderRun = (\r\n')
            msFileObject.write(mystr)
            msFileObject.write(')\r\n')
        msFileObject.close()
        self.G_PROCESS_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
        
        
    def retrySocketSend(self,finalData):
        retry_times = 9
        while retry_times > 0:
            ret = self.socketSend(finalData)
            if ret:
                break
            else:
                retry_times -= 1
                time.sleep(10)
                self.G_PROCESS_LOG.info ('[retry]send grab socket')
            
        
    def socketSend(self,finalData):
        try:
            self.client=socket(AF_INET, SOCK_STREAM)
            self.client.connect(self.ADDR)
            self.client.send(finalData.encode('utf8'))
            recvData=self.client.recv(self.BUFSIZ)
            self.G_PROCESS_LOG.info('socket send result '+self.HOST+'_____'+recvData.decode('utf8'))
            if recvData!=None and recvData.endswith('success'):
                return True
            else:
                return False
        except Exception,e:
            self.G_PROCESS_LOG.info ('[err] connect socket exeception')
            self.G_PROCESS_LOG.info (e)
            return False
            
        
    def startGrab(self):
    
        self.G_PROCESS_LOG.info ('-------start grab------')
        
        grabRate='300'
        grabFolderLocal=os.path.join(self.G_RENDER_WORK_TASK,'grab').replace('\\','/')
        grabFolderServer=self.G_PATH_GRAB
        
        startSocket='rdf1grab|'+grabRate+'|'+grabFolderLocal+'|'+grabFolderServer+'|'+self.G_MUNU_ID+'_'+self.G_JOB_ID+'|'+self.G_NODE_NAME
        
        self.G_PROCESS_LOG.info ('SOCKET_DATA___'+startSocket)
        startSocketLen=len(startSocket)
        startSocketLenHex=hex(startSocketLen)
        print (str(startSocketLen)+'>>'+str(startSocketLenHex))
        startSocketLenHexStr=str(startSocketLenHex)[2:].zfill(8)
        finalData=startSocketLenHexStr+startSocket
        self.G_PROCESS_LOG.info('MSG______'+self.HOST+':'+str(self.PORT)+'____'+finalData)
        #self.socketSend(finalData.encode(sys.getfilesystemencoding()))
        self.retrySocketSend(finalData)
        
    def stopGrab(self):
        stopSocket='rdf1stop'
        stopSocketLen=len(stopSocket)
        stopSocketLenHex=hex(stopSocketLen)
        print (str(stopSocketLen)+'>>'+str(stopSocketLenHex))
        stopSocketLenHexStr=str(stopSocketLenHex)[2:].zfill(8)
        finalData=stopSocketLenHexStr+stopSocket
        self.G_PROCESS_LOG.info('MSG______'+self.HOST+':'+str(self.PORT)+'____'+finalData)
        self.retrySocketSend(finalData)
        
        #try:
            
        #    os.system('taskkill /F /IM grab_service.exe /T')
        #except Exception,e:
        #    pass
            
            
    
    def RBrenderCmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        #self.RBlog(cmdStr)
        self.RBlog("\n\n-------------------------------------------Start max program-------------------------------------\n\n")
        
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        #cmdp.stdin.write('3/n')
        #cmdp.stdin.write('4/n')
        while True:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine == '' and cmdp.poll()!=None:
                break
            resultLine1 = ''
            for word in resultLine:
                word_ord = ord(word)
                if word_ord != 0:
                    resultLine1+=word
            # self.RBlog(resultLine,'system')
            self.RBlog(resultLine1,'system')
            
            if '[End maxscript photon]' in resultLine1:
                try:
                    os.system('taskkill /F /IM 3dsmax.exe /T')
                except  Exception, e:
                    self.G_PROCESS_LOG.info('taskkill 3dsmax.exe exeception')  
                    self.G_PROCESS_LOG.info(e)  
                try:
                    os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
                except  Exception, e:
                    self.G_PROCESS_LOG.info('taskkill 3dsmaxcmd.exe exeception')  
                    self.G_PROCESS_LOG.info(e)                      
                #self.maxKill(cmdp.pid)
                self.RUN_RENDER_CMD_TIME += 1
                self.RBlog("\n\n-------------------------------------------End max photon-------------------------------------\n\n")
                
                
            # if '[End maxscript render]' in resultLine:
            if '[End maxscript render]' in resultLine1:
                try:
                    os.system('taskkill /F /IM 3dsmax.exe /T')
                except  Exception, e:
                    self.G_PROCESS_LOG.info('taskkill 3dsmax.exe exeception')  
                    self.G_PROCESS_LOG.info(e)  
                try:
                    os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
                except  Exception, e:
                    self.G_PROCESS_LOG.info('taskkill 3dsmaxcmd.exe exeception')  
                    self.G_PROCESS_LOG.info(e)                      
                #self.maxKill(cmdp.pid)
                self.RBlog("\n\n-------------------------------------------End max program-------------------------------------\n\n")
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.RBlog('resultStr...'+resultStr)
        self.RBlog('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr
    
    def maxKill(self,parentId):
        self.RBlog('maxKill...start...\n')
        cmdStr='wmic process where name="3dsmax.exe" get Caption,ParentProcessId,ProcessId'
        cmdp=subprocess.Popen(cmdStr,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while True:
            buff = cmdp.stdout.readline().strip()
            if buff == '' and cmdp.poll() != None:
                #print cmdp.poll()
                break
            #self.G_PROCESS_LOG.info(buff)
            if buff!=None and buff!='' :
                try:
                    self.G_PROCESS_LOG.info('max process info...')
                    self.G_PROCESS_LOG.info(buff)
                    buffArr=buff.split()
                    #print buff
                    if int(buffArr[1])==parentId:
                        #print 'kill...'+buff
                        os.system("taskkill /f /pid %s" % (buffArr[2]))
                except:
                    pass
        self.RBlog('maxKill...end...\n')
        

        
        
        
            
        
    def getLightcacheFrame(self):
        self.G_PROCESS_LOG.info('[Max.getLightcacheFrame.start....]')
        lightcacheFrame=None
        if self.RENDER_CFG_PARSER.has_option('vray','gi') and self.RENDER_CFG_PARSER.get('vray','gi')=='on':
            self.G_PROCESS_LOG.info('[Max.getLightcacheFrame.start1....]')
            if self.RENDER_CFG_PARSER.has_option('vray','lightcacheMode') and  self.RENDER_CFG_PARSER.get('vray','lightcacheMode')=='1':
                if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                    self.G_PROCESS_LOG.info('[Max.getLightcacheFrame.start2....]')
                    lightcacheFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
                else:
                    self.G_PROCESS_LOG.info('[Max.getLightcacheFrame.start3....]')
                    lightcacheFrame=self.RENDER_CFG_PARSER.get('common','frames')
        self.G_PROCESS_LOG.info('[Max.getLightcacheFrame.end....]')
        self.RBlog('lightcacheFrame:')
        self.RBlog(lightcacheFrame)
        return lightcacheFrame
    
    def getMaxVrayLog(self):
        if self.MAX_VRAY_DISTRIBUTE:
            userProFile=os.environ["userprofile"]
            userTempFile=os.environ["temp"]
            maxlog_dir = userProFile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu\\Network'
            maxlog_dir = maxlog_dir.replace('/','\\')
            maxlog_path = os.path.join(maxlog_dir,'Max.log').replace('/','\\')
            vraylog_dir = userTempFile.replace('/','\\')
            vraylog_path = os.path.join(vraylog_dir,'vraylog.txt').replace('/','\\')
            
            nodeIP_list = []
            for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
                nodeIP_list.append(node_ip)
            print nodeIP_list
            # nodeIP_num = len(nodeIP_list)  #numbers of node ip
            if nodeIP_list:
                for nodeIP in nodeIP_list:
                    maxlog_node_remote = '\\\\' + nodeIP + '\\' + maxlog_path.replace(':','$')
                    vraylog_node_remote = '\\\\' + nodeIP + '\\' + vraylog_path.replace(':','$')
                    maxlog_to_master = os.path.join(self.G_LOG_WORK,self.G_TASKID,nodeIP).replace('/','\\')
                    vraylog_to_master = os.path.join(self.G_LOG_WORK,self.G_TASKID,nodeIP).replace('/','\\')
                    maxlog_cmd=r'c:\fcopy\FastCopy.exe /cmd=force_copy /speed=full /force_close /no_confirm_stop /force_start "'+maxlog_node_remote+'" /to="'+maxlog_to_master+'"'
                    vraylog_cmd=r'c:\fcopy\FastCopy.exe /cmd=force_copy /speed=full /force_close /no_confirm_stop /force_start "'+vraylog_node_remote+'" /to="'+vraylog_to_master+'"'
                    self.RBlog(maxlog_cmd)
                    self.RBcmd(maxlog_cmd,True,myLog=True)
                    self.RBlog(vraylog_cmd)
                    self.RBcmd(vraylog_cmd,True,myLog=True)
        
    # Wait for the node computer's vrayspawner*.exe service to start
    def waitDistributeNode(self):
        if self.MAX_VRAY_DISTRIBUTE:
            self.G_PROCESS_LOG.info('[Max.waitDistributeNode.start....]')
            vrayspawner_node_ip_list = []    #list of node ip that started vrayspawner*.exe server
            
            def check_vrayspawner_cmd(thread_name,node_ip):
                self.G_PROCESS_LOG.info("%s begin: %s\n" % (thread_name,time.ctime(time.time())))
                check_cmd = 'tasklist /S %s /FI "IMAGENAME eq vrayspawner*"' % (node_ip)
                cmdp = subprocess.Popen(check_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                while cmdp.poll()==None:
                    result_str = cmdp.stdout.read().strip()
                    if result_str!='' and 'vrayspawner' in result_str:
                        self.G_PROCESS_LOG.info(result_str)
                        if node_ip not in vrayspawner_node_ip_list:
                            vrayspawner_node_ip_list.append(node_ip)
                    
                resultCode = cmdp.returncode        
                self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
                self.G_PROCESS_LOG.info("%s end: %s\n" % (thread_name,time.ctime(time.time())))
                
            node_ip_list = []
            wait_time = 8  #waiting time(min)
            for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
                node_ip_list.append(node_ip)
            self.G_PROCESS_LOG.info('node ip list:%s' % node_ip_list)
            node_ip_num = len(node_ip_list)  #numbers of node ip
            if node_ip_list:
                for i in range(wait_time):
                    thread_list = []  #thread list
                    for node_ip in node_ip_list:                
                        t = threading.Thread(target=check_vrayspawner_cmd,args=("Check vrayspawner-%s" % (node_ip),node_ip))
                        thread_list.append(t)
                    for t in thread_list:
                        t.start()
                    for t in thread_list:
                        t.join()
                        
                    while True:
                        active_thread_list = threading.enumerate()
                        self.G_PROCESS_LOG.info('active thread list:%s' % active_thread_list)
                        active_thread_num = threading.active_count()
                        if active_thread_num == 1:  #<_MainThread(MainThread, started 4092)>
                            break
                        time.sleep(5)
                    self.G_PROCESS_LOG.info('vrayspawner node ip list:%s' % vrayspawner_node_ip_list)
                    if len(vrayspawner_node_ip_list) == node_ip_num:
                        break
                    else:
                        if i == (wait_time - 1):
                            if len(vrayspawner_node_ip_list)/(node_ip_num*1.0) < 0.6:
                                self.G_PROCESS_LOG.info('[err]The percentage of render node machines is less than 60%')
                                sys.exit(-1)
                    time.sleep(60)
            else:
                self.G_PROCESS_LOG.info('nodeIP_list is empty\n')
            self.G_PROCESS_LOG.info('[Max.waitDistributeNode.end....]')
            
    # Kill the node computer's vrayspawner*.exe service
    def killDistributeNode(self):
        if self.MAX_VRAY_DISTRIBUTE:
            self.G_PROCESS_LOG.info('[Max.killDistributeNode.start....]')
            
            def kill_vrayspawner_cmd(thread_name,node_ip):
                self.G_PROCESS_LOG.info("%s begin: %s\n" % (thread_name,time.ctime(time.time())))
                check_cmd = 'taskkill /S %s /FI "IMAGENAME eq vrayspawner*"' % (node_ip)
                try:
                    os.system(check_cmd)
                except Exception as e:
                    self.G_PROCESS_LOG.info('[err]kill vrayspawner server failed!-%s' % node_ip)
                self.G_PROCESS_LOG.info("%s end: %s\n" % (thread_name,time.ctime(time.time())))
                
            node_ip_list = []
            for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
                node_ip_list.append(node_ip)
            self.G_PROCESS_LOG.info('node ip list:%s' % node_ip_list)
            node_ip_num = len(node_ip_list)  #numbers of node ip
            if node_ip_list:
                thread_list = []  #thread list
                for node_ip in node_ip_list:                
                    t = threading.Thread(target=kill_vrayspawner_cmd,args=("Kill vrayspawner-%s" % (node_ip),node_ip))
                    thread_list.append(t)
                for t in thread_list:
                    t.start()
                for t in thread_list:
                    t.join()
            else:
                self.G_PROCESS_LOG.info('nodeIP_list is empty\n')
            self.G_PROCESS_LOG.info('[Max.killDistributeNode.end....]')
            
            
    def RBrender(self):#7
        self.RBlog('渲染','start')
        
        self.G_PROCESS_LOG.info('[Max.RBrender.start....]')
        startTime = time.time()
        mySonid='0'
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        if self.MAX_VRAY_DISTRIBUTE:
            self.G_FEE_LOG.info('distribute=true')
            distributenode = self.RENDER_CFG_PARSER.get('vray','distributenode')
            self.G_FEE_LOG.info('distributenode=%s' % distributenode)  #numbers = host numbers + node numbers
        
        cgFile = self.argsmap['sceneFile'].replace('\\' , '/')
        print '----------type.......'
        print type(cgFile)
        '''
        if isinstance(cgFile,unicode):
            cgFile=cgFile.encode(sys.getfilesystemencoding())
        else:
            cgFile=cgFile.decode(sys.getfilesystemencoding()).encode('utf-8')
        '''
        cgFilePath,cgFileName = os.path.split(cgFile)
        cgFile=os.path.join(self.G_RENDER_WORK_TASK_MAX,cgFileName).replace('\\','/')
        #if  self.RENDER_CFG_PARSER.get('common','projectSymbol').endswith('_rb_netRender'):
        netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
        if  os.path.exists(netRenderTxt):#-----abort
            
            self.RBlog('-------Net Render-------')
            cgFile=os.path.join(r'A:/',cgFileName).replace('\\','/')
        '''
        if self.isScriptUpdateOk(20151125):
            cgFile=os.path.join(self.G_RENDER_WORK_TASK_MAX,cgFileName).replace('\\','/')
        '''
        
        '''
        if self.RENDER_CFG_PARSER.has_option('common','projectSymbol'):
            projectSymbol=self.RENDER_CFG_PARSER.get('common','projectSymbol')
            if projectSymbol.endswith('_renderlocal'):
                cgFilePath,cgFileName = os.path.split(cgFile)
                cgFile=os.path.join(self.G_RENDER_WORK_TASK,cgFileName).replace('\\','/')
        '''
        renderFrame=self.G_CG_START_FRAME
        if self.G_CG_START_FRAME==self.G_CG_END_FRAME:
            renderFrame=self.G_CG_START_FRAME
        else:
            renderFrame=self.G_CG_START_FRAME+'-'+self.G_CG_END_FRAME+'['+self.G_CG_BY_FRAME+']'
        if  self.G_KG=='100':#inc
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                    if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                        renderFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
                    else:
                        lightcacheFrame=self.RENDER_CFG_PARSER.get('common','frames')
        elif self.G_KG=='101':#animation
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                lighatcacheFrame=self.getLightcacheFrame()
                if lighatcacheFrame!=None:
                    renderFrame=lighatcacheFrame
        elif self.G_KG=='102':#fast inc
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                lighatcacheFrame=self.getLightcacheFrame()
                if lighatcacheFrame!=None:
                    renderFrame=lighatcacheFrame
        else:
            lighatcacheFrame=self.getLightcacheFrame()
            if lighatcacheFrame!=None:
                renderFrame=lighatcacheFrame
        '''
        if self.RENDER_CFG_PARSER.has_option('common','update'):
            scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
            scriptupdate=int(scriptupdateStr)
            if scriptupdate>20151000:
                if  self.G_KG=='100':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                            renderFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
                elif self.G_KG=='101':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        renderFrame=self.getLightcacheFrame()
                elif self.G_KG=='102':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        renderFrame=self.getLightcacheFrame()
                else:
                    renderFrame=self.getLightcacheFrame()
            else:
                if  self.G_KG=='100':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                            renderFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
        '''
        self.RBlog('renderframe='+renderFrame)
        
        renderOutput=self.G_RENDER_WORK_OUTPUT.replace('\\','/')
        myCamera=''
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            myCamera= self.RENDER_CFG_PARSER.get('common','renderablecamera')
        else:
            myCamera= self.RENDER_CFG_PARSER.get('renderSettings','renderablecamera')
        myCamera=myCamera.strip('[,]')
        if '[,]' in myCamera:
            renderOutput=renderOutput+'/'+self.G_CG_OPTION+'/'
        if int(self.G_CG_TILECOUNT)>1:
            if self.G_CG_TILECOUNT==self.G_CG_TILE:#merge
                if '[,]' in myCamera:
                    renderOutput=os.path.join(self.G_RENDER_WORK_OUTPUT,self.G_CG_OPTION).replace('\\','/')
                else:
                    renderOutput=self.G_RENDER_WORK_OUTPUT.replace('\\','/')
                
            else:#block render
                if '[,]' in myCamera:
                    renderOutput=os.path.join(self.G_RENDER_WORK_OUTPUT,('frame_'+renderFrame),self.G_CG_OPTION,('block_'+self.G_CG_TILE)).replace('\\','/')
                else:
                    renderOutput=os.path.join(self.G_RENDER_WORK_OUTPUT,('frame_'+renderFrame),('block_'+self.G_CG_TILE)).replace('\\','/')
                    
        if not os.path.exists(renderOutput):
            os.makedirs(renderOutput.decode('utf-8'))
        
        maxRenderExe='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmax.exe"'
        
        
        #self.RBlog('---maxscript---')
        #self.RBlog(debugCmdStr1)
        #self.RBlog(debugCmdStr2.encode(sys.getfilesystemencoding()))
        
    
        renderMsFile=self.writeMsFile(self.MAX_FILE.replace('\\','/'),renderOutput,renderFrame)
        #""C:/Program Files/Autodesk/3ds Max 2010/3dsmaxcmd.exe"  -start:3925 -end:3925   -o:"C:/enfwork/339844/output/ETCP__.tga" -camera:Cam00 -w:1920 -h:1080 -videoColorCheck:0 -atmospherics:1 -superBlack:0 -renderHidden:1 -force2Sided:0 -displacements:1 -renderFields:0  -effects:1 -RLA_ALPHA:1 -showRFW:true -continueOnError  -gammaCorrection:1  -gammaValueIn:2.2  -gammaValueOut:1.0  "339844.max""
        pluginDict=self.PLUGIN_DICT['plugins']
        standVrayList=[]
        standVrayList.append('3ds Max 2016_vray3.30.05')
        standVrayList.append('3ds Max 2015_vray3.30.05')
        standVrayList.append('3ds Max 2014_vray3.30.05')
        standVrayList.append('3ds Max 2016_vray3.40.01')
        standVrayList.append('3ds Max 2015_vray3.40.01')
        standVrayList.append('3ds Max 2014_vray3.40.01')
        standVrayList.append('3ds Max 2017_vray3.40.01')
        # standVrayList.append('3ds Max 2016_vray3.60.03')
        standVrayList.append('3ds Max 2014_vray0000')
        standVrayList.append('3ds Max 2015_vray0000')
        standVrayList.append('3ds Max 2017_vray0000')
        renderer=''
        if pluginDict.has_key('vray'):
            renderer='vray'+pluginDict['vray']
        standVrayStr=self.G_CG_VERSION+'_'+renderer
        
        self.G_PROCESS_LOG.info('\r\n\r\n==========================')
        self.G_PROCESS_LOG.info(standVrayStr)
        msFileNotRender=renderMsFile.replace('.ms','_notrender.ms')
        
        cmdStr = maxRenderExe+' -silent  -ma -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
        cmdStr2 = maxRenderExe+' -q -silent -ma -U MAXScript  "'+msFileNotRender+'"'
        if standVrayStr in standVrayList:
            cmdStr = maxRenderExe+'   -ma -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
            cmdStr2 = maxRenderExe+'   -ma -U MAXScript  "'+msFileNotRender+'"'
        
        substBat=os.path.join(self.G_RENDER_WORK_TASK_CFG,('substDriver.bat')).replace('\\','/')
        batFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('render'+renderFrame+'_notrender.bat')).replace('\\','/')
        cmdBat='call ' + substBat+'\r\n' +cmdStr2
        self.writeBat(batFile,cmdBat)
        #cmdFool='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -start:'+renderFrame+' -end:'+renderFrame+' -o:'+renderOutput+'/test.tga "'+cgFile+'"'
        #cmdStr=cmdFool
        
        if  self.MAX_CMD_RENDER==True:
            if self.argsmap.has_key('from') and self.argsmap['from']=='web':
                obase = self.RENDER_CFG_PARSER.get('common','rendoutputfilebasename')
                otype = self.RENDER_CFG_PARSER.get('common','rendoutputfiletype')
                cmdRenderOutput=obase+otype
                if self.RENDER_CFG_PARSER.has_option('common','renderablecamera'):
                    cmdRenderCam = self.RENDER_CFG_PARSER.get('common','renderableCamera')
                    cmdRenderCam = cmdRenderCam.strip('[,]')
                    if '[,]' in cmdRenderCam:
                        cmdRenderCam = self.G_CG_OPTION
                if self.RENDER_CFG_PARSER.has_option('common','width'):
                    cmdRenderwidth = self.RENDER_CFG_PARSER.get('common','width')
                if self.RENDER_CFG_PARSER.has_option('common','height'):
                    cmdRenderheight = self.RENDER_CFG_PARSER.get('common','height')
            else:
                if self.RENDER_CFG_PARSER.has_option('renderSettings','output'):
                    cmdRenderOutput = self.RENDER_CFG_PARSER.get('renderSettings','output')
                if self.RENDER_CFG_PARSER.has_option('renderSettings','renderableCamera'):
                    cmdRenderCam = self.RENDER_CFG_PARSER.get('renderSettings','renderableCamera')
                    cmdRenderCam = cmdRenderCam.strip('[,]')
                    if '[,]' in cmdRenderCam:
                        cmdRenderCam = self.G_CG_OPTION
                if self.RENDER_CFG_PARSER.has_option('renderSettings','width'):
                    cmdRenderwidth = self.RENDER_CFG_PARSER.get('renderSettings','width')
                if self.RENDER_CFG_PARSER.has_option('renderSettings','height'):
                    cmdRenderheight = self.RENDER_CFG_PARSER.get('renderSettings','height')
            
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                if self.RENDER_CFG_PARSER.has_option('vray','giwidth'):
                    cmdRenderwidth = self.RENDER_CFG_PARSER.get('vray','giwidth')
                if self.RENDER_CFG_PARSER.has_option('vray','giheight'):
                    cmdRenderheight = self.RENDER_CFG_PARSER.get('vray','giheight')
                
            #-----------------------------------------frames-----------------------------------------------
            frame_start = None
            frame_end = None
            frame_nth = None
            patt = '(-?\d+)(?:-?(-?\d+)(?:\[(-?\d+)\])?)?'
            m = re.match(patt,renderFrame)
            if m != None:
                frame_start = m.group(1)
                frame_end = m.group(2)
                frame_nth = m.group(3)
                if frame_end == None:
                    frame_end = frame_start
                if frame_nth == None:
                    frame_nth = '1'
                cmdStr='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -start:'+frame_start+' -end:'+frame_end+' -nthFrame:'+frame_nth+' -o:"'+renderOutput+'/'+cmdRenderOutput+'" -camera:"'+cmdRenderCam+'" -w:'+cmdRenderwidth+' -h:'+cmdRenderheight+' -continueOnError '
            else:
                print 'frames is not match'
                #cmdStr='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -start:'+renderFrame+' -end:'+renderFrame+' -o:"'+renderOutput+'/'+cmdRenderOutput+'" -camera:"'+cmdRenderCam+'" -w:'+cmdRenderwidth+' -h:'+cmdRenderheight+' -continueOnError '
                cmdStr='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -frames:'+renderFrame+' -o:"'+renderOutput+'/'+cmdRenderOutput+'" -camera:"'+cmdRenderCam+'" -w:'+cmdRenderwidth+' -h:'+cmdRenderheight+' -continueOnError '
            
            cmdStr += ' -showRFW:1 '  # show the Render Frame Window during render. 1:enable , 0:disable
            
            if self.G_USERID =='1840568':
                gammaStr=' -gammaCorrection:1 -gammaValueIn:2.2 -gammaValueOut:2.2 '
                cmdStr=cmdStr+gammaStr
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                maxfile_photon = self.MAX_FILE[:-4] + '_photon' + self.MAX_FILE[-4:]
                cmdStr=cmdStr+' "'+maxfile_photon.replace('\\','/')+'"'
            else:            
                cmdStr=cmdStr+' "'+self.MAX_FILE.replace('\\','/')+'"'
            #cmdStr=cmdFool
            
        self.RBlog(cmdStr)
        #if self.G_CG_VERSION=='3ds Max 2010':
            #renderMsFile=self.writeMsFile(cgFile,renderOutput,renderFrame,mySonid)
            #cmdStr = maxRenderExe+' -silent  -ma -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
        #else:
            #cmdStr = maxRenderExe+' -silent -ma -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_USERID+'\\" \\"'+self.G_TASKID+'\\" \\"'+mySonid+'\\" \\"'+renderFrame+'\\" \\"'+self.G_CG_TILE+'\\" \\"'+self.G_CG_TILECOUNT+'\\" \\"'+self.G_KG+'\\" \\"'+self.G_JOB_NAME+'\\" \\"'+cgFile+'\\" \\"'+renderOutput+'/\\" \\"'+self.G_PLATFORM+'\\" \\"'+self.CURRENT_TASK+'\\""'
        '''
        if isinstance(cmdStr,unicode):
            cmdStr=cmdStr.encode('utf-8')
        else:
            cmdStr.decode('gbk').encode('utf-8')
        '''
        #self.RBcmd('wmic path win32_desktopMonitor get screenHeight,screenWidth')
        
        ## -- Downline in 20180312 --
        # self.G_PROCESS_LOG.info('showdesktop.start')
        # try:
            # os.system('B:/tools/showDesktop.exe')
        # except Exception, e:
            # print 'exception in showDesktop'
            # print e
        # self.G_PROCESS_LOG.info('showdesktop.end')
        
        
        monitorLogList = []
        
        monLMU= MonitorLMU(180,self.G_TASKID,self.G_JOB_NAME,self.G_NODE_NAME,self.G_PROCESS_LOG,self.G_RENDER_WORK_TASK_CFG)
        monLMU.setDaemon(True)
        monLMU.start()
        monitorMaxT= MonitorMaxThread(180,self.G_TASKID,self.G_JOB_NAME,self.G_NODE_NAME,self.G_PROCESS_LOG,self.G_RENDER_WORK_TASK_CFG)
        monitorMaxT.setDaemon(True)
        monitorMaxT.start()
        monitorLogT= MonitorLog(180,self.G_TASKID,self.G_CG_VERSION,self.G_PROCESS_LOG,self.G_FEE_LOG,self.G_LOG_WORK,self.G_JOB_NAME,self.G_MUNU_ID,self.G_JOB_ID,monitorLogList,os.path.dirname(self.G_PATH_COST),max_vray_distribute=self.MAX_VRAY_DISTRIBUTE,render_work_task=self.G_RENDER_WORK_TASK)
        monitorLogT.setDaemon(True)
        monitorLogT.start()
        monMaxadapter= MonitorMaxadapter(180,self.G_TASKID,self.G_JOB_NAME,self.G_NODE_NAME,self.G_PROCESS_LOG,self.G_RENDER_WORK_TASK_CFG)
        monMaxadapter.setDaemon(True)
        monMaxadapter.start()
        
        
        self.startGrab()
        
        
#        sys.exit(-1)
        
        cmdStr=cmdStr.encode(sys.getfilesystemencoding())
        self.RBrenderCmd(cmdStr,True,True)
        #Distribute task and kg==0
        if self.G_KG == '0' and self.MAX_VRAY_DISTRIBUTE == True and self.RUN_RENDER_CMD_TIME > 1:
            # for i in range(self.RUN_RENDER_CMD_TIME-1):
            self.G_PROCESS_LOG.info('[Restart]Are you ready to restart 3dsmax? yes!!!')
            self.stopGrab()
            self.startGrab()
            self.RBrenderCmd(cmdStr,True,True)
            
        #rename photon file,add serial number
        if self.MAX_CMD_RENDER==True:
            if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                if self.G_KG=='102':  #fast inc
                    if os.path.exists(renderOutput):
                        renderOutput_list = os.listdir(renderOutput)
                        for file_basename in renderOutput_list:
                            if file_basename.endswith(r'irrmap.vrmap'):
                                # serial = self.G_JOB_NAME[6:]  #photon0000
                                length = len(self.G_CG_START_FRAME)
                                if length >= 4:
                                    serial = self.G_CG_START_FRAME
                                else:
                                    serial = '0'*(4-length) + self.G_CG_START_FRAME
                                file_newname = file_basename[:-6] + serial + file_basename[-6:]
                                try:
                                    os.rename(os.path.join(renderOutput,file_basename),os.path.join(renderOutput,file_newname))
                                except Exception as e:
                                    print 'rename failed'
                                    print e
        
        self.stopGrab()
        
        if monLMU!=None:
            monLMU.stop()
        if monitorMaxT!=None:
            monitorMaxT.stop()
        if monitorLogT!=None:
            monitorLogT.stop()
        if monMaxadapter!=None:
            monMaxadapter.stop()
            
        self.G_PROCESS_LOG.info('DEBUG_TASKKILL_3DSMAXCMD')            
        try:
            os.system('taskkill /F /IM 3dsmaxcmd.exe /T')
        except  Exception, e:
            self.G_PROCESS_LOG.info('2taskkill 3dsmaxcmd.exe exeception')  
            self.G_PROCESS_LOG.info(e) 
        
        
        self.G_PROCESS_LOG.info('DEBUG_TASKKILL_3DSMAX')
        try:
            os.system('taskkill /F /IM 3dsmax.exe /T')
        except  Exception, e:
            self.G_PROCESS_LOG.info('2taskkill 3dsmax.exe exeception')  
            self.G_PROCESS_LOG.info(e) 
            
        # time.sleep(3)
        # self.G_PROCESS_LOG.info('DEBUG_TASKKILL_MAXADAPTER')
        # try:
            # os.system('taskkill /F /IM maxadapter.adp.exe /T')
        # except  Exception, e:
            # self.G_PROCESS_LOG.info('2taskkill maxadapter.adp.exe exeception')  
            # self.G_PROCESS_LOG.info(e) 
        
        self.G_PROCESS_LOG.info('DEBUG_FEE__LOG') 
        
        
            
        print '\r\n\r\n------------------end render -----------\r\n\r\n\r\n'
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        
        self.delSubst()
        
        maxLog = MaxLog(self.G_TASKID,self.G_CG_VERSION,self.G_PROCESS_LOG,self.G_LOG_WORK,self.G_JOB_NAME)
        maxLog.do()
        
        self.getMaxVrayLog()
        
        # Kill the node computer's vrayspawner*.exe service
        self.killDistributeNode()
        
        if monitorLogList:
            # copy flag to storage server
            flag_file_src_dir = self.G_RENDER_WORK_TASK
            flag_file_dest_dir = os.path.join(os.path.dirname(self.G_PATH_COST),'distribute_problem')
            if not os.path.exists(flag_file_dest_dir):
                os.makedirs(flag_file_dest_dir)

            flag_start_string = '%s_%s_%s' % (self.G_TASKID, self.G_MUNU_ID, self.G_JOB_ID)
            for filename in os.listdir(flag_file_src_dir):
                if filename.startswith(flag_start_string) and filename.endswith('.log'):
                    move_flag_cmd= 'c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "%s" /to="%s"' % (os.path.join(flag_file_src_dir, filename).replace('/','\\'), flag_file_dest_dir.replace('/','\\'))
                    self.RBcmd(move_flag_cmd, myLog=True)
            
            self.G_PROCESS_LOG.info('[error]monitor log makes the task fail!!!')
            self.G_PROCESS_LOG.info(monitorLogList)
            
            sys.exit(-1)
        
        self.G_PROCESS_LOG.info('[Max.RBrender.end.....]')
        self.RBlog('done','end')
    
    def RBResultActionPhoton(self):
        self.G_PROCESS_LOG.info('[Max.RBResultActionPhoton.start.....]')  
        photonPath=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/"+self.argsmap['projectSymbol']+"/max/photon/"
        uploadPath=photonPath+self.G_TASKID+'/'
        if  self.isScriptUpdateOk(20160900):
            if self.argsmap['kg'] == '102':#fast inc map
                photonPath=os.path.join(self.argsmap['tempPath'],self.G_TASKID,'photon')
                uploadPath=photonPath.replace('\\','/')+'/'
            else:
                photonPath=self.argsmap['inputDataPath']+self.G_USERID_PARENT+"/"+self.G_USERID+"/photon/"
                uploadPath=photonPath+self.G_TASKID+'/'
        frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        self.RBlog('节点机输出路径:'+self.G_RENDER_WORK_OUTPUT.replace('\\','/'))
        self.RBlog('节点机输出备份路径:'+self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        self.RBlog('最终光子路径:'+uploadPath.replace('/','\\'))
        #uploadCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
        uploadCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+uploadPath.replace('/','\\')+'"'
        frameCheckcmd='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ uploadPath.rstrip()+'"'
        bakCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
        self.RvMakeDirs(uploadPath)
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME_STR+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        feeLogCmd='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'\\" '
        
        self.RBlog('uploadCmd='+uploadCmd)
        self.RBlog('frameCheckcmd='+frameCheckcmd)
        self.RBlog('bakCmd='+bakCmd)
        self.RBlog('feeLogCmd='+feeLogCmd)
        self.RBcmd(uploadCmd,myLog=True)
        self.RBcmd(frameCheckcmd,myLog=True)
        self.RBcmd(bakCmd,myLog=True)
        self.RBcmd(feeLogCmd.encode(sys.getfilesystemencoding()),myLog=True)
        self.G_PROCESS_LOG.info('[Max.RBResultActionPhoton.end.....]')  
        
    def RBhanResult(self):#8
        self.RBlog('结果处理','start')
        self.G_PROCESS_LOG.info('[Max.RBhanResult.start.....]')        
        if hasattr(self,'argsmap'):
            self.RBlog('kg='+self.argsmap['kg'] )
            self.RBlog('currentTask='+self.argsmap['currentTask'] )
            
            
            self.RBlog('onlyphoton='+self.argsmap['onlyphoton'] )
            
            if self.argsmap['kg'] == '100' or  self.argsmap['kg'] == '101':
                if self.argsmap['currentTask'] =='photon':
                    if self.argsmap['onlyphoton']=='true':
                        self.RBresultAction()
                    else:
                        self.RBResultActionPhoton()
                else:
                    self.RBresultAction()
            elif self.argsmap['kg'] == '102':
                if self.argsmap['currentTask'] =='photon':
                    self.RBResultActionPhoton()
                else:
                    self.RBresultAction()
            else:
                self.RBresultAction()
            
        else:
            self.RBresultAction()
        
        
        
        self.G_PROCESS_LOG.info('[Max.RBhanResult.end.....]')
        self.RBlog('done','end')
    '''
        upload result
    '''    
    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[Max.RBresultAction.start.....]')
        #RB_small
        #if not os.path.exists(self.G_PATH_SMALL):
            #os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        print 'type----------=========='
        print type(self.G_PATH_USER_OUTPUT)
        userOutput=self.G_PATH_USER_OUTPUT
        if int(self.G_CG_TILECOUNT)>1:
            if self.G_CG_TILECOUNT==self.G_CG_TILE:#merge
                pass
            else:#block render
                userOutput=os.path.join(self.argsmap['tempPath'],self.G_TASKID,'block')
        self.RBlog('节点机输出路径:'+self.G_RENDER_WORK_OUTPUT.replace('\\','/'))
        self.RBlog('节点机输出备份路径:'+self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        self.RBlog('最终输出路径:'+userOutput.replace('/','\\'))
        cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+userOutput.replace('/','\\')+'"'
        cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ userOutput.replace('/','\\')+'"'
        cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
        
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME_STR+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'\\" '
        
        print sys.getfilesystemencoding()
        #self.G_PROCESS_LOG.info(cmd1)
        cmd1=cmd1.encode(sys.getfilesystemencoding())
        self.G_PROCESS_LOG.info(cmd1)
        cmd2=cmd2.encode(sys.getfilesystemencoding())
        print 'cmd2-------=========',cmd2
        self.RBlog(cmd1.decode(sys.getfilesystemencoding()))
        self.RBTry3cmd(cmd1)
        
        try:
            self.checkResult()
        except Exception, e:
            print '[checkResult.err]'
            print e
        
        
        self.RBlog(cmd2.decode(sys.getfilesystemencoding()))
        self.RBcmd(cmd2,myLog=True)
        
        
        self.RBlog(cmd3.decode(sys.getfilesystemencoding()))
        self.RBTry3cmd(cmd3,continueOnErr=True)
        self.RBlog(cmd4)
        self.RBcmd(cmd4.encode(sys.getfilesystemencoding()),myLog=True)
        self.G_PROCESS_LOG.info('[Max.RBresultAction.end.....]')

            
    def vrayDistributeNode(self):
        def send_cmd(thread_name,localIP,nodeIP):
            self.G_PROCESS_LOG.info(u"%s begin: %s\n" % (thread_name,time.ctime(time.time())))
            from_addr = self.G_POOL+"\\script2\\Max\\MaxDistribute.py"
            from_addr_user = '%s\\script2\\User\\%s\\Max\\MaxDistribute.py' % (self.G_POOL,self.G_USERID)
            from_addr2 = self.G_POOL+"\\script2\\Max\\MaxPlugin.py"
            from_addr2_user = '%s\\script2\\User\\%s\\Max\\MaxPlugin.py' % (self.G_POOL,self.G_USERID)
            to_addr = r'\\' + nodeIP + r'\c$\script\py'
            copyNodeScriptPath='xcopy /Y /V /F "%s" "%s"' % (from_addr,to_addr)
            copyNodeScriptPath2='xcopy /Y /V /F "%s" "%s"' % (from_addr2,to_addr)
            if os.path.exists(from_addr_user):
                copyNodeScriptPath='xcopy /Y /V /F "%s" "%s"' % (from_addr_user,to_addr)
            if os.path.exists(from_addr2_user):
                copyNodeScriptPath2='xcopy /Y /V /F "%s" "%s"' % (from_addr2_user,to_addr)
            print copyNodeScriptPath,copyNodeScriptPath2
            if not os.path.exists(to_addr):
                os.makedirs(to_addr)
            self.RBcmd(copyNodeScriptPath,myLog=True)
            self.RBcmd(copyNodeScriptPath2,myLog=True)
            # else:
                # self.RBcmd(copyNodeScriptPath,myLog=True)
                # self.RBcmd(copyNodeScriptPath2,myLog=True)
            nodeScriptPath = os.path.join(r'c:\script\py','MaxDistribute.py')
            # print nodeScriptPath
            munu_port = '10001'
            if self.G_PLATFORM == '1016':
                munu_port = '10011'
            runPypath='B:/tools/munu_agent_controller.exe %s %s "C:\\Python27\\python.exe %s "%s" "%s" "%s" "c:\\log""' % (nodeIP,munu_port,nodeScriptPath,self.PLUGIN_PATH,self.G_TASKID,localIP)
            # self.G_PROCESS_LOG.info(runPypath)
            self.RBcmd(runPypath,myLog=True)
            self.G_PROCESS_LOG.info(u"%s over: %s\n" % (thread_name,time.ctime(time.time())))

        if self.MAX_VRAY_DISTRIBUTE:
            self.G_PROCESS_LOG.info('---------TODO Vray dist---------') 
            ##get IP
            #localIP = gethostbyname(gethostname())  #169.254.41.243
            ipList = gethostbyname_ex(gethostname())  #('GA010', [], ['10.60.1.10', '169.254.41.243'])
            localIP = ipList[2][0]  #get localhost IP：10.60.1.10
            self.G_PROCESS_LOG.info(u'local IP:%s' % localIP)
                
            ##get node ip list
            # with open(r"B:\plugins\max\ini\vrayDistribute\servers.json") as f1:  #B:   \\10.60.100.152\td
                # json_dict = json.load(f1)  #{u'10.60.1.5': [u'10.60.1.6', u'10.60.1.7'], u'10.60.1.10': [u'10.60.1.8', u'10.60.1.9']}
            # print json_dict
            # nodeIP_list = json_dict[localIP]  #[u'10.60.1.8', u'10.60.1.9']
            nodeIP_list = []
            for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
                nodeIP_list.append(node_ip)
            self.G_PROCESS_LOG.info(u'node ip list:%s' % nodeIP_list)
            thread_list = []  #thread list
            ##send command with multi thread
            if nodeIP_list:
                for nodeIP in nodeIP_list:
                    #thread.start_new_thread(send_cmd,("Thread-%s" % (nodeIP),localIP,nodeIP))
                    t = threading.Thread(target=send_cmd,args=("Thread-%s" % (nodeIP),localIP,nodeIP))
                    thread_list.append(t)
                for t in thread_list:
                    t.start()
                for t in thread_list:
                    t.join()
            else:
                self.G_PROCESS_LOG.info(u'node ip list is empty\n') 
            # time.sleep(120)
            
            
    def vrayDistributeRoot(self):
        if self.MAX_VRAY_DISTRIBUTE:
            self.G_PROCESS_LOG.info('---------TODO Vray dist---------')
            content = u""  
            nodeIP_list = []
            for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
                nodeIP_list.append(node_ip)
            self.G_PROCESS_LOG.info(u'node ip list:%s' % nodeIP_list)
            if nodeIP_list:
                for nodeIP in nodeIP_list:
                    content = content + nodeIP + u'\n'
                content = content.strip()
                self.G_PROCESS_LOG.info(u'content:\n%s' % content)
                configure_tmp_path = 'D:\\work\\render\\%s\\cfg\\vray_dr.cfg' % (self.G_TASKID)  #tmp path
                with open(configure_tmp_path, 'w') as f:
                    f.write(content)
                version_year = self.G_CG_VERSION[-4:]
                if int(version_year) < 2013:
                    configure_path = 'C:\\users\\enfuzion\\AppData\\Local\\Autodesk\\3dsmax\\%s - 64bit\\ENU\\plugcfg' % (version_year)
                else:
                    configure_path = 'C:\\Users\\enfuzion\\AppData\\Local\\Autodesk\\3dsMax\\%s - 64bit\\ENU\\en-US\\plugcfg' % (version_year)
                file_path = os.path.join(configure_path,"vray_dr.cfg")
                self.G_PROCESS_LOG.info(u'vray_dr.cfg path:%s' % file_path)
                if not os.path.exists(configure_path):
                    os.makedirs(configure_path)
                shutil.copy(configure_tmp_path,file_path)                    
                #os.system("copy %s %s" % (configure_tmp_path,file_path))
                #cmdcp=subprocess.Popen("copy %s %s" % (configure_tmp_path,configure_path),stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
                if os.path.isfile(file_path):
                    self.G_PROCESS_LOG.info(u'write vray_dr.cfg success\n')
            else:
                self.G_PROCESS_LOG.info(u'node ip list is empty\n')
            
            #------------------------------------subst Z:-------------------------------------
            subst_cmd = 'subst Z: "%s"' % (self.G_RENDER_WORK_TASK)
            if os.path.exists(self.G_RENDER_WORK_TASK):
                self.RBcmd(subst_cmd,myLog=True)
            
            time.sleep(120)
            
'''
import thread            
    def vrayDistribute(self):
    
        if self.MAX_VRAY_DISTRIBUTE:
            self.G_PROCESS_LOG.info('---------TODO Vray dist---------') 
            content = ""  
            content_top_list = []  
            content_top = ""  
            content_bottom = ""  

            def send_cmd(thread_name,localIP,nodeIP):
                print "%s begin: %s\n" % (thread_name,time.ctime(time.time()))
                from_addr = self.G_POOL+"\\script\\py\\py\\common\\MaxDistribute.py"
                from_addr2 = self.G_POOL+"\\script\\py\\py\\common\\MaxPlugin.py"
                to_addr = r'\\' + nodeIP + r'\c$\script\py'
                print to_addr
                copyNodeScriptPath='xcopy /Y /V /F "%s" "%s"' % (from_addr,to_addr)
                copyNodeScriptPath2='xcopy /Y /V /F "%s" "%s"' % (from_addr2,to_addr)
                print copyNodeScriptPath,copyNodeScriptPath2
                if not os.path.exists(to_addr):
                    os.makedirs(to_addr)
                    self.RBcmd(copyNodeScriptPath)
                    self.RBcmd(copyNodeScriptPath2)
                else:
                    self.RBcmd(copyNodeScriptPath)
                    self.RBcmd(copyNodeScriptPath2)
                nodeScriptPath = os.path.join(r'c:\script\py','MaxDistribute.py')
                print nodeScriptPath
                runPypath='B:/tools/munu_agent_controller.exe %s 10001 "C:\\Python27\\python.exe %s "%s" "%s" "%s" "c:\\log""' % (nodeIP,nodeScriptPath,self.PLUGIN_PATH,self.G_TASKID,localIP)
                print runPypath
                self.RBcmd(runPypath)
                print "%s over: %s\n" % (thread_name,time.ctime(time.time()))

            ##get IP
            #localIP = gethostbyname(gethostname())  #169.254.41.243
            ipList = gethostbyname_ex(gethostname())  #('GA010', [], ['10.60.1.10', '169.254.41.243'])
            localIP = ipList[2][0]  #get localhost IP：10.60.1.10
            print localIP
            
            ##analysis json
            with open(r"B:\plugins\max\ini\vrayDistribute\servers.json") as f1:  #B:   \\10.60.100.152\td
                json_dict = json.load(f1)  #{u'10.60.1.5': [u'10.60.1.6', u'10.60.1.7'], u'10.60.1.10': [u'10.60.1.8', u'10.60.1.9']}
            print json_dict
            nodeIP_list = json_dict[localIP]  #[u'10.60.1.8', u'10.60.1.9']
            print nodeIP_list
            nodeIP_num = len(nodeIP_list)  #numbers of node ip
            
            if nodeIP_list:
                for nodeIP in nodeIP_list:
                    try:
                        thread.start_new_thread(send_cmd,("Thread-%s" % (nodeIP),localIP,nodeIP))
                    except:
                        print "Error: unable to start thread\n"
                    if self.PLUGIN_DICT['plugins']['vray'].startswith('3'):
                        content_top_list.append('%s 1 20204\n' % (nodeIP))
                    else:
                        content_top_list.append('%s 1\n' % (nodeIP))
                    
                ####write cfg####
                for i in range(len(content_top_list)):
                    content_top = content_top + content_top_list[i]
                    
                if self.PLUGIN_DICT['plugins']['vray'].startswith('1'):
                    print 'vray1\n'
                    content_bottom = """restart_slaves 1
list_in_scene 1
"""
                elif self.PLUGIN_DICT['plugins']['vray'].startswith('2'):
                    print 'vray2\n'
                    content_bottom = """restart_slaves 1
list_in_scene 1
max_servers %s
""" % (nodeIP_num)
                elif self.PLUGIN_DICT['plugins']['vray'].startswith('3'):
                    print 'vray3\n'
                    content_bottom = """restart_slaves 1
list_in_scene 1
max_servers %s
use_local_machine 1
transfer_missing_assets 1
use_cached_assets 1
cache_limit_type 2
cache_limit 100.000000
""" % (nodeIP_num)
                else:
                    print 'vray version error\n'
                    sys.exit(-1)
                content = content_top.strip() + '\n' + content_bottom.strip()
                print content
                configure_tmp_path = 'D:\\work\\render\\%s\\cfg\\vray_dr.cfg' % (self.G_TASKID)  #tmp path
                with open(configure_tmp_path, 'w') as f:
                    f.write(content)
                version_year = self.G_CG_VERSION[-4:]
                if int(version_year) < 2013:
                    configure_path = 'C:\\users\\enfuzion\\AppData\\Local\\Autodesk\\3dsmax\\%s - 64bit\\ENU\\plugcfg' % (version_year)
                else:
                    configure_path = 'C:\\Users\\enfuzion\\AppData\\Local\\Autodesk\\3dsMax\\%s - 64bit\\ENU\\en-US\\plugcfg' % (version_year)
                print configure_path
                file_path = os.path.join(configure_path,"vray_dr.cfg")
                print file_path
                if not os.path.exists(configure_path):
                    os.makedirs(configure_path)
                shutil.copy(configure_tmp_path,file_path)                    
                #os.system("copy %s %s" % (configure_tmp_path,file_path))
                #cmdcp=subprocess.Popen("copy %s %s" % (configure_tmp_path,configure_path),stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
                if os.path.isfile(file_path):
                    print "Success\n"
            else:
                print 'nodeIP_list is empty\n'
            time.sleep(120)
'''