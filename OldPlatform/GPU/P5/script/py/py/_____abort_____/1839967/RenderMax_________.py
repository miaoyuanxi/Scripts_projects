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
import codecs
import ConfigParser
import threading
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from RenderBase import RenderBase
from NodeHelper import NodeHelper


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
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        #self.PLUGINS_MAX_SCRIPT='B:/plugins/max/script/user'
        
        #----------------------qsy20160712-----------------------
        self.G_MAX_B='B:/plugins/max'
        self.G_MAXSCRIPT=self.G_MAX_B+'/script'
        self.G_MAXSCRIPT_NAME='renderu.ms'#max2013,max204,max2015
        self.G_CUSTOM_BAT_NAME='custom.bat'
        self.G_USER_HOST_NAME='hosts.txt'
        self.G_PROGRAMFILES='C:/Program Files'

        self.ASSET_WEB_COOLECT_BY_PATH=False
        
        
        #------------------------------------------------
        
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

    def RBhanFile(self):#3 copy script,copy max ,texture,cache,vrmap,#unpack
        self.RBlog('文件拷贝处理','start')
        self.G_PROCESS_LOG.info('[Max.RBhanFile.start.....]')
        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBlog(moveOutputCmd)
        self.RBcmd(moveOutputCmd)
        
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        self.RBlog(copyVBSCmd)
        self.RBcmd(copyVBSCmd)
        
        pluginPath=self.argsmap['pluginPath']
        zip=os.path.join(pluginPath,'tools','7-Zip')
        copy7zCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+zip.replace('/','\\')+'" /to="c:\\"'
        self.RBlog(copy7zCmd)
        self.RBcmd(copy7zCmd)
        #if  not self.RENDER_CFG_PARSER.get('common','projectSymbol').endswith('_rb_netRender'):
        
        #max.7z
        print 'tile------------------'
        print '..',self.G_CG_TILE,'--'
        print '..',self.G_CG_TILECOUNT,'--'
        
        tempPath=self.argsmap['tempPath']
        if int(self.G_CG_TILECOUNT)>1 and self.G_CG_TILECOUNT==self.G_CG_TILE:#merge Pic
            self.G_RENDER_WORK_TASK_BLOCK=os.path.join(self.G_RENDER_WORK_TASK,'block').replace('/','\\')
        
            blockPath1=os.path.join(tempPath,self.G_TASKID,'block').replace('/','\\')
            self.RBlog(blockPath1)
            self.G_PROCESS_LOG.info(blockPath1)
            if os.path.exists(blockPath1):
                copyBlockCmd='c:\\fcopy\\FastCopy.exe   /speed=full /force_close  /no_confirm_stop /force_start "'+blockPath1+'\\*.*" /to="'+self.G_RENDER_WORK_TASK_BLOCK.replace('/','\\')+'"'
                copyBlockCmd=copyBlockCmd.encode(sys.getfilesystemencoding())
                self.RBlog(copyBlockCmd)
                self.RBcmd(copyBlockCmd)
            
        else:

            netRenderTxt=os.path.join(self.G_MAXSCRIPT,'user',self.G_USERID,'netrender.txt').replace('\\','/')
            self.G_PROCESS_LOG.info(netRenderTxt)
            

                
            if not os.path.exists(netRenderTxt):
            
                tempFull2=os.path.join(tempPath,self.G_TASKID,'max.7z')
                copyPoolCmd2='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull2.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK_MAX.replace('/','\\')+'"'
                self.RBlog(tempFull2)
                self.RBlog(copyPoolCmd2)
                try:
                    self.RBcmd(copyPoolCmd2)
                except Exception, e:
                    self.G_PROCESS_LOG.info(e)
                    
                zzzExdupe=os.path.join(self.G_RENDER_WORK_TASK_CFG,'zzz.exdupe')
                if not os.path.exists(zzzExdupe):
                    maxfull=os.path.join(self.G_RENDER_WORK_TASK_MAX,'max.full')
                    max7z=os.path.join(self.G_RENDER_WORK_TASK_MAX,'max.7z')
                    self.RBlog(maxfull)
                    self.RBlog(max7z)
                    if os.path.exists(max7z):
                        self.G_PROCESS_LOG.info('unpack 7z...')
                        unpackCmd=self.G_DRIVERC_7Z+' x "'+max7z+'" -y -aos -o"'+self.G_RENDER_WORK_TASK_MAX+'"' 
                        self.RBlog(unpackCmd)
                        self.RBcmd(unpackCmd)
                    elif os.path.exists(maxfull):
                        self.G_PROCESS_LOG.info('unpack exdupe...')
                        exdupeCmd='c:/exdupe.exe -Rf ' + maxfull +' '+self.G_RENDER_WORK_TASK_MAX
                        self.RBlog(exdupeCmd)
                        self.RBcmd(exdupeCmd)
                    os.system('echo finish>'+zzzExdupe)
                
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
                self.RBcmd(workAreaExe)
        except Exception, e:
            self.G_PROCESS_LOG.info(e)
        
        #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
        self.RBlog(tempFull)
        self.RBcmd(copyPoolCmd)
        
        


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
                    self.RBcmd(copyPhotonCmd)
                    
                if os.path.exists(photonProjectPath2.replace('/','\\')):
                    copyPhotonCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+photonProjectPath2.replace('/','\\')+'\\*.*" /to="'+photonWorkPath.replace('/','\\')+'"'
                    self.RBlog(copyPhotonCmd)
                    self.RBcmd(copyPhotonCmd)

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
        
                
        cgFile=self.RENDER_CFG_PARSER.get('max','max').replace('\\','/')
        self.MAX_FILE=self.getMaxFile(cgFile)
        self.RBlog('MAX_FILE='+self.MAX_FILE)
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
                substCmd='subst '+dirName+': '+dirPath
                self.RBlog(substCmd)
                self.G_PROCESS_LOG.info(substCmd)
                self.G_RENDER_LOG.info(substCmd)
                os.system(substCmd)
        self.G_PROCESS_LOG.info('[Max.substPath end]')
        
    def netPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        self.RBlog('net映射','start')
        print '----------------net----------------'
        self.G_RENDER_LOG.info('[path config]') 
        inputDataPath=self.argsmap['inputDataPath']
        mountFrom=self.argsmap['mountFrom']
        
        cleanMountFrom='try3 net use * /del /y'
        self.RBlog(cleanMountFrom)
        self.G_RENDER_LOG.info(cleanMountFrom)
        self.RBcmd(cleanMountFrom)
        
        self.delSubst()
        
        pluginPath=self.argsmap['pluginPath']
        if not os.path.exists(r'B:\plugins'):
            cmd='try3 net use B: '+pluginPath.replace('/','\\')
            self.RBlog(cmd) 
            self.G_RENDER_LOG.info(cmd)
            self.RBcmd(cmd)
        

            
        if not self.isScriptUpdateOk(20160900):
        
            projectPath=os.path.join(inputDataPath,self.G_USERID_PARENT,self.G_USERID,self.RENDER_CFG_PARSER.get('common','projectSymbol'),'max')
            projectPath=projectPath.replace('/','\\')
            #self.RBlog(projectPath)
            self.G_PROCESS_LOG.info(projectPath)
            if not os.path.exists(projectPath):
                os.makedirs(projectPath)
            
            cmd='try3 net use A: '+projectPath
            self.RBlog(cmd) 
            self.G_RENDER_LOG.info(cmd) 
            self.RBcmd(cmd)
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
              
        
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            self.G_MAXSCRIPT_NAME='rendera1.2.ms'
        else:
            self.G_MAXSCRIPT_NAME='renderu1.2.ms'
            
            
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
        maxPlugin=MaxPlugin(self.G_PROCESS_LOG,self.G_MAX_B,self.G_CG_VERSION,self.PLUGIN_DICT,self.G_PROGRAMFILES,self.G_SIMPLE_LOG)
        maxPlugin.config()
        
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
                self.RBcmd(copyMaxiniCmd)
            
            if os.path.exists(maxUserIni) and os.path.exists(maxEnu) :
                copyMaxiniCmd='xcopy /y /v /f "'+maxUserIni +'" "'+maxEnu.replace('\\','/')+'/"' 
                self.RBlog(copyMaxiniCmd)
                self.RBcmd(copyMaxiniCmd)
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
                self.RBcmd(copyDefaultMaxiniCmd)

        #------------custom.bat----------
        if os.path.exists(customBat):
            self.RBlog('执行custom.bat定制脚本')
            self.RBcmd(customBat)
            
        #------------host----------
        self.RBconfigHost(userHostFile)
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.end.....]')
        self.RBlog('done','end')
        
        #------------red shift license----------
        try:
            self.RBlog('environ redshift_license 5057@10.50.2.12')
            os.environ['redshift_license']='5057@10.50.2.12'
        except Exception, e:
            self.G_PROCESS_LOG.info('[err].red shift license env')
            self.G_PROCESS_LOG.info(e)
            
    def writeBat(self,renderFrame,cmdStr):
        #subst
        batFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,('render'+renderFrame+'_notrender.bat')).replace('\\','/')
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
        msFileObject.write('fn renderRun = (\r\n')
        mystr='rvRender "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+notRender+'" "'+renderFrame+'" "'+self.G_CG_TILE+'" "'+self.G_CG_TILECOUNT+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'"  "'+renderOutput+'/" "'+self.G_PLATFORM+'" "'+self.CURRENT_TASK+'"\r\n'
        print '\r\n\r\n\r\n\r\n\r\n+++++++++++++'
        print self.argsmap.has_key('from')
        if self.argsmap.has_key('from') and self.argsmap['from']=='web':
            mystr='fastRender "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+notRender+'" "'+renderFrame+'" "'+self.G_CG_TILE+'" "'+self.G_CG_TILECOUNT+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'"  "'+renderOutput+'/" "'+self.G_PLATFORM+'" "'+self.CURRENT_TASK+'" "web" "'+sceneFile+'" \r\n'
        self.RBlog('--------ms-------')
        self.RBlog(mystr)
        
        msFileObject.write(mystr)
        msFileObject.write(')\r\n')
        msFileObject.close()
        self.G_PROCESS_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
    
    def RBrenderCmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_RENDER_LOG.info(cmdStr)
        self.G_RENDER_LOG.info("\n\n-------------------------------------------Start max program-------------------------------------\n\n")
        
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        #cmdp.stdin.write('3/n')
        #cmdp.stdin.write('4/n')
        while True:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine == '' and cmdp.poll()!=None:
                break
            self.G_RENDER_LOG.info(resultLine)
            
            if '[End maxscript render]' in resultLine:
                self.maxKill(cmdp.pid)
                self.G_RENDER_LOG.info("\n\n-------------------------------------------End max program-------------------------------------\n\n")
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.G_RENDER_LOG.info('resultStr...'+resultStr)
        self.G_RENDER_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr
    
    def maxKill(self,parentId):
        self.G_RENDER_LOG.info('maxKill...start...\n')
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
        self.G_RENDER_LOG.info('maxKill...end...\n')
        

        
    def RBcgLog(self):
        self.RBlog('max日志和vray日志')
        self.G_RENDER_LOG.info('\n\n-----------------------------------------Max log file-------------------------------------\n\n')
        userProFile=os.environ["userprofile"]
        maxlog=userProFile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu\\Network\\Max.log'
        self.RBlog(maxlog)
        if os.path.exists(maxlog):
            maxLoglist=self.readFile(maxlog)
            for logStr in maxLoglist:
                self.G_RENDER_LOG.info(logStr)
        
        userTempFile=os.environ["temp"]
        myTempVrayLog=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
        self.RBlog(myTempVrayLog)
        self.G_RENDER_LOG.info('\n\n-----------------------------------------Vray log file-------------------------------------\n\n')
        if os.path.exists(myTempVrayLog):
            vrayLogList=self.readFile(myTempVrayLog)
            for logStr in vrayLogList:
                self.G_RENDER_LOG.info(logStr)
        
        self.G_RENDER_LOG.info('\n\n-----------------------------------------end-------------------------------------\n\n')
        
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
    
    def RBrender(self):#7
        self.RBlog('渲染','start')
        
        self.G_PROCESS_LOG.info('[Max.RBrender.start....]')
        startTime = time.time()
        mySonid='0'
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
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
        if  os.path.exists(netRenderTxt):
            
            self.G_RENDER_LOG.info('-------Net Render-------')
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
        if int(self.G_CG_TILECOUNT)>1:
            if self.G_CG_TILECOUNT==self.G_CG_TILE:#merge
                pass
            else:#block render
                renderOutput=os.path.join(self.G_RENDER_WORK_OUTPUT,('frame_'+renderFrame),('block_'+self.G_CG_TILE)).replace('\\','/')
        
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
        
        renderer=''
        if pluginDict.has_key('vray'):
            renderer='vray'+pluginDict['vray']
        standVrayStr=self.G_CG_VERSION+'_'+renderer
        
        self.G_PROCESS_LOG.info('\r\n\r\n==========================')
        self.G_PROCESS_LOG.info(standVrayStr)
        msFileNotRender=renderMsFile.replace('.ms','_notrender.ms')
        
        cmdStr = maxRenderExe+' -silent  -ma -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
        cmdStr2 = maxRenderExe+' -silent  -ma -mxs "filein \\"'+msFileNotRender+'\\";renderRun() "'
        if standVrayStr in standVrayList:
            cmdStr = maxRenderExe+'   -ma -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
            cmdStr2 = maxRenderExe+'   -ma -mxs "filein \\"'+msFileNotRender+'\\";renderRun() "'
        
        self.writeBat(renderFrame,cmdStr2)
        #cmdFool='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -start:'+renderFrame+' -end:'+renderFrame+' -o:'+renderOutput+'/test.tga "'+cgFile+'"'
        #cmdStr=cmdFool
        customUsers=['123456','1821122','1822553','964488','1833382','1818029','964497']
        if self.G_USERID in customUsers:
            if self.RENDER_CFG_PARSER.has_option('renderSettings','output'):
                cmdRenderOutput = self.RENDER_CFG_PARSER.get('renderSettings','output')
            if self.RENDER_CFG_PARSER.has_option('renderSettings','renderableCamera'):
                cmdRenderCam = self.RENDER_CFG_PARSER.get('renderSettings','renderableCamera')
            if self.RENDER_CFG_PARSER.has_option('renderSettings','width'):
                cmdRenderwidth = self.RENDER_CFG_PARSER.get('renderSettings','width')
            if self.RENDER_CFG_PARSER.has_option('renderSettings','height'):
                cmdRenderheight = self.RENDER_CFG_PARSER.get('renderSettings','height')
            
            cmdStr='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmaxcmd.exe" -start:'+renderFrame+' -end:'+renderFrame+' -o:"'+renderOutput+'/'+cmdRenderOutput+'" -camera:'+cmdRenderCam+' -w:'+cmdRenderwidth+' -h:'+cmdRenderheight+' -continueOnError "'+self.MAX_FILE.replace('\\','/')+'"'
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
        
        self.G_PROCESS_LOG.info('showdesktop.start')
        try:
            os.system('B:/tools/showDesktop.exe')
        except Exception, e:
            print 'exception in showDesktop'
            print e
        self.G_PROCESS_LOG.info('showdesktop.end')
        
        myT=None
        if os.path.exists(pySitePackagesNode):
            myT= MaxThread(300,self.G_TASKID,self.G_JOB_NAME,self.G_NODE_NAME,self.G_RENDER_WORK_TASK,self.G_PATH_GRAB,self.G_PROCESS_LOG)
            myT.start()
        cmdStr=cmdStr.encode(sys.getfilesystemencoding())
        self.RBrenderCmd(cmdStr,True,True)
        if myT!=None:
            myT.stop()
            
        print '\r\n\r\n------------------end render -----------\r\n\r\n\r\n'
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        
        self.delSubst()
        
        self.RBcgLog()
        

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
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        feeLogCmd='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'\\" '
        
        self.RBlog('uploadCmd='+uploadCmd)
        self.RBlog('frameCheckcmd='+frameCheckcmd)
        self.RBlog('bakCmd='+bakCmd)
        self.RBlog('feeLogCmd='+feeLogCmd)
        self.RBcmd(uploadCmd)
        self.RBcmd(frameCheckcmd)
        self.RBcmd(bakCmd)
        self.RBcmd(feeLogCmd)
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
        
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
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
        self.RBcmd(cmd2)
        
        
        self.RBlog(cmd3.decode(sys.getfilesystemencoding()))
        self.RBTry3cmd(cmd3)
        self.RBlog(cmd4)
        self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[Max.RBresultAction.end.....]')


