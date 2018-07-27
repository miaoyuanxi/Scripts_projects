import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import commands
import codecs
from RenderBase import RenderBase

class Maya(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "MAYA INIT"
        self.G_SCRIPT_NAME='maya_preRender5.mel'
        self.G_RENDERBAT_NAME='render5.bat'
        self.G_RENDERBAT_NAME2='render5_test20180328.bat'
        self.G_PLUGINBAT_NAME='plugin.bat'
        if self.G_RENDEROS=='Linux':
            self.G_RENDERBAT_NAME='render5.sh'
            self.G_PLUGINBAT_NAME='plugin.sh'

    '''
        copy black.xml
    '''
    def copyBlack(self):
        # cmd="xcopy /y /f \"\\\\10.50.1.22\\td\\tools\\sweeper\\black.xml\" \"c:\\work\\munu_client\\sweeper\\\""
        # self.RBcmd(cmd)
        sweeper="c:\\work\\munu_client\\sweeper\\"
        #blackPath="\\\\10.50.1.22\\td\\tools\\sweeper\\black.xml"
        # blackPath="\\\\10.60.100.151\\td\\tools\\sweeper\\black.xml"
        blackPath="%s\\tools\\sweeper\\black.xml" % (self.PLUGINPATH.replace('/','\\'))
        if self.G_RENDEROS=='Linux':
            sweeper="/root/rayvision/work/munu_client/sweeper/"
            blackPath="\\B\\tools\\sweeper\\black.xml"
        self.pythonCopy(blackPath,sweeper)

    def removeOutput(self,count):
        try:
            if os.path.exists(self.G_RENDER_WORK_OUTPUT.replace('\\',"/")):
                shutil.rmtree(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"))
        except Exception, e:
            pass
        
        if not os.path.exists(self.G_RENDER_WORK_OUTPUT.replace('\\',"/")):
            os.makedirs(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"))
        else:
            count = count -1
            time.sleep(10)
            self.removeOutput(count)
            self.G_RENDER_LOG.info('[Maya.clearFile.failed.....]')
            if count==-1:
                sys.exists(-1)

    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]'+self.G_RENDERTYPE)
        
        if self.G_RENDERTYPE=="gpu":
            self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK_TASK,'output',self.G_CG_START_FRAME+'_'+self.G_CG_END_FRAME+'_'+self.G_CG_BY_FRAME)
            self.G_RENDER_WORK_OUTPUTBAK = os.path.join(self.G_RENDER_WORK_TASK,'outputbak',self.G_CG_START_FRAME+'_'+self.G_CG_END_FRAME+'_'+self.G_CG_BY_FRAME)
        if os.path.exists(self.G_RENDER_WORK_OUTPUT):
            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        self.removeOutput(10)
        scriptmaya=r'script\maya'
        melFile=os.path.join(self.G_POOL,scriptmaya,self.G_SCRIPT_NAME)
        renderBat=os.path.join(self.G_POOL,scriptmaya,self.G_RENDERBAT_NAME2)
        pluginBat=os.path.join(self.G_POOL,scriptmaya,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        
        mayascript='c:/script/maya'
        vbs="c:/script/vbs/"
        
        if self.G_RENDEROS=='Linux':
            mayascript='/root/rayvision/script/maya'
            vbs="/root/rayvision/script/vbs/"
            self.webMntPath()
        else:
            self.webNetPath()
        self.pythonCopy(melFile,mayascript)
        self.pythonCopy(renderBat,mayascript)
        #self.pythonCopy(pluginBat,mayascript)
        self.pythonCopy(vbsFile,vbs)
        
        self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
        
    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1,myLog=True)
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)
        #self.RBcmd(umountcmd)

        self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
        self.G_CONFIG = self.G_CONFIG.replace("\\","/")
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                for key in configJson["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
                    # self.G_RENDER_LOG.info(cmd)
                    self.RBcmd(cmd,False,1)
                    
    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            print configJson
            isContinue = False
            if isinstance(configJson["mntMap"],dict):
                if self.G_RENDERTYPE=="gpu":
                    isContinue = True
                for key in configJson["mntMap"]:
                    self.RBTry3cmd('net use "'+key+'" "'+configJson["mntMap"][key].replace('/','\\')+'"',isContinue)
                    
                            

    def RBrenderConfig(self):#5
        self.G_RENDER_LOG.info('[Maya.RBrenderConfig.start.....]')
        #multicatter = getattr(self,'G_CG_SCATTER')
        # if hasattr(self,'G_CG_RENDER_VERSION'):
            # if self.G_CG_RENDER_VERSION.startswith('arnold'):
                # self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.start.....]')
                # shortRenderVersion=self.G_CG_RENDER_VERSION.replace('arnold','')
                # configMultCmd='c:/script/maya/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' "arnold" "' +shortRenderVersion+'"'
                # self.RBcmd(configMultCmd,myLog=True)
                # self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.end.....]')
        self.G_RENDER_LOG.info('[Maya.RBrenderConfig.end.....]')
        
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
        # self.G_RENDER_LOG.info('kill sweeper.exe')
        # retcode = subprocess.call(r"taskkill /F /IM sweeper.exe /T ",shell=True)
        # self.G_RENDER_LOG.info('start sweeper.exe')
        # retcode = subprocess.call(r"start C:\sweeper\sweeper.exe",shell=True)
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
        mayaExePath=mayaExePath.replace('\\','/')
        renderTxtFile = ""
        #os.path.join(self.G_RENDER_WORK_TASK_CFG,os.path.basename(self.G_RENDER_TXTNAME))

        mayascript='c:/script/maya'
        vbs="c:/script/vbs/"
        if self.G_RENDEROS=='Linux':
            mayascript='/root/rayvision/script/maya'
            vbs="/root/rayvision/script/vbs/"
            mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'-x64/bin/mayapy'
            if not os.path.exists(mayaExePath):
                mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'/bin/mayapy'
            renderTxtFile = ""
            #os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_RENDER_TXTNAME[self.G_RENDER_TXTNAME.rfind("\\")+1:len(self.G_RENDER_TXTNAME)])
        renderTxtFile=renderTxtFile.replace('\\','/')

        melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME2)
        pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(vbs,self.G_CONVERTVBS_NAME)
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            if isinstance(configJson["common"],dict):
                self.G_PATH_INPUTFILE=configJson["common"]["cgFile"]
                print self.G_PATH_INPUTFILE
        
         #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" "'+ self.G_PLUGINS+'" "'+ self.G_CG_TILE+'" "'+ self.G_CG_TILECOUNT+'" '
        
        renderCmd2 = r'"C:/Program Files/Autodesk/maya2018/bin/render.exe" -s 1 -e 10000 -b 1 -proj "" -rd "c:/work/render/9999999/output/22222/" -preRender "_RV_RSConfig;" -r redshift -logLevel 2 -log "D:/test_gpu_new.txt" -gpu {0,1} "N:/TD_test_gpu/maya2018_rs2560.ma"'
        
        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,1,myLog=True)
        # self.RBcmd(renderCmd2,False,myLog=True)
        os.system('start "" /WAIT %s' % renderCmd2)
        
        
        
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')

    def denoise(self):
        self.G_RENDER_LOG.info('[Maya.denoise.start.....]')
        startTime = time.time()
        
        #os.environ["RMSTREE"] = 'B:\\custom_config\\1843630\\rms_copy\\RenderManForMaya-21.3-maya2015\\RenderManForMaya-21.3-maya2015'
        #os.environ["RMANTREE"] = 'B:\\custom_config\\1843630\\rms_copy\\RenderManForMaya-21.3-maya2015\\RenderManProServer-21.3'
        #licenseCmd=""

        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        denoiseObj=self.getDenoiseFile()
        print "* * * "*20
        print denoiseObj
        print "* * * "*20
        exe = 'B:\\plugins\\maya\\rmps\\RenderManProServer-21.3\\bin\\denoise.exe'
        exeEnviron = os.getenv("RMANTREE")
        pyPath="B:\\scripts\\Maya\\denoise_maya.py"
        if exeEnviron!=None and exeEnviron!='':
            exe = exeEnviron+'\\bin\\denoise.exe'
        for key in denoiseObj:
            denoiseFile = key.replace("###","{"+denoiseObj[key]+"}")
            #denoiseCmd = '"'+exe+'" --crossframe -v variance -f default.filter.json "'+denoiseFile+'"'
            denoiseCmd = 'C:\\Python27\\python.exe '+pyPath+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+denoiseFile+'" "'+self.G_PLUGINS+'"'
            print denoiseCmd
            self.RBcmd(denoiseCmd,False,1,myLog=True)

        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.denoise.end.....]')

    def getDenoiseFile(self):
        rootdir = self.G_PATH_USER_OUTPUT
        fileobj={}
        for parent,dirnames,filenames in os.walk(rootdir):
            for filename in filenames:
                if 'variance' in filename:
                    filePath=os.path.join(parent,filename)
                    if "variance_" in filePath:
                        nameArray=filePath.split('variance_')
                        name=nameArray[1].split(".")
                        key = nameArray[0]+'variance_'+"###."+name[1]
                        if fileobj.has_key(key):
                            fileobj[key]=fileobj[key]+','+name[0]
                        else:
                            fileobj[key]=name[0]
                    elif  "variance." in filePath:
                        nameArray=filePath.split('variance.')
                        print nameArray
                        name=nameArray[1].split(".")
                        key = nameArray[0]+'variance.'+"###."+name[1]
                        if fileobj.has_key(key):
                            fileobj[key]=fileobj[key]+','+name[0]
                        else:
                            fileobj[key]=name[0]
        return fileobj


    def RBcmd(self,cmdStr,continueOnErr=False,myShell=False,myLog=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        if myLog:
            self.G_PROCESS_LOG.info('cmd...'+cmdStr)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        exitcode = 0
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                if "License error" in resultLine or "[mtoa] Failed batch render" in resultLine or "error checking out license for arnold" in resultLine or "No license for product (-1)" in resultLine:
                    exitcode = -1
                if myLog:
                    self.G_PROCESS_LOG.info(resultLine)
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode

        if myLog:
            self.G_PROCESS_LOG.info('resultStr...'+resultStr)
            self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
            self.G_PROCESS_LOG.info('exitcode...'+str(exitcode))
        if exitcode==-1:
            sys.exit(-1)

        if not continueOnErr:
            if myLog:
                self.G_PROCESS_LOG.info('resultStr...-----'+resultStr)
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr

    def gpuDelNet(self):
        self.G_PROCESS_LOG.info('gpu...delNetUse')
        userFilePath = "D:\\work\\user\\userId.txt"
        userId=self.G_USERID
        isSame=False
        if os.path.exists(userFilePath):
            rbModel = codecs.open(userFilePath,"r","utf-8")
            lines = rbModel.readlines()
            for line in lines:
                if userId in line:
                    isSame = True
            rbModel.close()
        if not isSame:
            folder = "D:\\work\\user\\";
            if not os.path.exists(folder):
                os.makedirs(folder) 
            self.delNetUse()
            rb=codecs.open(userFilePath,'w') 
            try :
                rb.write(userId.encode("UTF-8"))
            finally :
                rb.close()
    def waitting(self):
        self.G_PROCESS_LOG.info('waitting---start')
        # time.sleep(60)
        self.G_PROCESS_LOG.info('waitting---end')

    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.G_PATH_SMALL):
            os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',"SingleFrameCheck.exe")
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        if self.G_RENDEROS=='Linux':
            outputPath="/output"
            ouputbakPath="/outputbak"
            feePath="/fee"
            spPath = "outputdata5"
            outputFolder=self.G_PATH_USER_OUTPUT[self.G_PATH_USER_OUTPUT.rfind(spPath)+len(spPath):len(self.G_PATH_USER_OUTPUT)]
            outputMntpath =  self.G_PATH_USER_OUTPUT.replace(outputFolder,'').replace('\\','/')
            outputmnt='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+outputMntpath+' '+outputPath
            feemnt='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+self.G_PATH_COST.replace('\\','/')+' '+feePath
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)
            if not os.path.exists(feePath):
                os.makedirs(feePath)
            self.RBcmd(outputmnt,False,1)
            self.RBcmd(feemnt,False,1)
            outputPath=outputPath+outputFolder.replace("\\","/")
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),outputPath)
            self.userOutputPath=outputPath
            if self.G_TASKID=="9215495":
                self.pythonMove(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
            else:
                self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\','/'),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
            self.pythonCopy(feeTxt,"/fee")
        else:
            output=self.G_PATH_USER_OUTPUT
            if self.G_CG_TILECOUNT !='1' and self.G_CG_TILECOUNT!=self.G_CG_TILE:
                output=self.G_PATH_TILES

            
            cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+output+'"'
            cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ output.rstrip()+'"'
            cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
            cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST.replace('/','\\')+'/" '
            if not self.G_CG_OPTION=='denoise':
                self.RBTry3cmd(cmd1)
                
                try:
                    self.checkResult()
                except Exception, e:
                    print '[checkResult.err]'
                    print e
                
                
                self.RBcmd(cmd2,myLog=True)
                self.RBTry3cmd(cmd3)
            self.RBcmd(cmd4,myLog=True)			
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

    def RBexecute(self):#Render
        self.RBBackupPy()
        self.RBinitLog()
        self.waitting()
        self.G_RENDER_LOG.info('[MAYA.RBexecute.start...]')
        self.RBnodeClean()
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()


        self.RBreadCfg()
        if self.G_RENDEROS=='Linux':
            print 'no Subst'
        else:
            print 'no Subst-------'
            if not self.G_RENDERTYPE=="gpu":
                print 'no Subst-------sdsd'
                self.delSubst()
                self.delNetUse()
            else:
                self.gpuDelNet()
            self.copyBlack()
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.resourceMonitor()
        if self.G_CG_OPTION=='denoise':
            self.denoise()
        else:
            self.RBrender()
            if self.G_RENDEROS=='Linux':
                print 'no smallpic'
            else:
                self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Maya.RBexecute.end.....]')

