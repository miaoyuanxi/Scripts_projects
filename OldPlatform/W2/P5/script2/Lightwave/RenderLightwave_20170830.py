import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Lightwave(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Lightwave INIT"
        self.G_SCRIPT_NAME='Lightwave_preRender5.mel'
        self.G_RENDERBAT_NAME='render5.bat'
        self.G_PLUGINBAT_NAME='plugin.bat'

    
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.delSubst()
        self.G_RENDER_LOG.info('[Lightwave.RBhanFile.start.....]')
        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        self.RBcmd(moveOutputCmd,myLog=True)
        
        scriptLightwave=r'script\Lightwave'
        melFile=os.path.join(self.G_POOL,scriptLightwave,self.G_SCRIPT_NAME)
        renderBat=os.path.join(self.G_POOL,scriptLightwave,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(self.G_POOL,scriptLightwave,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
        
        Lightwavescript='c:/script/Lightwave'
        copyScriptCmd1='xcopy /y /f "'+melFile+'" "'+Lightwavescript+'/" '
        copyScriptCmd2='xcopy /y /f "'+renderBat+'" "'+Lightwavescript+'/" '
        copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+Lightwavescript+'/" '
        copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
        
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            print configJson
            self.CGSOFT=configJson['common']["cgSoftName"]
            projectName= configJson['common']["projectSymbol"]
            replacePath="\\"+projectName+"\\"+self.CGSOFT+"\\"
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y",myLog=True)
                for key in configJson["mntMap"]:
                    newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
                    # self.RBcmd("net use "+key+" "+newPath)
                    self.RBcmd("net use "+key+" \""+newPath+"\"",myLog=True)

        
        self.RBcmd(copyScriptCmd1,myLog=True)
        self.RBcmd(copyScriptCmd2,myLog=True)
        self.RBcmd(copyScriptCmd3,myLog=True)
        self.RBcmd(copyVBSCmd,myLog=True)
        self.G_RENDER_LOG.info('[Lightwave.RBhanFile.end.....]')
        
        
    def RBrenderConfig(self):#5
        self.G_RENDER_LOG.info('[Lightwave.RBrenderConfig.start.....]')
        #multicatter = getattr(self,'G_CG_SCATTER')
        if hasattr(self,'G_CG_RENDER_VERSION'):
            if self.G_CG_RENDER_VERSION.startswith('arnold'):
                self.G_RENDER_LOG.info('[Lightwave.RBrenderConfig.arnold.start.....]')
                shortRenderVersion=self.G_CG_RENDER_VERSION.replace('arnold','')
                configMultCmd='c:/script/Lightwave/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' "arnold" "' +shortRenderVersion+'"'
                self.RBcmd(configMultCmd,myLog=True)
                self.G_RENDER_LOG.info('[Lightwave.RBrenderConfig.arnold.end.....]')
        self.G_RENDER_LOG.info('[Lightwave.RBrenderConfig.end.....]')
        
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Lightwave.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        LightwaveExePath=os.path.join('B:/NewTek/',self.G_CG_VERSION,'bin/lwsn.exe')
        LightwaveExePath=LightwaveExePath.replace('\\','/')
        renderTxtFile = ""
        #os.path.join(self.G_RENDER_WORK_TASK_CFG,os.path.basename(self.G_RENDER_TXTNAME))
        #renderTxtFile=renderTxtFile.replace('\\','/')
        
        Lightwavescript='c:/script/Lightwave'
        melFile=os.path.join(Lightwavescript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(Lightwavescript,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(Lightwavescript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
        outputrenderlogFile = os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'_render.log')).replace("/", "\\")
         #C:/script/Lightwave/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+LightwaveExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" "'+ self.G_PLUGINS+'" '+ ' >>' + '"' + outputrenderlogFile +'"'

        self.G_PROCESS_LOG.info("Cmds: %s"%renderCmd)
        if self.G_RENDEROS=='Linux':
            self.RBcmd(renderCmd,True,1,myLog=True)
        else:
            ## ------------------------------------------------------------------------------------
            #os.system(renderCmd)
            TL_result = subprocess.Popen(renderCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            r_err = ''
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_PROCESS_LOG.info(r_info)
                    r_err = r_info
            #r_result = TL_result.wait()
            r_code = TL_result.returncode
            #r_err = TL_result.stderr.read()
            self.G_PROCESS_LOG.info("RenderCmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")

        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,False,myLog=True)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Lightwave.RBrender.end.....]')

    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
        #RB_small
        if not os.path.exists(self.G_PATH_SMALL):
            os.makedirs(self.G_PATH_SMALL)
        frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
        feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
        feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
        
        cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+self.G_PATH_USER_OUTPUT+'"'
        cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ self.G_PATH_USER_OUTPUT+'"'
        cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'

        cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '

        self.RBTry3cmd(cmd1)
        self.RBcmd(cmd2,myLog=True)
        self.RBTry3cmd(cmd3)
        self.RBcmd(cmd4,myLog=True)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')
        
    def RBexecute(self):#Render
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Lightwave.RBexecute.start...]')
        self.RBprePy()
        self.RBmakeDir()
        
        self.RBcopyTempFile()
        self.RBreadCfg()
        self.RBhanFile()
        
        
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Lightwave.RBexecute.end.....]')

#--------------------- Lightwave express--------------------    
class LightwaveExpress(Lightwave):
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Lightwave.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        LightwaveExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
        LightwaveExePath=LightwaveExePath.replace('\\','/')
        Lightwavescript='c:/script/Lightwave'
        melFile=os.path.join(Lightwavescript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(Lightwavescript,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(Lightwavescript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
         #C:/script/Lightwave/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+LightwaveExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" '
        
        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,False,myLog=True)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Lightwave.RBrender.end.....]')
        
        
#--------------------- Lightwave Client--------------------    
class LightwaveClient(Lightwave):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Lightwave INIT"
        self.G_SCRIPT_NAME='Lightwave_preRender5.mel'
        self.G_RENDERBAT_NAME='crender.bat'
        self.G_PLUGINBAT_NAME='plugin.bat'
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Lightwave.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))
        self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+self.G_CG_VERSION)
        LightwaveExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
        self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+LightwaveExePath)
        LightwaveExePath=LightwaveExePath.replace('\\','/')
        Lightwavescript='c:/script/Lightwave'
        melFile=os.path.join(Lightwavescript,self.G_SCRIPT_NAME)
        renderBat=os.path.join(Lightwavescript,self.G_RENDERBAT_NAME)
        pluginBat=os.path.join(Lightwavescript,self.G_PLUGINBAT_NAME)
        vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
         #C:/script/Lightwave/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
        renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+LightwaveExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" '
        
        #os.system(renderCmd)
        self.RBcmd(renderCmd,False,False,myLog=True)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Lightwave.RBrender.end.....]')