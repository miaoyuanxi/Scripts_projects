# ! /usr/bin/env python
# coding=utf-8
import argparse
import os
import subprocess
import _subprocess
import pprint
import sys
import shutil
import filecmp
import time
import RayvisionPluginsLoader
import re
import json



def set_plugins(self):
    if self["common"]["plugin_file"]:
        sys.stdout.flush()
        plginLd = RayvisionPluginsLoader.RayvisionPluginsLoader()
        sys.stdout.flush()
        custom_file = ""
        plginLd.RayvisionPluginsLoader(self["common"]["plugin_file"], [custom_file])
        sys.stdout.flush()


class MayaRender(MayaClass):

    def __init__(self, options):
        MayaClass.__init__(self, options)

    def RBcmd(self,cmdStr,continueOnErr=False,myShell=False,myLog=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        exitcode = 0
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                if "License error" in resultLine or "[mtoa] Failed batch render" in resultLine or "error checking out license for arnold" in resultLine or "No license for product (-1)" in resultLine:
                    exitcode = -1
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode

        if exitcode==-1:
            sys.exit(-1)

        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr        
        
        
        
        
        
def render(self):
    if os.environ.has_key('gpuid'):
        gid = int(os.environ.get('gpuid')) - 1
        d_log = r"D:/Temp/REDSHIFT/CACHE/G{}/Log/Log.Latest.0/log.html".format(gid)
        if not os.path.exists(d_log):
            os.makedirs(os.path.dirname(d_log))
            with open(d_log,"w"):
                ""            
            print "Creat empty Redshift log file: {}".format(d_log)
        if not os.path.exists(r"C:/ProgramData/Redshift/Log/Log.Latest.0/log.html"):
            os.makedirs(r"C:/ProgramData/Redshift/Log/Log.Latest.0")

            with open(r"C:/ProgramData/Redshift//Log/Log.Latest.0/log.html","w"):
                "" 
    os.system(r"B:\scripts\Maya\redshift_cmd\Erender_RS_new.bat")



