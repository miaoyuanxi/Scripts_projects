#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
import string
import logging
import time
import shutil
import codecs
from RenderBase import RenderBase
class Clarisse(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.cgfile=configJson['common']["cgFile"]
            self.projectPath=configJson['renderSettings']["projectPath"]
            # self.cgv=configJson['common']["cgv"]
            self.cgName=configJson['common']["cgSoftName"]

            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    # self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
                    self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)
        #self.RBcmd(umountcmd)

        self.G_RENDER_LOG.info('[config....]'+self.G_CONFIG)
        self.G_CONFIG = self.G_CONFIG.replace("\\","/")
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.cgfile=configJson['common']["cgFile"]
            self.projectPath=configJson['renderSettings']["projectPath"]
            # self.cgv=configJson['common']["cgv"]
            self.cgName=configJson['common']["cgSoftName"]
            self.cgName = self.cgName.lower()
            print configJson
            if isinstance(configJson["mntMap"],dict):
                for key in configJson["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
                    self.G_RENDER_LOG.info(cmd)
                    self.RBcmd(cmd,False,1)
        
    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[Clarisse.RBrender.start.....]'+self.G_CG_OPTION)
        startTime = time.time()
        self.G_FEE_LOG.info('startTime='+str(int(startTime)))

        if self.G_RENDEROS=='Linux':
            exePath=r'/usr/isotropix/'+self.cgName+'/clarisse/cnode'
            renderpy = "/B/plugins/clarisse/lib/python/clarissefunction.py"
            cmds_py = "python"
        else:
            exePath=os.path.join(r'D:\plugins\clarisse',self.cgName,r'Clarisse\cnode.exe')
            renderpy = "B:/plugins/clarisse/lib/python/clarissefunction.py"
            cmds_py = "C:/python27/python.exe"

        if os.path.exists(exePath):
            print 'exeExist'

            frames_r = '"'+ str(self.G_CG_START_FRAME)+" "+str(self.G_CG_END_FRAME)+" "+str(1)+'"'
            render_log = "%s/%s/%s_render.log"%(self.G_LOG_WORK,self.G_TASKID,self.G_JOB_NAME)
            self.ExtInfo(render_log,'')
            func = "render"
            output = os.path.join(self.G_RENDER_WORK_OUTPUT,os.path.basename(self.G_CG_LAYER_NAME))

            cmds = "%s %s " % (cmds_py,renderpy)
            cmds += "-software %s " % exePath
            cmds += "-project %s " % self.cgfile.replace("\\","/")
            cmds += "-image %s " % self.G_CG_LAYER_NAME 
            cmds += "-frames %s " % frames_r
            cmds += "-output %s " % self.G_RENDER_WORK_OUTPUT.replace("\\","/")
            cmds += "-function %s " % func
            cmds += "-log %s " % render_log

            self.G_PROCESS_LOG.info("Render cmds: %s"%cmds)
            os.system(cmds)

        endTime = time.time()
        self.G_FEE_LOG.info('endTime='+str(int(endTime)))
        self.G_RENDER_LOG.info('[Clarisse.RBrender.end.....]')

    def clean(self):
        myCgVersion = self.cgName.replace("_"," ")
        cleanCmd='"C:/Python27/python.exe" "B:\\plugins\\clarisee\\lib\\python\\clearnlic.py" "'+myCgVersion+'"'
        #self.RBcmd(cleanCmd,True)

    def copySoft(self):
        plant = "linux" if self.G_RENDEROS=='Linux' else "win"
        py_source = "B:\\plugins\\clarisse\\lib\\python\\SetupSoftvar.py "if not self.G_RENDEROS=='Linux' else "/B/plugins/clarisse/lib/python/SetupSoftvar.py "
        cmds = "c:\\python27\\python.exe " if not self.G_RENDEROS=='Linux' else "python "
        cmds += py_source
        cmds += "soft=%s "%self.cgName
        cmds += "plant=%s"%plant
        self.G_PROCESS_LOG.info('[cmd....]'+cmds)
        self.RBcmd(cmds,False,1)
    
    def ExtInfo(self,file='',info='',towrite=True,toprint=True,types="w"):
        if info == "" and not file=='':
            infos = "Render Log start at: %s"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            infos += "\nSoftware: Clarisse"
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

    def RBcmd(self,cmdStr,continueOnErr=False,myShell=False,render=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_PROCESS_LOG.info('cmd...'+cmdStr)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                self.G_PROCESS_LOG.info(resultLine)
                if render:self.ExtInfo(self.render_log,resultLine,1,0,"a")
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.G_PROCESS_LOG.info('resultStr...'+resultStr)
        self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                self.clean()
                sys.exit(resultCode)
        return resultStr

    def RBexecute(self):#Render
        
        print 'Clarisse.execute.....'
        self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[Clarisse.RBexecute.start.....]')
        self.RBnodeClean()
        self.RBprePy()
        self.RBmakeDir()
        self.RBcopyTempFile()
        if self.G_RENDEROS=='Linux':
            self.webMntPath();
        else:
            self.delSubst()
            self.webNetPath()
        self.copySoft()
        self.RBreadCfg()
        self.RBhanFile()
        self.RBrenderConfig()
        self.RBwriteConsumeTxt()
        self.resourceMonitor()
        self.RBrender()
        self.clean()
        if not self.G_RENDEROS=='Linux':
            self.RBconvertSmallPic()
        self.RBhanResult()
        #self.RBpostPy()
        self.G_RENDER_LOG.info('[Clarisse.RBexecute.end.....]')