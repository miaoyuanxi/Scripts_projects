import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

#---------------------calss maxclient--------------------
class MaxClient(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print 'Max.init...'
        self.G_MAXBAT_NAME='max.bat'
        self.G_RENDERBAT_NAME='crender.bat'        
        self.G_PLUGINBAT_NAME='plugin.bat'
        self.G_SCRIPT_NAME='crender.ms'
        
        self.G_CG_FILE=self.G_TASKID+'.max'
    
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_RENDER_LOG.info('[Max.RBhanFile.start.....]')
        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBcmd(moveOutputCmd)
        
        scriptmax=r'script\max'
        msFile=os.path.join(self.G_POOL,scriptmax,self.G_SCRIPT_NAME)
        maxBat=os.path.join(self.G_POOL,scriptmax,self.G_MAXBAT_NAME)
        renderBat=os.path.join(self.G_POOL,scriptmax,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(self.G_POOL,scriptmax,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        maxscript='c:/script/max'
        copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
        copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
        copyScriptCmd3='xcopy /y /f "'+msFile+'" "'+maxscript+'/" '
        copyScriptCmd4='xcopy /y /f "'+renderBat+'" "'+maxscript+'/" '
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        
        
        #self.RBcmd(copyScriptCmd1)
        
        #self.RBcmd(copyScriptCmd2)
        
        #self.RBcmd(copyScriptCmd3)
        
        #self.RBcmd(copyScriptCmd4)
        
        self.RBcmd(copyVBSCmd)
        
        '''
        oldMax=os.path.join(self.G_RENDER_WORK_TASK,os.path.basename(self.G_PATH_INPUTFILE))
        newMax=os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
        #if  os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        if  os.path.exists(oldMax) and not os.path.exists(newMax):
            oldMax = oldMax.replace('\\','/')
            newMax = newMax.replace('\\','/')
            print oldMax
            print newMax
            os.rename(oldMax,newMax)
        '''
        self.G_RENDER_LOG.info('[Max.RBhanFile.end.....]')
    
    def RBcopyTempFile(self):
        self.G_RENDER_LOG.info('[Max.RBcopyTempFile.start.....]')
    #copy temp file
        #if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
        tempFull=os.path.join(self.G_POOL_TASK,'*.*')
        copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
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
        self.G_RENDER_LOG.info('[Max.RBcopyTempFile.end.....]')

    def RBloadPlugin(self):
        self.G_RENDER_LOG.info('[Max.RVloadPlugin start]')
        self.G_RENDER_LOG.info('\n\n------------------------------------------------------------[Start Config plugin]--------------------------------------------------------\n\n')
        
        pluginDelCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "del"'
        self.G_RENDER_LOG.info('pluginDelCmd------'+pluginDelCmd)
        self.G_RENDER_LOG.info(pluginDelCmd+'\n')
        
        self.RBcmd(pluginDelCmd)
        
        if 'vray' in self.G_CG_RENDER_VERSION:
            pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "vray" "'+  self.G_CG_RENDER_VERSION+'"'
            self.G_RENDER_LOG.info('vraypluginCmd------'+pluginCmd)
            self.G_RENDER_LOG.info(pluginCmd+'\n')
            self.RBcmd(pluginCmd)

        allPlugDict=self.RBgetPluginDict()
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:
                pluginVersion=pluginDict[pluginName]
                self.G_RENDER_LOG.info('pluginName...'+ pluginName)
                self.G_RENDER_LOG.info('pluginVersion...'+ pluginVersion)
                pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "'+ pluginName +'" "'+  pluginName+pluginVersion+'"'
                self.G_RENDER_LOG.info('pluginCmd------'+pluginCmd)
                self.G_RENDER_LOG.info(pluginCmd+'\n')
                self.RBcmd(pluginCmd)
        maxCmd=self.G_RAYVISION_MAXBAT+' "'+self.G_CG_VERSION+'" "config"'
        self.G_RENDER_LOG.info('maxCmd------'+maxCmd)
        self.G_RENDER_LOG.info(maxCmd+'\n')
        self.RBcmd(maxCmd)

    def RBrenderConfig(self):#5
        self.G_RENDER_LOG.info('[Max.RBrenderConfig.start.....]')
        #multicatter = getattr(self,'G_CG_SCATTER')
        #---------------------------------
        maxscriptPath='B:/plugins/max/script'
        maxscriptName='renderU3_0_1.ms'
        pluginBatName='plugin.bat'
        maxBatName='max.bat'
        customBatName='custom.bat'
        
        self.G_KG=self.argsmap['kg']
        self.G_PATH_SMALL=self.argsmap['smallPath']
        self.G_SINGLE_FRAME_CHECK=self.argsmap['singleFrameCheck']
        self.G_PATH_COST=self.argsmap['pathCost']
        self.G_FIRST_FRAME=self.argsmap['firstFrame']

        self.G_ZONE=self.argsmap['zone']
        self.G_PATH_USER_OUTPUT=self.argsmap['output']
        self.G_CG_VERSION=self.argsmap['cgv']
        self.G_CG_RENDER_VERSION=self.argsmap['renderVersion']
        #-----------------------------------
        
        
        
        customerScriptPath=os.path.join(maxscriptPath,self.G_USERID).replace('\\','/')
        
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            maxscriptName='renderA3_0_1.ms'
        customerMs=os.path.join(customerScriptPath,maxscriptName).replace('\\','/')
        customerPluginBat=os.path.join(customerScriptPath,pluginBatName).replace('\\','/')
        customerMaxBat=os.path.join(customerScriptPath,maxBatName).replace('\\','/')
        customBat=os.path.join(customerScriptPath,customBatName).replace('\\','/')
        self.G_RENDER_LOG.info('customBat------'+customBat)
        
        self.G_RAYVISION_MAXMS=os.path.join(maxscriptPath,maxscriptName).replace('\\','/')
        if os.path.exists(customerMs):
            self.G_RAYVISION_MAXMS=customerMs
            
        self.G_RAYVISION_PLUGINBAT=os.path.join(maxscriptPath,pluginBatName).replace('\\','/')
        if os.path.exists(customerPluginBat):
            self.G_RAYVISION_PLUGINBAT=customerPluginBat
        
        self.G_RAYVISION_MAXBAT=os.path.join(maxscriptPath,maxBatName).replace('\\','/')
        if os.path.exists(customerMaxBat):
            self.G_RAYVISION_MAXBAT=customerMaxBat
        
        if os.path.exists(customBat):
            self.G_RENDER_LOG.info('customCmd------>>>>')
            customCmd=customBat+' "'+self.G_TASKID+'"'
            self.G_RENDER_LOG.info('customCmd------'+customCmd)
            self.RBcmd(customCmd)
        
        self.RBloadPlugin()
        self.G_RENDER_LOG.info('[Max.RBrenderConfig.end.....]')
        
    def writeMsFile(self,sceneFile,renderFrame,mySonid):
        self.G_RENDER_LOG.info('[Max.writeMsFile.start.....]')
        #C:\users\enfuzion\AppData\Roaming\RenderBus\Profiles\users\cust\enfuzion\maxscript
        msFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.ms')
        msFile=msFile.replace('\\','/')
        self.G_RENDER_LOG.info('msFile...'+msFile)
        print msFile
        # cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_RAYVISION_USER_ID+'\\" \\"'+self.G_RAYVISION_TASK_ID+'\\" \\"0\\" \\"'+framenum['startFrame']+'\\" \\"0\\" \\"'+self.G_RAYVISION_STARTFRAME+'\\" \\"'+sceneFile+'\\" \\"'+output+'\\" "'
        sceneFile=sceneFile.decode('utf-8').encode('gbk')
        msFileObject=codecs.open(msFile,'a')
        msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
        msFileObject.write('filein @"'+self.G_RAYVISION_MAXMS+'"\r\n')
        msFileObject.write('fn renderRun = (\r\n')
        mystr='rvRender "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+mySonid+'" "'+renderFrame+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'" "'+sceneFile+'" "'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/" "1005" ""\r\n'
        
        msFileObject.write(mystr)
        msFileObject.write(')\r\n')
        msFileObject.close()
        self.G_RENDER_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
        
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Max.RBrender.start.....]')
        startTime = time.time()
        #cgFile = os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
        #cgFile = cgFile.replace('\\' , '/')
        cgFile=self.argsmap['sceneFile']
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        mySonid='0'
        if hasattr(self,'G_SONID'):
            mySonid=self.G_SONID
        #renderCmd='c:/script/max/'+self.G_RENDERBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' '+mySonid+' ' +self.G_CG_START_FRAME  +' '+self.G_KG+' "'+self.G_JOB_NAME+'" "' +cgFile+'"'
        #self.RBcmd(renderCmd,True,False)
        maxRenderExe='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmax.exe"'
        if self.G_CG_VERSION=='3ds Max 2010':
            renderMsFile=self.writeMsFile(cgFile,self.G_CG_START_FRAME,mySonid)
            cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
        else:
            cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_USERID+'\\" \\"'+self.G_TASKID+'\\" \\"'+mySonid+'\\" \\"'+self.G_CG_START_FRAME+'\\" \\"'+self.G_KG+'\\" \\"'+self.G_JOB_NAME+'\\" \\"'+cgFile+'\\" \\"'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/\\" \\"1100\\" \\"\\""'
        
        self.RBcmd(cmdStr.decode('utf-8').encode('gbk'),True,False)
        
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Max.RBrender.end.....]')

        