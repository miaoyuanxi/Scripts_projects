#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import time
import subprocess

# class FileHandle
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class RBMayaUtil(object):
    
    
    @classmethod  
    def killMayabatch(self,progressLog):
        progressLog.info('MayaLogDEBUG_TASKKILL_mayabatch')            
        try:
            os.system('taskkill /F /IM mayabatch.exe /T')
        except  Exception, e:
            progressLog.info('MayaLog2taskkill mayabatch.exe exeception')  
            progressLog.info(e)

            
      
        
       

            
    @classmethod      
    def kill_lic_all(self,my_log = None):     
        print "Rendering Completed!"

        # if not %errorlevel%==0 goto fail
        # echo "exit rlm "
        # wmic process where name="rlm.exe" delete
        # wmic process where name="JGS_mtoa_licserver.exe" delete
        # wmic process where name="rlm_redshift.exe" delete
        # wmic process where name="rlm_Golaem.exe" delete
        # wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
        # ::wmic process where ExecutablePath="C:\\Golaem\\rlm_Golaem.exe" delete
        # %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
        # %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
        # %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls

        kill_win_cmd_list = []
        pid_name_list = []
        lic_process_list = []        
        cmdow_path = "B:" + r"/tools/cmdow/cmdow.exe"
        lic_path_list = [r"C:\Golaem\rlm.exe",r"C:\Golaem\rlm_Golaem.exe",r"C:\AMPED\rlm.exe"] 
        lic_list = ["rlm.exe","JGS_mtoa_licserver.exe","rlm_redshift.exe","rlm_Golaem.exe"]

        for i in lic_path_list:
            lic_path_list_cmd = cmdow_path + " " + i
            kill_win_cmd_list.append(lic_path_list_cmd)     

        if kill_win_cmd_list:
            print kill_win_cmd_list
            for i in kill_win_cmd_list:            
                try:
                    a = os.system(i)
                    print 'Have been killed the %s,return :%s' % (i, a)
                except OSError, e:
                    print 'There is not lic windows!!!'

        else:
            print "the kill_win_cmd_list is none"


        RunningProcessList=[]
        KillList=[]

        f=os.popen('tasklist').readlines()

        for i in f:
            try:
                thisone=i.split()[0]
                if '.exe' not in thisone:
                    continue
                if thisone in RunningProcessList:
                    continue
                RunningProcessList.append(thisone)
                if thisone in lic_list:
                    KillList.append(thisone)
            except:
                pass

            
        if KillList:
            print KillList
            for name in KillList:  
                try:                              
                    a = os.system('taskkill /f /im '+name)
                    # command = 'taskkill /F /IM %s' %name
                    # a = os.system(command)
                    print 'Have been killed the %s,return :%s' % (name, a)
                except OSError, e:
                    print 'there is no process!!!'