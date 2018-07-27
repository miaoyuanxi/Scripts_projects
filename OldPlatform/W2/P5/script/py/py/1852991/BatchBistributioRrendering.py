# -*- coding: utf-8 -*-  

#-----version3.0-------- 
import os,sys,shutil,subprocess

class ConfigDistributedFiles():
    def __init__(self):
        self.lines=[]
        configPath=os.path.split(os.path.realpath(__file__))[0] +r'\config.txt'
        for line in open(configPath): 
            self.lines.append(line.strip('\n'))
        
    def copyCfgFile(self):
        for nodeIP in self.lines:
            nodeScriptPath=r'\\'+nodeIP+r'\d$\vray_dis_test'
            print nodeScriptPath,"----nihao"
            copyNodeScriptPath='xcopy /Y /E /F "D:/vray_dis_test\*.*" "%s"' % (nodeScriptPath)
            print copyNodeScriptPath
            if not os.path.exists(nodeScriptPath):
                os.makedirs(nodeScriptPath)
                self.runcmd(copyNodeScriptPath)
            else:
                self.runcmd(copyNodeScriptPath)
                
            runPypath='D:\\munu_agent_controller.exe %s 10001 "C:\\Python27\\python.exe D:\\vray_dis_test\\vray_distribute.py "\\\\10.60.100.152\\td" "5350956" "10.60.1.106" "c:\\log""' % (nodeIP)
            self.runcmd(runPypath)
        
    def runcmd(self,cmdStr):
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        while True:
            buff=cmdp.stdout.readline()
            if buff=='' and cmdp.poll() !=None:
                break
        resultCode=cmdp.returncode

    def configAll(self):
        self.copyCfgFile()
		
configInfo=ConfigDistributedFiles()
configInfo.configAll()