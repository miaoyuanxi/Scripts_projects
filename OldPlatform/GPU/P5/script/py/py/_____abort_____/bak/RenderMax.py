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
        self.G_PROCESS_LOG.info('[Max.RBhanFile.start.....]')
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
        self.G_PROCESS_LOG.info('[Max.RBhanFile.end.....]')
    
    def RBcopyTempFile(self):
        self.G_PROCESS_LOG.info('[Max.RBcopyTempFile.start.....]')
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
        self.G_PROCESS_LOG.info('[Max.RBcopyTempFile.end.....]')
    
    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.start.....]')
        renderCfg=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.cfg')
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        self.RENDER_CFG_PARSER.read(renderCfg)
        
        self.G_PROCESS_LOG.info('[Max.readRenderCfg.end.....]')
        
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
        
    def RBloadPlugin(self):
        self.G_PROCESS_LOG.info('[Max.RVloadPlugin start]')
        self.G_PROCESS_LOG.info('\n\n------------------------------------------------------------[Start Config plugin]--------------------------------------------------------\n\n')
        cmdList=[]
        
        pluginDelCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "del"'
        self.G_PROCESS_LOG.info('pluginDelCmd------'+pluginDelCmd)
        self.G_PROCESS_LOG.info(pluginDelCmd+'\n')
        cmdList.append(pluginDelCmd)
        #self.RBcmd(pluginDelCmd)
        
        if 'vray' in self.G_CG_RENDER_VERSION:
            pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "vray" "'+  self.G_CG_RENDER_VERSION+'"'
            self.G_PROCESS_LOG.info('vraypluginCmd------'+pluginCmd)
            self.G_PROCESS_LOG.info(pluginCmd+'\n')
            cmdList.append(pluginCmd)
            #self.RBcmd(pluginCmd)

        allPlugDict=self.RBgetPluginDict()
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:
                pluginVersion=pluginDict[pluginName]
                if pluginName=='' or pluginVersion=='':
                    self.G_PROCESS_LOG.info('empty plugin...')
                else:
                    self.G_PROCESS_LOG.info('pluginName...'+ pluginName)
                    self.G_PROCESS_LOG.info('pluginVersion...'+ pluginVersion)
                    pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "'+ pluginName +'" "'+  pluginName+pluginVersion+'"'
                    self.G_PROCESS_LOG.info('pluginCmd------'+pluginCmd)
                    self.G_PROCESS_LOG.info(pluginCmd+'\n')
                    #self.RBcmd(pluginCmd)
                    cmdList.append(pluginCmd)
        maxCmd=self.G_RAYVISION_MAXBAT+' "'+self.G_CG_VERSION+'" "config"'
        self.G_PROCESS_LOG.info('maxCmd------'+maxCmd)
        self.G_PROCESS_LOG.info(maxCmd+'\n')
        cmdList.append(maxCmd)
        #self.RBcmd(maxCmd)
        
        self.G_RENDER_LOG.info('\n----------------cmd-------------------\n')
        for cmdStr in cmdList:
            self.G_RENDER_LOG.info(cmdStr)
        self.G_PROCESS_LOG.info('\n----------------execute cmd-------------------\n')
        for cmdStr in cmdList:
            self.RBcmd(cmdStr)

    def netPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        '''
        inputDataPath=r'//10.50.8.15/d/ninputdata5/'
        if self.RENDER_CFG_PARSER.has_option('client','storage_texture'):
            storage=self.RENDER_CFG_PARSER.get('client','storage_texture')
            if storage=='3443':
                inputDataPath=r'//10.50.8.16/d/inputdata5/'
        '''
        inputDataPath=self.argsmap['inputDataPath']
        mountFrom=self.argsmap['mountFrom']
        
        cleanMountFrom='try3 net use * /del /y'
        self.G_RENDER_LOG.info(cleanMountFrom)
        self.RBcmd(cleanMountFrom)
        
        pluginPath=self.argsmap['pluginPath']
        cmd='try3 net use B: '+pluginPath.replace('/','\\')
        self.G_RENDER_LOG.info(cmd) 
        self.RBcmd(cmd)
        
        
        projectPath=os.path.join(inputDataPath,self.G_USERID_PARENT,self.G_USERID,self.RENDER_CFG_PARSER.get('common','projectSymbol'),'max')
        cmd='try3 net use A: '+projectPath.replace('/','\\')
        self.G_RENDER_LOG.info(cmd) 
        self.RBcmd(cmd)
        '''
        if self.G_USERID=='962869' or (self.RENDER_CFG_PARSER.has_option('common','projectSymbol') and self.RENDER_CFG_PARSER.get('common','projectSymbol').endswith('_renderlocal')):
            projectPath=os.path.join(inputDataPath,self.G_USERID_PARENT,self.G_USERID,self.RENDER_CFG_PARSER.get('common','projectSymbol'),'max')
            cmd='try3 net use A: '+projectPath.replace('/','\\')
            self.G_RENDER_LOG.info(cmd) 
            self.RBcmd(cmd) 
        else:
            s=eval(mountFrom)
            for key in s.keys():
                cmd='try3 net use '+s[key]+' '+inputDataPath.replace('/','\\')+self.G_USERID_PARENT+key.replace('/','\\')
                self.G_RENDER_LOG.info(cmd)            
                self.RBcmd(cmd)
        '''
            
         
        
    def RBrenderConfig(self):#5
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.start.....]')
        
        
        #multicatter = getattr(self,'G_CG_SCATTER')
        #---------------------------------
        maxscriptPath='B:/plugins/max/script'
        maxscriptName='renderb_3_1_0.ms'#max2013,max204,max2015
        pluginBatName='plugin.bat'
        maxBatName='max.bat'
        customBatName='custom.bat'
        
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
        self.CURRENT_TASK='picture'
        
        if self.RENDER_CFG_PARSER.has_option('common','update'):
            scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
            scriptupdate=int(scriptupdateStr)
            if scriptupdate>20151000:
                maxscriptName='renderu.ms'
            
        if self.G_USERID=='962869':
            self.copyRenderFile()
        
        self.copyRenderFile()
        '''
        if self.RENDER_CFG_PARSER.has_option('common','projectSymbol'):
            projectSymbol=self.RENDER_CFG_PARSER.get('common','projectSymbol')
            if projectSymbol.endswith('_renderlocal'):
                self.copyRenderFile()
        '''
            
            
            
        if self.argsmap.has_key('currentTask'):
            self.CURRENT_TASK=self.argsmap['currentTask']

        customerScriptPath=os.path.join(maxscriptPath,self.G_USERID).replace('\\','/')
        
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            maxscriptName='rendera_3_1_0.ms'
            if self.RENDER_CFG_PARSER.has_option('common','update'):
                scriptupdateStr=self.RENDER_CFG_PARSER.get('common','update')
                scriptupdate=int(scriptupdateStr)
                if scriptupdate>20151000:
                    maxscriptName='rendera.ms'
        customerMs=os.path.join(customerScriptPath,maxscriptName).replace('\\','/')
        customerPluginBat=os.path.join(customerScriptPath,pluginBatName).replace('\\','/')
        customerMaxBat=os.path.join(customerScriptPath,maxBatName).replace('\\','/')
        customBat=os.path.join(customerScriptPath,customBatName).replace('\\','/')
        self.G_PROCESS_LOG.info('customBat------'+customBat)
        self.G_PROCESS_LOG.info('maxscriptName------'+maxscriptName)
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
            self.G_PROCESS_LOG.info('customCmd------>>>>')
            customCmd=customBat+' "'+self.G_TASKID+'"'
            self.G_PROCESS_LOG.info('customCmd------'+customCmd)
            self.RBcmd(customCmd)
                
        userprofile=os.environ["userprofile"]
        maxlog=userprofile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu\\Network\\Max.log'
        if os.path.exists(maxlog):
            try:
                os.remove(maxlog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)

        userTempFile=os.environ["temp"]
        myTempVrayLog=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
        if os.path.exists(myTempVrayLog):
            try:
                os.remove(myTempVrayLog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)

        self.RBloadPlugin()
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.end.....]')
        
    def writeMsFile(self,sceneFile,renderFrame,mySonid):

        self.G_PROCESS_LOG.info('[Max.writeMsFile.start.....]')
        #C:\users\enfuzion\AppData\Roaming\RenderBus\Profiles\users\cust\enfuzion\maxscript
        msFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.ms')
        msFile=msFile.replace('\\','/')
        self.G_PROCESS_LOG.info('msFile...'+msFile)
        print msFile
        # cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_RAYVISION_USER_ID+'\\" \\"'+self.G_RAYVISION_TASK_ID+'\\" \\"0\\" \\"'+framenum['startFrame']+'\\" \\"0\\" \\"'+self.G_RAYVISION_STARTFRAME+'\\" \\"'+sceneFile+'\\" \\"'+output+'\\" "'
        #sceneFile=sceneFile.decode('utf-8').encode('gbk')
        msFileObject=codecs.open(msFile,'a')
        msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
        msFileObject.write('filein @"'+self.G_RAYVISION_MAXMS+'"\r\n')
        msFileObject.write('fn renderRun = (\r\n')
        mystr='rvRender "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+mySonid+'" "'+renderFrame+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'" "'+sceneFile+'" "'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/" "'+self.G_PLATFORM+'" "'+self.CURRENT_TASK+'"\r\n'
        
        msFileObject.write(mystr)
        msFileObject.write(')\r\n')
        msFileObject.close()
        self.G_PROCESS_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
    
    def RBrenderCmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_RENDER_LOG.info(cmdStr)
        self.G_RENDER_LOG.info("\n\n--------------------------------------------------------------[Start max program]--------------------------------------------------------\n\n")
        
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
                self.G_RENDER_LOG.info("\n\n--------------------------------------------------------------[End max program]--------------------------------------------------------\n\n")
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
        self.G_RENDER_LOG.info('\n\n------------------------------------------------------------[Max log file]--------------------------------------------------------\n\n')
        userProFile=os.environ["userprofile"]
        maxlog=userProFile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu\\Network\\Max.log'
        if os.path.exists(maxlog):
            maxLoglist=self.readFile(maxlog)
            for logStr in maxLoglist:
                self.G_RENDER_LOG.info(logStr)
        
        userTempFile=os.environ["temp"]
        myTempVrayLog=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
        self.G_RENDER_LOG.info('\n\n------------------------------------------------------------[Vray log file]--------------------------------------------------------\n\n')
        if os.path.exists(myTempVrayLog):
            vrayLogList=self.readFile(myTempVrayLog)
            for logStr in vrayLogList:
                self.G_RENDER_LOG.info(logStr)
        
        self.G_RENDER_LOG.info('\n\n------------------------------------------------------------[end]--------------------------------------------------------\n\n')
        
    def getFlythroughtFrame(self):
        self.G_PROCESS_LOG.info('[Max.getFlythroughtFrame.start....]')
        renderFrame=self.G_CG_START_FRAME
        if self.RENDER_CFG_PARSER.has_option('vray','gi') and self.RENDER_CFG_PARSER.get('vray','gi')=='on':
            self.G_PROCESS_LOG.info('[Max.getFlythroughtFrame.start1....]')
            if self.RENDER_CFG_PARSER.has_option('vray','lightcacheMode') and  self.RENDER_CFG_PARSER.get('vray','lightcacheMode')=='1':
                if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                    self.G_PROCESS_LOG.info('[Max.getFlythroughtFrame.start2....]')
                    renderFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
                else:
                    self.G_PROCESS_LOG.info('[Max.getFlythroughtFrame.start3....]')
                    renderFrame=self.RENDER_CFG_PARSER.get('common','frames')
        self.G_PROCESS_LOG.info('[Max.getFlythroughtFrame.start....]')
        return renderFrame
    
    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[Max.RBrender.start....]')
        startTime = time.time()
        mySonid='0'
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        cgFile = self.argsmap['sceneFile'].replace('\\' , '/')
        
        if self.G_USERID=='962869':
            cgFilePath,cgFileName = os.path.split(cgFile)
            cgFile=os.path.join(self.G_RENDER_WORK_TASK,cgFileName).replace('\\','/')
            
        cgFilePath,cgFileName = os.path.split(cgFile)
        cgFile=os.path.join(self.G_RENDER_WORK_TASK,cgFileName).replace('\\','/')
        '''
        if self.RENDER_CFG_PARSER.has_option('common','projectSymbol'):
            projectSymbol=self.RENDER_CFG_PARSER.get('common','projectSymbol')
            if projectSymbol.endswith('_renderlocal'):
                cgFilePath,cgFileName = os.path.split(cgFile)
                cgFile=os.path.join(self.G_RENDER_WORK_TASK,cgFileName).replace('\\','/')
        '''
        renderFrame=self.G_CG_START_FRAME
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
                        renderFrame=self.getFlythroughtFrame()
                elif self.G_KG=='102':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        renderFrame=self.getFlythroughtFrame()
                else:
                    renderFrame=self.getFlythroughtFrame()
            else:
                if  self.G_KG=='100':
                    if self.argsmap.has_key('currentTask') and self.argsmap['currentTask'] in 'photon':
                        if self.RENDER_CFG_PARSER.has_option('vray','giframes'):
                            renderFrame=self.RENDER_CFG_PARSER.get('vray','giframes')
        
        self.G_PROCESS_LOG.info('renderframe='+renderFrame)
            
        maxRenderExe='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmax.exe"'
        if self.G_CG_VERSION=='3ds Max 2010':
            renderMsFile=self.writeMsFile(cgFile,renderFrame,mySonid)
            cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
        else:
            cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_USERID+'\\" \\"'+self.G_TASKID+'\\" \\"'+mySonid+'\\" \\"'+renderFrame+'\\" \\"'+self.G_KG+'\\" \\"'+self.G_JOB_NAME+'\\" \\"'+cgFile+'\\" \\"'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/\\" \\"'+self.G_PLATFORM+'\\" \\"'+self.CURRENT_TASK+'\\""'
        if isinstance(cmdStr,unicode):
            cmdStr=cmd.encode('utf-8')
        else:
            cmdStr.decode('gbk').encode('utf-8')
        self.RBrenderCmd(cmdStr,True,True)
        
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        
        self.RBcgLog()
        self.G_PROCESS_LOG.info('[Max.RBrender.end.....]')
        