class MaxPlugin():
    def __init__(self,processLog,maxB,cgVersion,pluginDict,g_programfiles,renderlog):
        print 'config lugin...'
        self.G_LOCAL_AUTODESK='C:/Program Files/Autodesk'
        self.G_PROCESS_LOG=processLog
        self.G_MAX_B=maxB
        self.G_PLUGIN_INI=self.G_MAX_B+'/ini'
        self.G_CG_VERSION=cgVersion
        self.G_PLUGIN_DICT=pluginDict
        self.G_PROGRAM_FILES=g_programfiles
        self.G_RENDER_LOG=renderlog
        
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            pluginDict['rayvision']='1.0.0'
            
        print "maxclient-----"
       
    def delete(self):
        print 'config lugin...',self.G_PROCESS_LOG
        self.G_PROCESS_LOG.info('\n\n-----------------------------------------Start Config plugin.delete-------------------------------------\n\n')
        defDelPath=self.G_MAX_B+ '/script/pluginBat/delFile.bat' 
        print 'defDelPath...',defDelPath
        self.G_RENDER_LOG.info('del plugins\n')
        delCmd='"'+defDelPath+'"'+' '+'"'+self.G_CG_VERSION+'"'
        if os.path.exists(defDelPath):
            self.G_PROCESS_LOG.info('pluginDelCmd------'+defDelPath)
            self.runcmd(delCmd)
            self.G_PROCESS_LOG.info('pluginDelCmd...finished\n')
            
    
    def getIncludeIni(self):
        self.G_PROCESS_LOG.info('\n\n-------------Start config ini -------------\n\n')
        self.G_PROCESS_LOG.info('getIncludeIni...start------\n')
        standIni=os.path.join(self.G_PLUGIN_INI,'standard',self.G_CG_VERSION,'plugin_include.ini').replace('\\','/')
        includeIniList=[]
        if os.path.exists(standIni):
            f=open(standIni)
            sourceinclude=f.read()
            f.close()
            includeIniList.append(sourceinclude)
            
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:  
                pluginVersion=pluginDict[pluginName]
                pluginPath=os.path.join(self.G_PLUGIN_INI,pluginName,pluginName+pluginVersion,self.G_CG_VERSION,'plugin_include.ini').replace('\\','/')
                if os.path.exists(pluginPath):
                    f=open(pluginPath)
                    sourceinclude=f.read()
                    f.close()
                    includeIniList.append(sourceinclude) 
                
        return includeIniList
        
    def getDirectoryIni(self):
        self.G_PROCESS_LOG.info('getDirectoryIni...start------\n')
        standIni=os.path.join(self.G_PLUGIN_INI,'standard',self.G_CG_VERSION,'plugin_directory.ini')
        directoryIniList=[]
        if os.path.exists(standIni):
            f=open(standIni)
            sourcedirectory=f.read()
            f.close()
            directoryIniList.append(sourcedirectory)
            
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:  
                pluginVersion=pluginDict[pluginName]
                pluginPath=os.path.join(self.G_PLUGIN_INI,pluginName,pluginName+pluginVersion,self.G_CG_VERSION,'plugin_directory.ini').replace('\\','/')
                if os.path.exists(pluginPath):
                    f=open(pluginPath)
                    sourcedirectory=f.read()
                    f.close()
                    directoryIniList.append(sourcedirectory)
        return directoryIniList
        
    def writeIni(self):
        self.G_PROCESS_LOG.info('writeIni...start------\n')
        includeIniList=self.getIncludeIni()
        directoryIniList=self.getDirectoryIni()
        targetPath=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION,'en-US','plugin.ini').replace('\\','/')
        if self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2012':
            targetPath=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION,'plugin.ini').replace('\\','/') 
        if os.path.exists(targetPath):
            os.system('del /s /q "%s"' % (targetPath)) 
            self.G_PROCESS_LOG.info('del ini'+targetPath+'\n')
        self.G_PROCESS_LOG.info('write ini to '+targetPath+'\n')
        f=open(targetPath,'wb')
        if includeIniList: 
            f.write('[Include]'+'\n')
            for includeIni in includeIniList:
                f.write(includeIni+'\n')
            
        if directoryIniList: 
            f.write('[Directory]'+'\n')
            for directoryIni in directoryIniList:
                f.write(directoryIni+'\n')
        self.G_PROCESS_LOG.info('write ini finished\n')
        f.close()    
        self.G_PROCESS_LOG.info('writeIni...end\n')
        
        
    def copyConfigPlugin(self):
        self.G_PROCESS_LOG.info('\n\n-------------start copy plugin-------------\n\n')
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:
                if pluginName=="vray":
                    pluginVersion=pluginDict[pluginName]
                    self.G_PROCESS_LOG.info('[Load Plugin]----'+pluginName+","+pluginName+pluginVersion)
                    self.G_RENDER_LOG.info('[Load Plugin]----'+pluginName+","+pluginName+pluginVersion)
                    srcDir=os.path.join(self.G_MAX_B,pluginName,pluginName+pluginVersion,self.G_CG_VERSION).replace('\\','/')
                    os.system('robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (srcDir,self.G_PROGRAM_FILES))
                    #pluginBatPath=os.path.join(self.G_MAX_B,pluginName,'script',pluginName + '.bat').replace('\\','/')
                    #cmdStr='"'+pluginBatPath+'" "'+self.G_CG_VERSION+'" "'+pluginName+'" "'+pluginName+pluginVersion+'" "'+self.G_MAX_B+'"'
                    #if os.path.exists(pluginBatPath):
                        #self.runcmd(cmdStr) 
            for pluginName in pluginDict:
                if pluginName=="vray":
                    pass
                else:
                    pluginVersion=pluginDict[pluginName]
                    self.G_PROCESS_LOG.info('[Load Plugin]----'+pluginName+","+pluginName+pluginVersion)
                    self.G_RENDER_LOG.info('[Load Plugin]----'+pluginName+","+pluginName+pluginVersion)
                    pluginBatPath=os.path.join(self.G_MAX_B,'script','pluginBat',pluginName + '.bat').replace('\\','/')
                    cmdStr='"'+pluginBatPath+'" "'+self.G_CG_VERSION+'" "'+pluginName+'" "'+pluginName+pluginVersion+'" "'+self.G_MAX_B+'"'
                    if os.path.exists(pluginBatPath):
                        self.runcmd(cmdStr)
                    else:
                        srcDir=os.path.join(self.G_MAX_B,pluginName,pluginName+pluginVersion,self.G_CG_VERSION).replace('\\','/')
                        dstDir=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION).replace('\\','/')
                        os.system('robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (srcDir,dstDir))
        self.G_PROCESS_LOG.info('Config Plugin...finished\n')
        self.G_RENDER_LOG.info('Config Plugin...finished\n')
    
    def runcmd(self,cmdStr):
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        while True:
            resultLine=cmdp.stdout.readline()
            if resultLine == '' and cmdp.poll()!=None:
                break
            self.G_PROCESS_LOG.info(resultLine)
        resultCode=cmdp.returncode
        
    def config(self):
        self.delete()
        self.writeIni()
        self.copyConfigPlugin()
        
        