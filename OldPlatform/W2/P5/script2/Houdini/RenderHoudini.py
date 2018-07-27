import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Houdini(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Houdini INIT"
        self.G_RENDERBAT_NAME='Erender_HD.bat'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV="";
        self.CGFILE="";
        self.houdiniScript='c:/script/houdini'

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
        self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')

        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        if os.path.exists(self.G_RENDER_WORK_OUTPUT):
            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        self.removeOutput(10)
        if not self.G_RENDEROS=='Linux':
            scriptHoudini=r'script\houdini'
            renderBat=os.path.join(self.G_POOL,scriptHoudini,self.G_RENDERBAT_NAME)
            
            vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
            
            copyScriptCmd='xcopy /y /f "'+renderBat+'" "'+self.houdiniScript+'/" '
            copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
            
            self.RBcmd(copyScriptCmd)
            self.RBcmd(copyVBSCmd)
            self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
    
    def ExtInfo(self,file='',info='',towrite=True,toprint=True,types="w"):

        if info == "" and not file=='':
            infos = "Render Log start at: %s"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            infos += "\nSoftware: HOUDINI"
            with open(file,"w")as f:
                f.write(infos+"\n")
                f.close()
        elif not file=='':
            time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
            infos = "["+str(time_point) + "] " + str(info)

            if os.path.isfile(file):
                if types == "w":
                    with open(file,types)as f:
                        f.write("\n"+infos)
                        f.close()
                    if toprint:
                        print(infos)
                    print("Write to file")
                else:
                    types = "a"
                    with open(file,types)as f:
                        f.write("\n"+infos)
                        f.close()
                    if toprint:
                        print(infos)
                    print("Add to file")



    def RBrender(self):#7

        # ADD BY CHENZHONG
        os.environ['CID_INPUT_ROOT'] = self.G_PATH_INPUTPROJECT
        os.environ['TID_OUTPUT_ROOT'] = self.G_PATH_USER_OUTPUT
        # ADD BY CHENZHONG
        
        
        self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        renderBat=os.path.join(self.houdiniScript,self.G_RENDERBAT_NAME)
        #vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
        # "c:/script/Houdini/Erender.bat" "$userId" "$taskId" "$startFrame" "$endFrame" "$frameStep" "$cgv" "$projectPath" "$filePath" "$output"  "$layerName" "$option"" 
        #renderCmd='c:\\Python27\\python.exe '+renderPy +' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" "'+self.G_CG_OPTION+'"' 
        python_used = "C:/Python27/python.exe"
        renderScript= python_used+" B:\\plugins\\houdini\\Erender.py"

        ##-----------------------------------------------------------------
        ## Edit by shen, RS render 
        _RS_render = True
        '''
        if not self.G_RENDEROS=='Linux':
            json_path = r"B:\plugins\houdini\lib"
            sys.path.append(json_path)
            import dojson
            if os.path.exists("D:/work/render/%s" % self.G_TASKID):
                p_info = dojson.main(self.G_TASKID,'render')
                print(p_info)
                if len(p_info):
                    if p_info[0] == "RS":
                        _RS_render = True
        '''

        ##-----------------------------------------------------------------

        _log_file = "C:/log/render/%s/%s_render.log"%(self.G_TASKID,self.G_JOB_NAME)
        if _RS_render:
            renderScript = python_used + ' B:\\plugins\\houdini\\bin\\RSLogin.py'
            renderCmd =renderScript+' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" '+_log_file+' Render'
            renderCmd_info = renderCmd
            # self.G_PROCESS_LOG.info("RS_Cmds: %s"%renderCmd_info)
            self.G_PROCESS_LOG.info("Input: %s"%self.G_PATH_INPUTPROJECT)
            self.G_PROCESS_LOG.info("Output: %s"%self.G_PATH_USER_OUTPUT)
        else:
            renderCmd =renderScript+' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" "'+self.G_CG_OPTION+'" "'+self.G_PATH_INPUTPROJECT+'" "'+self.G_PATH_USER_OUTPUT+'" '
            renderCmd_info = renderCmd.replace(' "'+self.G_PATH_INPUTPROJECT+'" "'+self.G_PATH_USER_OUTPUT+'"',"")
            # self.G_PROCESS_LOG.info("Cmds: %s"%renderCmd_info)
            self.G_PROCESS_LOG.info("Input: %s"%self.G_PATH_INPUTPROJECT)
            self.G_PROCESS_LOG.info("Output: %s"%self.G_PATH_USER_OUTPUT)

        if self.G_RENDEROS=='Linux':
            renderScript="/B/plugins/houdini/Linux/Erender.sh"
            renderCmd =renderScript+' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.CGFILE+'" "'+self.G_CG_LAYER_NAME+'" "'+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'" "'+self.G_CG_OPTION+'" "'+self.G_PATH_INPUTPROJECT+'" "'+self.G_PATH_USER_OUTPUT+'" '
            self.G_PROCESS_LOG.info("G_RENDEROS: Linux")
        self.G_PROCESS_LOG.info("Cmds: %s"%renderCmd)

        if "-R" in self.G_CG_OPTION:
            renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+self.CGV+'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.CGFILE+'" "' +self.G_RENDER_WORK_OUTPUT+'"  "'+self.G_CG_LAYER_NAME+'" "'+self.G_CG_OPTION+'" "'+self.G_PATH_USER_OUTPUT+'" ' 
        self.G_RENDER_LOG.info(renderCmd)

        if self.G_RENDEROS=='Linux':
            #self.RBcmd(renderCmd,True,1)
            r_code = os.system(renderCmd)
            self.G_PROCESS_LOG.info("RenderCmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")
                #sys.exit(r_code)
        else:
            ## ------------------------------------------------------------------------------------
            #os.system(renderCmd)
            get_log_name = True if not self.G_JOB_NAME=="" else False
            render_log = "%s/%s/%s_render.log"%(self.G_LOG_WORK,self.G_TASKID,self.G_JOB_NAME)
            if not get_log_name:
                render_log = "%s/%s/frame%s_render.log"%(self.G_LOG_WORK,self.G_TASKID,self.G_CG_START_FRAME.zfill(4)) if self.G_CG_START_FRAME==self.G_CG_END_FRAME else "C:/log/render/%s/frame%s-%s_render.log"%(self.G_TASKID,self.G_CG_START_FRAME.zfill(4),self.G_CG_END_FRAME.zfill(4))

            self.G_PROCESS_LOG.info("Render_log: %s"%render_log)
            if not os.path.exists(os.path.dirname(render_log)):
                os.makedirs(os.path.dirname(render_log))

            ## ExtInfo(self,file='',info='',towrite=True,toprint=True,types="w"):
            self.ExtInfo(render_log,'')

            TL_result = subprocess.Popen(renderCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            linux_ext = 0
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_PROCESS_LOG.info(r_info)
                    if self.G_RENDEROS=='Linux' and linux_ext:
                        self.ExtInfo(render_log,r_info,1,0,"a")
                        linux_ext += 1
                    r_err = r_info

            r_code = TL_result.returncode
            self.G_PROCESS_LOG.info("RenderCmd return:"+str(r_code))
            if r_code:
                self.G_PROCESS_LOG.info("Error Print :")
                self.G_PROCESS_LOG.info("\n"+r_err+"\n")
                if self.G_RENDEROS=='Linux':
                    self.ExtInfo(render_log,"Error Print :",1,0,"a")
                    self.ExtInfo(render_log,("\n"+r_err+"\n"),1,0,"a")
            ## ----------------------------------------------------------------------------------
        #self.RBcmd(renderCmd,True,1)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            print self.G_CONFIG
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=''#configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    mnt_value = configJson["mntMap"][key].replace('/','\\')
                    if os.path.exists(mnt_value):
                        cmds = 'net use %s "%s"'%(key,mnt_value)
                        self.RBcmd(cmds)
                        self.G_PROCESS_LOG.info(cmds)
                    else:
                        self.G_PROCESS_LOG.info('[warn]The path is not exist:%s' % mnt_value)

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1)
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

    def copyHoudiniFile(self):
        cgvName =self.CGV.replace(".","")
        pluginPath="B:\\plugins\\houdini\\apps\\7z\\"+cgvName+".7z"
        localPath = "D:\\plugins\\houdini\\";
        if not os.path.exists(localPath+cgvName+"\\") or not os.listdir(localPath+cgvName+"\\"):
            if not os.path.exists(localPath+cgvName+".7z"):
                copyCmd = 'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +pluginPath +'" /to="'+localPath+'"'
                self.RBcmd(copyCmd)
            unpackCmd=self.G_DRIVERC_7Z+' x "'+localPath+cgvName+".7z"+'" -y -aos -o"'+localPath+cgvName+'\\"' 
            self.RBcmd(unpackCmd)

    def RBresultAction(self):
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.start.....]')
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
            # outputmnt='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+outputMntpath+' '+outputPath
            # feemnt='mount -t cifs -o username=administrator,password=Rayvision@2016,codepage=936,iocharset=gb2312 '+self.G_PATH_COST.replace('\\','/')+' '+feePath
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
            
            self.RBTry3cmd(cmd1)
            if float(self.G_CG_OPTION) <0:
                self.RBcmd(cmd2)

            self.RBTry3cmd(cmd3)
            self.RBcmd(cmd4)
        self.G_PROCESS_LOG.info('[BASE.RBresultAction.end.....]')

    def RBexecute(self):#Render
        
        print 'Houdini.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')
        self.RBnodeClean()
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        self.RBreadCfg()
        self.RBhanFile()
        if self.G_RENDEROS=='Linux':
            self.webMntPath()
        else:
            self.delSubst()
            self.webNetPath()
        #self.copyHoudiniFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.resourceMonitor()
        self.RBrender()
        if self.G_RENDEROS=='Linux':
            print 'no smallpic'
        else:
            self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')