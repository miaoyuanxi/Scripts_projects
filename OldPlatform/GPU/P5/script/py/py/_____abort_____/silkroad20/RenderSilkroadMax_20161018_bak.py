#! /usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import codecs
import string
import logging
reload(sys)
sys.setdefaultencoding('utf-8')


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
                    pluginBatPath=os.path.join(self.G_MAX_B,'script','pluginBat',pluginName + '.bat').replace('\\','/')
                    cmdStr='"'+pluginBatPath+'" "'+self.G_CG_VERSION+'" "'+pluginName+'" "'+pluginName+pluginVersion+'" "'+self.G_MAX_B+'"'
                    if os.path.exists(pluginBatPath):
                        self.runcmd(cmdStr)
                    else:
                        srcDir=os.path.join(self.G_MAX_B,pluginName,pluginName+pluginVersion,self.G_CG_VERSION).replace('\\','/')
                        dstDir=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION).replace('\\','/')
                        os.system('robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (srcDir,dstDir))
        self.G_PROCESS_LOG.info('Config Plugin...finished\n')
    
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

class RenderSilkroadMax():
    def __init__(self,**paramDict):
        self.G_SOURCE_FOLDER=paramDict['sourceFolder']
        self.G_SCRIPT_FOLDER=paramDict['scriptFile']
        self.G_WORK_RENDER=paramDict['workRender']
        self.G_ENV_PATH=paramDict['envPath']
        self.G_IP_BPATH=paramDict['bPath']
        self.G_MAXVERSION="3ds Max 2014"
        
        self.G_MAX_B=paramDict['maxB']
        self.G_PROGRAMFILES=paramDict['programFiles']
        self.G_CG_VERSION=paramDict['maxVersion']
        self.G_PLUGIN_DICT=eval(paramDict['pluginDict'])
        self.G_PROGRESS_LOG_PATH=paramDict['logPath']
        
        print 'self.G_SOURCE_FOLDER=',self.G_SOURCE_FOLDER
        print 'self.G_WORK_RENDER=',self.G_WORK_RENDER
        print 'self.G_IP_BPATH=',self.G_IP_BPATH
        print 'self.G_MAXVERSION=',self.G_MAXVERSION
        #print 'cgName=================='+cgName
        #exec('RenderAction.__bases__=('+cgName+',)')
        #exec(cgName+'.__init__(self,**paramDict)')
        
        
    #封装运行命令
    def rbCmd(self,cmdStr,continueOnErr=False,myShell=False):
        print cmdStr
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                print resultLine
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        print resultStr
        print resultCode
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr

    #
    def netPath(self):
        print 'net path start'
        netDelCmd = 'net use * /del /y'
        self.rbCmd(netDelCmd)
        netBcmd = 'net use B: ' + self.G_IP_BPATH
        self.rbCmd(netBcmd)
        pass

    #拷贝以存储的以下文件到节点机渲染
    #场景文件，素材文件
    def hanFile(self): 
        print 'hanFile start'
        #-------------maxscript file
        print 'maxscript'
        DelScript = 'del /F /S /Q ' + 'C:\script\max\ycxU.ms'
        print DelScript
        self.rbCmd(DelScript)
        scriptCmdStr = r'C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + self.G_SCRIPT_FOLDER.replace('/','\\') +'\\*.*" /to="c:\\script\\max\\"'
        print scriptCmdStr
        self.rbCmd(scriptCmdStr)
        
        taskPath=self.G_WORK_RENDER+"\\"+os.path.basename(self.G_SOURCE_FOLDER)
        if os.path.exists(taskPath):
            cleanCmd = 'rd /S /Q "' +taskPath +'"'
            print cleanCmd
            self.rbCmd(cleanCmd)
        
        #--------------env file
        print 'env'
        sourceEnv=os.path.join(self.G_ENV_PATH,'outdoor')
        doorTypePath=os.path.dirname(self.G_SOURCE_FOLDER)
        print doorTypePath
        if doorTypePath.lower().endswith('indoor'):
            sourceEnv=os.path.join(self.G_ENV_PATH,'indoor')

        envCmdStr = r'C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + sourceEnv.replace('/','\\') +'\\*.*" /to="' + self.G_WORK_RENDER +'\\'+os.path.split(self.G_SOURCE_FOLDER)[-1]+'\\env\\"'
        print envCmdStr
        self.rbCmd(envCmdStr)
        #----------------scene file 
        print 'scene'
        cmdStr = r'C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + self.G_SOURCE_FOLDER +'" /to="' + self.G_WORK_RENDER +'\\"'
        print cmdStr
        self.rbCmd(cmdStr)
        pass


    def initLog(self,processLogPath):
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        progressLog=logging.getLogger('processlog')
        progressLog.setLevel(logging.DEBUG)
        processLogHandler=logging.FileHandler(processLogPath)
        processLogHandler.setFormatter(fm)
        progressLog.addHandler(processLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        progressLog.addHandler(console)
        return progressLog
    
    #配置3dsmax软件
    #加载对应的vray版本和插件版本
    def configMax(self):
        print 'configMax start'

        G_PROGRESS_LOG=self.initLog(self.G_PROGRESS_LOG_PATH)

        maxPlugin=MaxPlugin(G_PROGRESS_LOG,self.G_MAX_B,self.G_CG_VERSION,self.G_PLUGIN_DICT,self.G_PROGRAMFILES,G_PROGRESS_LOG)
        maxPlugin.config()


    #调用渲染脚本，渲染场景
    def render(self):
        print 'render start'
        maxExe='"C:/Program Files/Autodesk/' + self.G_MAXVERSION +'/3dsmax.exe"'
        maxFileName=os.path.basename(self.G_SOURCE_FOLDER)
        maxFile= self.G_WORK_RENDER +'\\'+ maxFileName+'\\' + maxFileName+ '.max'
        envPath=self.G_WORK_RENDER +'\\'+ maxFileName+'\\env\\'
        renderCmd =  maxExe+" -silent -ma -mxs \"filein \\\"c:/script/max/ycxU.ms\\\";renderMaxYCX \\\"" +maxFile.replace('\\','/') + "\\\" \\\""+envPath.replace('\\','/')+"\\\" \""
        #print "%s" % renderCmd
        print renderCmd
        self.rbCmd(renderCmd,continueOnErr=True,myShell=False)
        pass



    #渲染结果处理
    #从节点机拷贝渲染结果回到服务器对应的位置
    def hanResult(self):
        print 'hanResult start'
        jpgFile = self.G_WORK_RENDER + '\\' + os.path.basename(self.G_SOURCE_FOLDER) + '\\' + os.path.basename(self.G_SOURCE_FOLDER + '.jpg')
        print jpgFile
        if os.path.exists(jpgFile):
            renderOutput = r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + jpgFile + '" /to="' + self.G_SOURCE_FOLDER +'\\"' 
            print renderOutput
            self.rbCmd(renderOutput)
        else:
            return -1
        pass



    #检查存储的渲染结果
    def checkResult(self):
        print 'checkResult start'
        jpgFile = self.G_SOURCE_FOLDER + '\\' + os.path.basename(self.G_SOURCE_FOLDER + '.jpg')
        #print jpgFile
        if os.path.exists(jpgFile):
            checkResult = '"' + self.G_SOURCE_FOLDER + '\\' + os.path.basename(self.G_SOURCE_FOLDER + '.jpg')
            print checkResult
        else:
            return -1
        #self.rbCmd(checkResult)
        pass
        
    def cleanThiTask(self):
        print 'cleanThiTask start'
        cleanCmd = 'rd /S /Q "' + self.G_WORK_RENDER+"\\"+os.path.basename(self.G_SOURCE_FOLDER)+'"'
        print cleanCmd
        try:
            print 'clean'
            #self.rbCmd(cleanCmd)
        except:
            pass
        pass

    def run(self):
        self.netPath()
        self.hanFile()
        self.configMax()
        self.render()
        self.hanResult()
        self.checkResult()
            