#--------------------- maya express--------------------	
class MayaExpress(Maya):
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
        # self.G_RENDER_LOG.info('kill sweeper.exe')
        # retcode = subprocess.call(r"taskkill /F /IM sweeper.exe /T ",shell=True)
        # self.G_RENDER_LOG.info('start sweeper.exe')
        # retcode = subprocess.call(r"start C:\sweeper\sweeper.exe",shell=True)
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
        mayascript='c:/script/maya'
        vbs="c:/script/vbs/"
        if self.G_RENDEROS=='Linux':
            mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'-x64/bin/mayapy'
            if not os.path.exists(mayaExePath):
                mayaExePath='/usr/autodesk/'+self.G_CG_VERSION+'/bin/mayapy'
            mayascript='/root/rayvision/script/maya'
            vbs="/root/rayvision/script/vbs/"
        mayaExePath=mayaExePath.replace('\\','/')
            
        melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(vbs,self.G_CONVERTVBS_NAME)
         #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" "'+ self.G_CG_TILE+'" "'+ self.G_CG_TILECOUNT+'" '
        
        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,False,myLog=True)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
        
        
#--------------------- maya Client--------------------	
class MayaClient(Maya):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "MAYA INIT"
        self.G_SCRIPT_NAME='maya_preRender5.mel'
        self.G_RENDERBAT_NAME='crender.bat'
        self.G_PLUGINBAT_NAME='plugin.bat'
    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[Maya.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        self.G_PROCESS_LOG.info('[G_CG_VERSION.....]'+self.G_CG_VERSION)
        mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
        self.G_PROCESS_LOG.info('[G_CG_VERSION.....]'+mayaExePath)
        self.G_PROCESS_LOG.info('[G_PATH_INPUTPROJECT.....]'+self.G_PATH_INPUTPROJECT)
        self.G_PROCESS_LOG.info('[G_USERID_PARENT.....]'+self.G_USERID_PARENT)
        
        mayaExePath=mayaExePath.replace('\\','/')
        mayascript='c:/script/maya'
        melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
        
        subStr=self.G_USERID
        if self.G_USERID_PARENT==self.G_USERID:
            subStr=self.G_USERID_PARENT+'\\'+self.G_USERID
        self.G_PROCESS_LOG.info('[subStr.....]'+subStr)
        projectPath = self.G_PATH_INPUTPROJECT[0:self.G_PATH_INPUTPROJECT.index(subStr)+len(subStr)]
        self.G_PROCESS_LOG.info('[projectPath.....]'+projectPath)
         #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ projectPath +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CG_TILE+'" "'+ self.G_CG_TILECOUNT+'" '
        
        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,False,myLog=True)
        self.G_RENDER_LOG.info('[Maya.end.....]')
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')