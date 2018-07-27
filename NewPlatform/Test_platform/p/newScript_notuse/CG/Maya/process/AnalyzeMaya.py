#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import os,sys,subprocess,string,logging,time,shutil
import glob
import logging
import codecs
import ConfigParser
import json
import gc
import xml.etree.ElementTree as ET
import re

from MayaPlugin import MayaPlugin
from Maya import Maya


from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from MayaUtil import RBMayaUtil as CLASS_MAYA_UTIL



    
    

class AnalyzeMaya(Maya):
    def __init__(self,**paramDict):
        Maya.__init__(self,**paramDict)
        self.format_log('AnalyzeMaya.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))
        self.format_log('done','end')
      
 


    
    def RB_CONFIG(self):
        self.G_DEBUG_LOG.info('[Maya.RBconfig.start.....]')
        print "----------------------------------------loading plugins start ------------------------------------------"
        
        #kill maya       

        print str(self.G_CG_CONFIG_DICT)
        print str(type(self.G_CG_CONFIG_DICT)) 
        
        
        # self.G_NODE_MAYAFUNCTION=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/function'))
        
        custom_file=os.path.join(self.G_NODE_MAYAFUNCTION,'MayaPluginPost.py').replace('\\','/')
        

        print custom_file
        plginLd = MayaPlugin()
        plginLd.MayaPlugin(self.G_CG_CONFIG_DICT, [custom_file])
        
        
        if self.G_CG_CONFIG_DICT:
            renderSoftware = self.G_CG_CONFIG_DICT['cg_name']
            softwareVer = self.G_CG_CONFIG_DICT['cg_version']
            plugis_list_dict = self.G_CG_CONFIG_DICT['plugins']
            print plugis_list_dict


        
        
        print "----------------------------------------loading plugins end ------------------------------------------"

        self.G_DEBUG_LOG.info('[Maya.RBconfig.end.....]')
        
        
        
            
    def RB_RENDER(self):
        self.G_DEBUG_LOG.info('[max.RBanalyse.start.....]')
        
        # renderSoftware = self.G_CG_CONFIG_DICT['cg_name']
        # softwareVer = self.G_CG_CONFIG_DICT['cg_version']
        # softvareVer_all  = renderSoftware + softwareVer
        mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/mayapy.exe')

        mayaExePath=mayaExePath.replace('\\','/')
        
        
        # self.G_NODE_MAYASCRIPT=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/script'))
        
        self.G_AN_MAYA_FILE=os.path.join(self.G_NODE_MAYASCRIPT,'Analyze.py').replace('\\','/')
            
                    

        analyze_cmd = "%s %s --ui %s --ti %s --proj %s --cgfile %s --taskjson %s" %(mayaExePath,self.G_AN_MAYA_FILE,self.G_USER_ID,self.G_TASK_ID,self.G_INPUT_PROJECT_PATH,self.G_INPUT_CG_FILE,self.G_TASK_JSON)
        # print analyze_cmd
        
        
        self.G_KAFKA_MESSAGE_BODY_DICT['startTime']=str(int(time.time()))
        self.G_DEBUG_LOG.info("\n\n-------------------------------------------Start maya program-------------------------------------\n\n")
        
        
        analyze_cmd = analyze_cmd.encode(sys.getfilesystemencoding())
        print analyze_cmd

        CLASS_COMMON_UTIL.cmd(analyze_cmd,my_log=self.G_DEBUG_LOG)
        
        
        CLASS_MAYA_UTIL.kill_lic_all(my_log=self.G_DEBUG_LOG)
        
        self.G_KAFKA_MESSAGE_BODY_DICT['endTime']=str(int(time.time()))
        
        self.G_DEBUG_LOG.info('[maya.RBanalyse.end.....]')
        
        
        
        
        
        
        
        
        
        
        
        
        
 