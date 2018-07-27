import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Nuke(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)
        print "Nuke INIT"
        self.G_RENDERBAT_NAME='Erender_HD.bat'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV="";
        self.CGFILE="";

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
            self.G_RENDER_LOG.info('[Nuke.clearFile.failed.....]')
            if count==-1:
                sys.exists(-1)
    
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_RENDER_LOG.info('[Nuke.RBhanFile.start.....]')

        moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
        if os.path.exists(self.G_RENDER_WORK_OUTPUT):
            self.pythonCopy(self.G_RENDER_WORK_OUTPUT.replace('\\',"/"),self.G_RENDER_WORK_OUTPUTBAK.replace('\\','/'))
        self.removeOutput(10)
        if not self.G_RENDEROS=='Linux':
            
            vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
            
            copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
            
            self.RBcmd(copyVBSCmd)
            self.G_RENDER_LOG.info('[Nuke.RBhanFile.end.....]')
        
    def RBrender(self):#7
        self.G_RENDER_LOG.info('[Nuke.RBrender.start.....]')
        startTime = time.time()
        
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        
        renderCmd =''
        self.G_RENDER_LOG.info(renderCmd)
        #os.system(renderCmd)
        self.RBcmd(renderCmd,True,1)
        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Nuke.RBrender.end.....]')
    
    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            print self.G_CONFIG
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))

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
                    self.G_RENDER_LOG.info(cmd)
                    self.RBcmd(cmd,False,1)


                    

                    
    def RBexecute(self):#Render
        
        print 'Nuke.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Nuke.RBexecute.start.....]')
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
            
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.RBrender()
        if self.G_RENDEROS=='Linux':
            print 'no smallpic'
        else:
            self.RBconvertSmallPic()
        self.RBhanResult()
        self.RBpostPy()
        self.G_RENDER_LOG.info('[Nuke.RBexecute.start.....]')