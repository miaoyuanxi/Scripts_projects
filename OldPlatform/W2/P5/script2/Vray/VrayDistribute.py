#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

#vray_distributed_rendering  version1.0

import logging
import os
import sys
import subprocess
import string
import time,datetime
import shutil
import ctypes
import json
    
class DistributedRender():
    def __init__(self):
        self.PLUGIN_B_PATH=sys.argv[1]#"\\10.50.1.22\td_new\td"
        self.R_TASKID=sys.argv[2]#"5250767"
        self.R_RENDER_WORK='D:/work/render'
        self.R_RENDER_WORK_TASK=os.path.join(self.R_RENDER_WORK,self.R_TASKID)
        if not os.path.exists(self.R_RENDER_WORK_TASK):
            os.makedirs(self.R_RENDER_WORK_TASK)
        self.R_RENDER_NODE_CFG=os.path.join(self.R_RENDER_WORK_TASK,'cfg')
        if not os.path.exists(self.R_RENDER_NODE_CFG):
            os.makedirs(self.R_RENDER_NODE_CFG)
        
        self.R_MASTERIP=r'\\'+ sys.argv[3]#"10.50.7.80"
        self.R_MASTER_WORK='D$/work/render'
        self.R_MASTER_WORK_TASK=os.path.join(self.R_MASTERIP,self.R_MASTER_WORK,self.R_TASKID)
        self.R_MASTER_WORK_TASK_CFG=os.path.join(self.R_MASTERIP,self.R_MASTER_WORK,self.R_TASKID,'cfg')
        
        if os.path.exists(self.R_MASTER_WORK_TASK_CFG):
            copyCfg='robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (self.R_MASTER_WORK_TASK_CFG,self.R_RENDER_NODE_CFG)
            self.runcmd(copyCfg)
            
        # self.G_PROGRAMFILES='C:/Program Files'
        
        self.G_LOG_WORK=sys.argv[4]#"c:/log"
        if not os.path.exists(self.G_LOG_WORK):
            os.makedirs(self.G_LOG_WORK)     
        self.G_PROCESS_LOG=logging.getLogger('processlog')
        
        self.G_RENDER_JSON = os.path.join(self.R_RENDER_NODE_CFG,'render.json')
        self.G_PLUGIN_JSON = os.path.join(self.R_RENDER_NODE_CFG,'plugins.json')
        if os.path.exists(self.G_RENDER_JSON):
            self.G_RENDER_JSON_DICT=eval(open(self.G_RENDER_JSON, 'r').read())
        else:
            self.error_exit_log('%s is not exist!' % self.G_RENDER_JSON)
        if os.path.exists(self.G_PLUGIN_JSON):
            self.G_PLUGIN_JSON_DICT=eval(open(self.G_PLUGIN_JSON, 'r').read())
        else:
            self.error_exit_log('%s is not exist!' % self.G_PLUGIN_JSON)
        
        if isinstance(self.G_PLUGIN_JSON_DICT["plugins"],dict):
            for key in self.G_PLUGIN_JSON_DICT["plugins"].keys():
                self.G_PLUGIN_NAME=key
                self.G_PLUGIN_VERSION=self.G_PLUGIN_JSON_DICT["plugins"][key]
        
        self.G_RENDER_SOFTWARE = self.G_PLUGIN_JSON_DICT['renderSoftware']  #V-Ray_standalone
        self.G_VRAY_B='B:/plugins/%s' % (self.G_RENDER_SOFTWARE)  # B:\plugins\V-Ray_standalone
        
    def outPutLogger (self):
        self.G_PROCESS_LOG.info("\n\n-----------------------[VDR- set log path]-----------------------\n\n")
        processLogDir=os.path.join(self.G_LOG_WORK,self.R_TASKID)
        if not os.path.exists(processLogDir):
            os.makedirs(processLogDir)
            
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        processLogPath=os.path.join(processLogDir,"vray_distribute_log.txt")
        self.G_PROCESS_LOG.info(processLogPath)
        self.G_PROCESS_LOG.setLevel(logging.DEBUG)
        processLogHandler=logging.FileHandler(processLogPath)
        processLogHandler.setFormatter(fm)
        self.G_PROCESS_LOG.addHandler(processLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_PROCESS_LOG.addHandler(console)
        self.G_PROCESS_LOG.info("[done]")
    
    def cleanServer(self):
        self.G_PROCESS_LOG.info("\n\n-----------------------[VDR- taskkill vray]-----------------------\n\n")
        vrayExe='taskkill /im vray.exe /f'
        self.G_PROCESS_LOG.info(vrayExe)
        self.runcmd(vrayExe)
        self.G_PROCESS_LOG.info("[done]")
        
    def mapDrive(self):
        self.G_PROCESS_LOG.info("\n\n-----------------------[VDR- del net path]-----------------------\n\n")
        self.G_PROCESS_LOG.info("del subst disk")
        existSubstDisk=['e:','f:','g:','h:','i:','j:','k:','l:','m:','n:','o:','p:','q:','r:','s:','t:','u:','v:','w:','x:','y:','z:']
        for substLocalDisk in existSubstDisk:
            delsubstDisk="subst %s /D" % (substLocalDisk)
            self.runcmd(delsubstDisk)
            self.runcmd(delsubstDisk)
        delBDisk='try3 net use * /del /y'
        self.G_PROCESS_LOG.info(delBDisk)
        self.runcmd(delBDisk)
        
        #net use
        b_flag = False
        cgName=self.G_RENDER_JSON_DICT['common']["cgSoftName"]
        projectName= self.G_RENDER_JSON_DICT['common']["projectSymbol"]
        replacePath="\\"+projectName+"\\"+cgName+"\\"
        if isinstance(self.G_RENDER_JSON_DICT["mntMap"],dict):
            del_net_use = "net use * /del /y"
            self.G_PROCESS_LOG.info(del_net_use)
            self.runcmd(del_net_use)
            for key in self.G_RENDER_JSON_DICT["mntMap"]:
                newPath =self.G_RENDER_JSON_DICT["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
                net_use_cmd = "net use "+key+" \""+newPath+"\""
                self.G_PROCESS_LOG.info(net_use_cmd)
                self.runcmd(net_use_cmd)
                if key.lower() == 'b:':
                    b_flag = True
        if not b_flag:
            map_cmd_b = 'net use B: "%s"' % (os.path.normpath(self.PLUGIN_B_PATH))
            self.G_PROCESS_LOG.info(map_cmd_b)
            self.runcmd(map_cmd_b)
        
        self.G_PROCESS_LOG.info("[done]")

    def copyFilesToNode(self):
        self.G_PROCESS_LOG.info("\n\n-----------------------[VDR- copy renderFiles to node]-----------------------\n\n")
        
        #-----------------------------------------copy license-----------------------------------------------
        license_src = os.path.join(self.G_VRAY_B,'license')
        license_dest = r'C:\Program Files\Common Files\ChaosGroup'
        license_copy_cmd = 'robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (license_src,license_dest)
        self.G_PROCESS_LOG.info(license_copy_cmd)
        self.runcmd(license_copy_cmd)

        app_path = os.path.join(self.G_VRAY_B,self.G_PLUGIN_NAME,self.G_PLUGIN_VERSION)
        vray_osl_path_x64=os.path.normpath(os.path.join(app_path,'opensl'))
        vray_app = os.path.normpath(os.path.join(app_path,r'bin\x64\vc11'))
        
        #set environ
        os.environ['VRAY_AUTH_CLIENT_FILE_PATH'] = license_dest
        os.environ['VRAY_OSL_PATH_x64'] = vray_osl_path_x64
        os.environ['VRAY_PATH'] = vray_app
        os.environ['VRAY_SDK'] = app_path
        
        #start vray.exe
        vray_exe_path = os.path.normpath(os.path.join(vray_app,'vray.exe'))
        if os.path.exists(vray_exe_path):
            self.G_PROCESS_LOG.info("*******************start vraystandalone_server**********************")
            start_vraystandalone_cmd = 'start "vraystandalone_server" "%s" -server' % (vray_exe_path)
            self.G_PROCESS_LOG.info(start_vraystandalone_cmd)
            os.system(start_vraystandalone_cmd)
        else:
            self.error_exit_log('%s is not exist!' % vray_exe_path)
        
        self.G_PROCESS_LOG.info("[done]")

    def runcmd(self,cmdStr):
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        while True:
            buff=cmdp.stdout.readline()
            if buff=='' and cmdp.poll() !=None:
                break
        resultCode=cmdp.returncode
    
    def error_exit_log(self,log_str,exit_code=-1,is_exit=True):
        self.G_PROCESS_LOG.info('\r\n\r\n---------------------------------[error]---------------------------------')
        self.G_PROCESS_LOG.info(log_str)
        self.G_PROCESS_LOG.info('-------------------------------------------------------------------------\r\n')
        if is_exit:
            sys.exit(exit_code)
    
    def runAllConfig(self):
        self.outPutLogger()
        self.cleanServer()
        self.mapDrive()
        self.copyFilesToNode()

runconfig=DistributedRender()
runconfig.runAllConfig()