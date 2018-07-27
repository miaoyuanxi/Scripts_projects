#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import os,sys,subprocess,string,logging,time,shutil
import glob
import logging
import codecs
import ConfigParser
import json
import xml.etree.ElementTree as ET


from AnalysisBase import AnalysisBase
from MaxPlugin import MaxPlugin



class ConflictPlugin:
    def __init__(self): 
        self.VRAY_MULTISCATTER=["2010_2.00.01_1.0.18a","2010_2.00.02_1.0.18a","2010_2.10.01_1.0.18a","2010_2.20.02_1.0.18a",
        "2010_2.40.03_1.0.18a","2010_2.00.01_1.1.05","2010_2.00.02_1.1.05","2010_2.10.01_1.1.05",
        "2010_2.20.02_1.1.05","2010_2.40.03_1.1.05","2010_2.00.01_1.1.05a","2010_2.00.02_1.1.05a",
        "2010_2.10.01_1.1.05a","2010_2.20.02_1.1.05a","2010_2.40.03_1.1.05a","2010_2.00.01_1.1.07a",
        "2010_2.00.02_1.1.07a","2010_2.10.01_1.1.07a","2010_2.20.02_1.1.07a","2010_2.40.03_1.1.07a",
        "2010_2.00.01_1.1.08b","2010_2.00.02_1.1.08b","2010_2.10.01_1.1.08b","2010_2.20.02_1.1.08b",
        "2010_2.40.03_1.1.08b","2010_2.00.01_1.1.09","2010_2.00.02_1.1.09","2010_2.10.01_1.1.09",
        "2010_2.20.02_1.1.09","2010_2.40.03_1.1.09","2010_2.00.01_1.1.09a","2010_2.00.02_1.1.09a",
        "2010_2.10.01_1.1.09a","2010_2.20.02_1.1.09a","2010_2.40.03_1.1.09a","2010_2.00.01_1.1.09c",
        "2010_2.00.02_1.1.09c","2010_2.10.01_1.1.09c","2010_2.20.02_1.1.09c","2010_2.40.03_1.1.09c",
        "2010_2.00.01_1.1.09d","2010_2.00.02_1.1.09d","2010_2.10.01_1.1.09d","2010_2.20.02_1.1.09d",
        "2010_2.40.03_1.1.09d","2010_2.00.01_1.2.0.3","2010_2.00.02_1.2.0.3","2010_2.10.01_1.2.0.3",
        "2010_2.20.02_1.2.0.3","2010_2.40.03_1.2.0.3","2010_2.00.01_1.2.0.123.0","2010_2.00.02_1.2.0.123.0",
        "2010_2.10.01_1.2.0.123.0","2010_2.20.02_1.2.0.123.0","2010_2.40.03_1.2.0.123.0","2010_2.00.01_1.3.1.3a",
        "2010_2.00.02_1.3.1.3a","2010_2.10.01_1.3.1.3a","2010_2.20.02_1.3.1.3a","2010_2.40.03_1.3.1.3a",
        "2011_2.00.01_1.0.18a","2011_2.00.02_1.0.18a","2011_2.10.01_1.0.18a","2011_2.20.02_1.0.18a",
        "2011_2.20.03_1.0.18a","2011_2.40.03_1.0.18a","2011_3.30.04_1.0.18a","2011_3.30.05_1.0.18a",
        "2011_2.00.01_1.1.05","2011_2.00.02_1.1.05","2011_2.10.01_1.1.05","2011_2.20.02_1.1.05",
        "2011_2.20.03_1.1.05","2011_2.40.03_1.1.05","2011_3.30.04_1.1.05","2011_3.30.05_1.1.05",
        "2011_2.00.01_1.1.05a","2011_2.00.02_1.1.05a","2011_2.10.01_1.1.05a","2011_2.20.02_1.1.05a",
        "2011_2.20.03_1.1.05a","2011_2.40.03_1.1.05a","2011_3.30.04_1.1.05a","2011_3.30.05_1.1.05a",
        "2011_2.00.01_1.1.07a","2011_2.00.02_1.1.07a","2011_2.10.01_1.1.07a","2011_2.20.02_1.1.07a",
        "2011_2.20.03_1.1.07a","2011_2.40.03_1.1.07a","2011_3.30.04_1.1.07a","2011_3.30.05_1.1.07a",
        "2011_2.00.01_1.1.08b","2011_2.00.02_1.1.08b","2011_2.10.01_1.1.08b","2011_2.20.02_1.1.08b",
        "2011_2.20.03_1.1.08b","2011_2.40.03_1.1.08b","2011_3.30.04_1.1.08b","2011_3.30.05_1.1.08b",
        "2011_2.00.01_1.1.09","2011_2.00.02_1.1.09","2011_2.10.01_1.1.09","2011_2.20.02_1.1.09",
        "2011_2.20.03_1.1.09","2011_2.40.03_1.1.09","2011_3.30.04_1.1.09","2011_3.30.05_1.1.09",
        "2011_2.00.01_1.1.09a","2011_2.00.02_1.1.09a","2011_2.10.01_1.1.09a","2011_2.20.02_1.1.09a",
        "2011_2.20.03_1.1.09a","2011_2.40.03_1.1.09a","2011_3.30.04_1.1.09a","2011_3.30.05_1.1.09a",
        "2011_2.00.01_1.1.09c","2011_2.00.02_1.1.09c","2011_2.10.01_1.1.09c","2011_2.20.02_1.1.09c",
        "2011_2.20.03_1.1.09c","2011_2.40.03_1.1.09c","2011_3.30.04_1.1.09c","2011_3.30.05_1.1.09c",
        "2011_2.00.01_1.1.09d","2011_2.00.02_1.1.09d","2011_2.10.01_1.1.09d","2011_2.20.02_1.1.09d",
        "2011_2.20.03_1.1.09d","2011_2.40.03_1.1.09d","2011_3.30.04_1.1.09d","2011_3.30.05_1.1.09d",
        "2011_2.00.01_1.2.0.3","2011_2.00.02_1.2.0.3","2011_2.10.01_1.2.0.3","2011_2.20.02_1.2.0.3",
        "2011_2.20.03_1.2.0.3","2011_2.40.03_1.2.0.3","2011_3.30.04_1.2.0.3","2011_3.30.05_1.2.0.3",
        "2011_2.00.01_1.2.0.123.0","2011_2.00.02_1.2.0.123.0","2011_2.10.01_1.2.0.123.0",
        "2011_2.20.02_1.2.0.123.0","2011_2.20.03_1.2.0.123.0","2011_2.40.03_1.2.0.123.0","2011_3.30.04_1.2.0.123.0",
        "2011_3.30.05_1.2.0.123.0","2011_2.00.01_1.3.1.3a","2011_2.00.02_1.3.1.3a","2011_2.10.01_1.3.1.3a","2011_2.20.02_1.3.1.3a",
        "2011_2.20.03_1.3.1.3a","2011_2.40.03_1.3.1.3a","2011_3.30.04_1.3.1.3a","2011_3.30.05_1.3.1.3a","2012_2.00.03_1.1.07a",
        "2012_2.10.01_1.1.07a","2012_2.20.02_1.1.07a","2012_2.20.03_1.1.07a","2012_2.30.01_1.1.07a","2012_2.40.03_1.1.07a",
        "2012_3.30.04_1.1.07a","2012_3.30.05_1.1.07a","2012_3.40.01_1.1.07a","2012_2.00.03_1.1.08b","2012_2.10.01_1.1.08b",
        "2012_2.20.02_1.1.08b","2012_2.20.03_1.1.08b","2012_2.30.01_1.1.08b","2012_2.40.03_1.1.08b","2012_3.30.04_1.1.08b",
        "2012_3.30.05_1.1.08b","2012_3.40.01_1.1.08b","2012_2.00.03_1.1.09","2012_2.10.01_1.1.09","2012_2.20.02_1.1.09",
        "2012_2.20.03_1.1.09","2012_2.30.01_1.1.09","2012_2.40.03_1.1.09","2012_3.30.04_1.1.09","2012_3.30.05_1.1.09",
        "2012_3.40.01_1.1.09","2012_2.00.03_1.1.09a","2012_2.10.01_1.1.09a","2012_2.20.02_1.1.09a","2012_2.20.03_1.1.09a",
        "2012_2.30.01_1.1.09a","2012_2.40.03_1.1.09a","2012_3.30.04_1.1.09a","2012_3.30.05_1.1.09a","2012_3.40.01_1.1.09a",
        "2012_2.00.03_1.1.09c","2012_2.10.01_1.1.09c","2012_2.20.02_1.1.09c","2012_2.20.03_1.1.09c","2012_2.30.01_1.1.09c",
        "2012_2.40.03_1.1.09c","2012_3.30.04_1.1.09c","2012_3.30.05_1.1.09c","2012_3.40.01_1.1.09c","2012_2.00.03_1.1.09d",
        "2012_2.10.01_1.1.09d","2012_2.20.02_1.1.09d","2012_2.20.03_1.1.09d","2012_2.30.01_1.1.09d","2012_2.40.03_1.1.09d",
        "2012_3.30.04_1.1.09d","2012_3.30.05_1.1.09d","2012_3.40.01_1.1.09d","2012_2.00.03_1.2.0.3","2012_2.10.01_1.2.0.3",
        "2012_2.20.02_1.2.0.3","2012_2.20.03_1.2.0.3","2012_2.30.01_1.2.0.3","2012_2.40.03_1.2.0.3","2012_3.30.04_1.2.0.3",
        "2012_3.30.05_1.2.0.3","2012_3.40.01_1.2.0.3","2012_2.00.03_1.2.0.123.0","2012_2.10.01_1.2.0.123.0","2012_2.20.02_1.2.0.123.0",
        "2012_2.20.03_1.2.0.123.0","2012_2.30.01_1.2.0.123.0","2012_2.40.03_1.2.0.123.0","2012_3.30.04_1.2.0.123.0","2012_3.30.05_1.2.0.123.0",
        "2012_3.40.01_1.2.0.123.0","2012_2.00.03_1.3.1.3a","2012_2.10.01_1.3.1.3a","2012_2.20.02_1.3.1.3a","2012_2.20.03_1.3.1.3a",
        "2012_2.30.01_1.3.1.3a","2012_2.40.03_1.3.1.3a","2012_3.30.04_1.3.1.3a","2012_3.30.05_1.3.1.3a","2012_3.40.01_1.3.1.3a",
        "2013_2.30.01_1.1.09c","2013_2.40.03_1.1.09c","2013_2.40.04_1.1.09c","2013_3.30.04_1.1.09c","2013_3.30.05_1.1.09c","2013_3.40.01_1.1.09c",
        "2013_2.30.01_1.1.09d","2013_2.40.03_1.1.09d","2013_2.40.04_1.1.09d","2013_3.30.04_1.1.09d","2013_3.30.05_1.1.09d","2013_3.40.01_1.1.09d",
        "2013_2.30.01_1.2.0.12","2013_2.40.03_1.2.0.12","2013_2.40.04_1.2.0.12","2013_3.30.04_1.2.0.12","2013_3.30.05_1.2.0.12",
        "2013_3.40.01_1.2.0.12","2013_2.30.01_1.2.0.3","2013_2.40.03_1.2.0.3","2013_2.40.04_1.2.0.3","2013_3.30.04_1.2.0.3",
        "2013_3.30.05_1.2.0.3","2013_3.40.01_1.2.0.3","2013_2.30.01_1.2.0.123.0","2013_2.40.03_1.2.0.123.0","2013_2.40.04_1.2.0.123.0",
        "2013_3.30.04_1.2.0.123.0","2013_3.30.05_1.2.0.123.0","2013_3.40.01_1.2.0.123.0","2013_2.30.01_1.3.1.3a","2013_2.40.03_1.3.1.3a",
        "2013_2.40.04_1.3.1.3a","2013_3.30.04_1.3.1.3a","2013_3.30.05_1.3.1.3a","2013_3.40.01_1.3.1.3a","2014_2.30.01_1.1.09c",
        "2014_2.40.03_1.1.09c","2014_2.40.04_1.1.09c","2014_3.30.04_1.1.09c","2014_3.30.05_1.1.09c","2014_3.40.01_1.1.09c",
        "2014_2.30.01_1.1.09d","2014_2.40.03_1.1.09d","2014_2.40.04_1.1.09d","2014_3.30.04_1.1.09d","2014_3.30.05_1.1.09d",
        "2014_3.40.01_1.1.09d","2014_2.30.01_1.2.0.12","2014_2.40.03_1.2.0.12","2014_2.40.04_1.2.0.12","2014_3.30.04_1.2.0.12",
        "2014_3.30.05_1.2.0.12","2014_3.40.01_1.2.0.12","2014_2.30.01_1.2.0.3","2014_2.40.03_1.2.0.3","2014_2.40.04_1.2.0.3",
        "2014_3.30.04_1.2.0.3","2014_3.30.05_1.2.0.3","2014_3.40.01_1.2.0.3","2014_2.30.01_1.2.0.123.0","2014_2.40.03_1.2.0.123.0",
        "2014_2.40.04_1.2.0.123.0","2014_3.30.04_1.2.0.123.0","2014_3.30.05_1.2.0.123.0","2014_3.40.01_1.2.0.123.0","2014_2.30.01_1.3.1.3a",
        "2014_2.40.03_1.3.1.3a","2014_2.40.04_1.3.1.3a_","2014_3.30.04_1.3.1.3a","2014_3.30.05_1.3.1.3a","2014_3.40.01_1.3.1.3a"]
        
    def maxPluginConflict(self,max='',plugin1='',plugin2=''):
        
        print '-----conflict Plugin--------'
        print max
        print plugin1
        print plugin2
        str_a=max+"_"+plugin1+"_"+plugin2
       
        if str_a  in self.VRAY_MULTISCATTER: 
            print("True!")
            return True
        else:
            print("False")
            return False

class RenderbusPath():
    def __init__(self,userPath,assetCollectAbsolutePath):
        self.G_INPUT_USER=userPath
        self.ASSET_WEB_COOLECT_BY_PATH=assetCollectAbsolutePath
    def InterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return False
            return True
        
    def parseInterPath(self,p):
        firstTwo = p[0:2]
        if firstTwo == '//' or firstTwo == '\\\\':
            normPath = p.replace('\\', '/')
            index = normPath.find('/', 2)
            if index <= 2:
                return ''
            
            return p[:index],p[index:]

    def convertPath(self,itemPath):
        if self.ASSET_WEB_COOLECT_BY_PATH:
            absPath=[['a:/','/a/'],
                ['b:/','/b/'],
                ['c:/','/c/'],
                ['d:/','/d/']]
                
            resultFile = itemPath
            lowerFile = os.path.normpath(itemPath.lower()).replace('\\', '/')
            is_abcd_path = False;
            is_InterPath = False;
            fileDir=os.path.dirname(lowerFile)
            if fileDir==None or fileDir.strip()=='':
                return os.path.normpath(resultFile)
            else:
                if self.InterPath(lowerFile):
                    start,rest = self.parseInterPath(lowerFile)
                    #resultFile= self.G_INPUT_USER + '/net' + start.replace('//', '/') + rest.replace('\\', '/') 
                    resultFile= self.G_INPUT_USER + '/__'+ start.replace('//', '')+ rest.replace('\\', '/') 
                else:
                    resultFile= self.G_INPUT_USER + '\\' + itemPath.replace('\\', '/').replace(':','')

                return os.path.normpath(resultFile)
        else:
            return itemPath
            
    def convertToUserPath(self,sourceFile):
        resultFile = sourceFile
        userInput=self.G_INPUT_USER
        userInput=userInput.replace('/','\\')
        sourceFile=sourceFile.replace('/','\\').replace(userInput,'')
        
        #if sourceFile.startswith('net'):
        if sourceFile.startswith('__'):
            resultFile = '\\\\'+sourceFile[2:]
            #resultFile=resultFile.replace('\\','/')
        elif sourceFile.startswith('a\\') or sourceFile.startswith('b\\') or sourceFile.startswith('c\\') or sourceFile.startswith('d\\'):
            resultFile = sourceFile[0]+':'+sourceFile[1:]
            resultFile=resultFile.replace('\\','/')
        else:
            resultFile=sourceFile[0]+':'+sourceFile[1:]
            resultFile=resultFile.replace('\\','/')
        
        return resultFile
        

class TipsCode():
    def __init__(self):
        #-----------code-----------
        self.MAXINFO_FAILED='15002'
        self.CONFLICT_MULTISCATTER_VRAY='15021'
        self.MAX_NOTMATCH='15013'
        self.CAMERA_DUPLICAT='15015'
        self.ELEMENT_DUPLICAT='15016'
        
        self.VRMESH_EXT_NULL="15018"
        self.PROXY_ENABLE="15010"
        self.RENDERER_NOTSUPPORT="15004"
        #-----------self.OUTPUTNAME_NULL="15007"
        self.CAMERA_NULL="15006"
        self.TASK_FOLDER_FAILED="15011"
        self.TASK_CREATE_FAILED="15012"
        self.MULTIFRAME_NOTSUPPORT="10015"#Irradiance map mode :  \"Multiframe incremental\" not supported
        self.ADDTOCMAP_NOTSUPPORT="10014"#Irradiance map mode : Add to current map not supported
        self.PPT_NOTSUPPORT="10016"#"Light cache mode : \"Progressive path tracing\" not supported "
        self.VRAY_HDRI_NOTSUPPORT="999"
        self.GAMMA_ON="10013"
        self.XREFFILES="10025"
        self.XREFOBJ="10026"
        self.VDB_MISSING="10028"
        self.REALFLOW_VERSION="15022"
        self.MISSING_FILE="10012"
        self.VRMESH_MISSING='10030'
        self.HDRI_MISSING="10012"
        self.VRMAP_MISSING="10023"
        self.VRLMAP_MISSING="10024"
        self.FUMEFX_MISSING="10011"
        self.PHOENIFX_MISSING="10022"
        self.FIRESMOKESIM_MISSING="10022"
        self.LIQUIDSIM_MISSING="10022"
        self.KK_MISSING="10019"
        self.ABC_MISSING="10018"
        self.XMESH_MISSING="10020"
        self.ANIMATION_MAP_MISSING="10027"
        self.REALFLOW_MISSING="10021"
        self.BAD_MATERIAL="10010"
        self.VRIMG_UNDEFINED="10017"#--"\"Render to V-Ray raw image file\" Checked but *.vrimg is undefined "
        self.CHANNEL_FILE_UNDEFINED="15017"#--"Save separate render channels Checked but channels file is error"
        
        
        self.DUPLICATE_TEXTURE='111'
        self.UNKNOW_ERR='999'
        self.UNKNOW_WARN='888'
        
        
        #++++++++++++++++++++++++++++++++++++++
        self.PC_MISSING='10029'
        self.GAMMA_ON='10013'
        self.TEXTURE_MISSING='10012'
        
        self.MAX_VERSION='103494'
        
        
        
class MaxResult():
    def __init__(self):
        pass
        
class Max(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "max.INIT"

        self.G_MAX_B='B:/plugins/max'
        self.G_MAXSCRIPT=self.G_MAX_B+'/script'
        self.G_MAXSCRIPT_NAME_U='analyseU.ms'#max2013,max2014,max2015
        self.G_MAXSCRIPT_NAME_A='analyseA.ms'#max2012,max2011,max2010
        
        self.G_HLEPER='C:/work/helper'
        
        configJson=eval(open(self.G_CONFIG, "r").read())
        self.G_ANALYSE_TXT_SERVER=configJson['common']["analyseTxt"]
        self.G_INPUT_USER=configJson['common']["inputUserPath"]
        self.G_BIG_TASK_ID=str(configJson['common']["taskId"])
        self.G_PROJECT_SYMBOL=str(configJson['common']["projectSymbol"])
        
        self.G_PLUGIN_PATH=configJson['mntMap']["B:"]
        
        self.G_HLEPER_TASK=os.path.join(self.G_HLEPER,self.G_BIG_TASK_ID).replace('\\','/')
        self.G_HLEPER_TASK_CFG=os.path.join(self.G_HLEPER_TASK,'cfg').replace('\\','/')
        self.G_ANALYSE_TXT_NODETEMP=os.path.join(self.G_HLEPER_TASK_CFG,'analyse_net_temp.txt').replace('\\','/')
        self.G_ANALYSE_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'analyse_net.txt').replace('\\','/')
        self.G_PROPERTY_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'property.txt').replace('\\','/')
        self.G_TIPS_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'tips.json').replace('\\','/')
        self.G_INPUT_CG_FILE=raw(configJson['common']["inputCgFile"]).decode("utf-8") 
        
        self.ASSET_INPUT_DIR=os.path.dirname(self.G_INPUT_CG_FILE)
        self.ASSET_INPUT_DIR_DICT={}
        self.ASSET_WEB_COOLECT_BY_PATH=False
        
        
        self.G_PROGRAMFILES='C:/Program Files/Autodesk'
        self.G_POOL_CONFIG = self.G_POOL + '/config/' + os.path.join(self.G_USERID_PARENT, self.G_USERID) + '/' + self.G_BIG_TASK_ID
        
        
        self.G_MAXFIND='B:/plugins/max/maxfind/GetMaxProperty.exe'
        self.G_MAXFIND_MAX_VERSION_STR=None
        self.G_MAXFIND_MAX_VERSION_INT=None
        self.G_MAXFIND_RENDERER=None
        self.G_MAXFIND_OUTPUT_GAMMA=None
        
        
        self.assetInputDict     = {}
        self.renderbusPathObj   = RenderbusPath(self.G_INPUT_USER,self.ASSET_WEB_COOLECT_BY_PATH)
        self.checkIflItems      = []
        #self.assetInputItems    = []
        self.assetiInputCount   = 1
        self.inputMissingItems  = []
        self.inputMissingCount  = 1
        
        self.TIPS_DICT={}
        self.TIPS_LIST=[]
        self.CONFLICT_PLUGIN=ConflictPlugin()
        self.TIPS_CODE=TipsCode()
        print '\r\n==================================================\r\n'
        print 'G_CONFIG=',self.G_CONFIG 
        print 'G_PLUGINS=',self.G_PLUGINS
        print 'G_USERID=',self.G_USERID 
        print 'G_USERID_PARENT=',self.G_USERID_PARENT 
        print 'G_TASKID=',self.G_TASKID 
        print 'G_BIG_TASK_ID=',self.G_BIG_TASK_ID
        print 'G_POOL=',self.G_POOL
        
        print 'G_INPUT_CG_FILE=',self.G_INPUT_CG_FILE        
        print 'G_HLEPER_TASK=',self.G_HLEPER_TASK 
        print 'G_ANALYSE_TXT_SERVER=',self.G_ANALYSE_TXT_SERVER
        print 'G_ANALYSE_TXT_NODE=',self.G_ANALYSE_TXT_NODE
        
        print '\r\n==================================================\r\n'
           

           
        #return#
        if not os.path.exists(self.G_HLEPER_TASK_CFG):
            os.makedirs(self.G_HLEPER_TASK_CFG)
        if  os.path.exists(self.G_ANALYSE_TXT_NODETEMP):
            os.remove(self.G_ANALYSE_TXT_NODETEMP)
        if  os.path.exists(self.G_ANALYSE_TXT_NODE):
            os.remove(self.G_ANALYSE_TXT_NODE)
    def RBBackupPy(self):
        print '[MAX.RBBackupPy.start.....]'

        print '[MAX.RBBackupPy.end.....]'
        
    def getSerial(self,number,numberCount):
        numberStr=str(number)
        while len(numberStr)<numberCount:
            numberStr='0'+numberStr
        return numberStr
            
    def countCharInStr(self,str,char):
        start = str.find(char)
        end = str.rfind(char)
        if start==-1 and end==-1:
            return 0
        else:
            clen=end-start+1
            return clen
        
    def convertFileCode(self,source,target,sourceCode='utf-8',targetCode='UTF-16'):
        if os.path.exists(target):
            os.remove(target)
        
        rsourceFileObj=codecs.open(source,'r')
        sourceFileResult=rsourceFileObj.read()
        sourceFileResult=sourceFileResult.decode(sourceCode)
        rsourceFileObj.close()
        
        
        renderCfgFileObj=codecs.open(target,'a',targetCode)
        renderCfgFileObj.write(sourceFileResult)
        renderCfgFileObj.close()
        
        
    def testMode(self):
        testFile=r'D:/test.txt'
        if os.path.exists(testFile):
            return
    def RBreadCfg(self):#4
        self.G_ANALYSE_LOG.info('[Max.RBreadCfg.start.....]')
        self.G_ANALYSE_LOG.info('[Max.RBreadCfg.end.....]')
        
    def RBcopyTempFile(self):
        self.G_ANALYSE_LOG.info('[MAX.RBcopyTempFile.start.....]')
        tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_analyse'))
        self.G_ANALYSE_LOG.info(tempFile)
        self.G_ANALYSE_LOG.info(self.G_HLEPER_TASK)
        #self.pythonCopy(tempFile.replace('/','\\'),self.G_HLEPER_TASK.replace('/','\\'))
        
        self.G_ANALYSE_LOG.info('[MAX.RBcopyTempFile.end.....]')	
    
    def RBhanFile(self):#3copy max file
        self.G_ANALYSE_LOG.info('[max.RBhanFile.start.....]')
        #C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "\\10.50.241.1\d\inputdata5\962500\962712\d\NONO\test_scene\0simpleTest\max2012-2014复杂贴图打包\要命要命不是人.max" /to="C:\work\helper\20628\max\"
        copyCmdStr = r'C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + os.path.join(self.G_INPUT_CG_FILE.replace('/','\\'))+'" /to="'+self.G_HLEPER_TASK.replace('/','\\')+'\\max\\"'
        print copyCmdStr
        copyCmdStr=copyCmdStr.encode(sys.getfilesystemencoding())
        self.RBcmd(copyCmdStr)
        self.G_ANALYSE_LOG.info('[max.RBhanFile.end.....]')
        
    def getMaxVersionByNumber(self,maxNumber):
        maxVersion=None
        if cmp(maxNumber,float(20))==1 or cmp(maxNumber,float(20))==0:
            maxVersion='3ds Max 2018'
        elif cmp(maxNumber,float(19))==1 or cmp(maxNumber,float(19))==0:
            maxVersion='3ds Max 2017'
        elif cmp(maxNumber,float(18))==1 or cmp(maxNumber,float(18))==0:
            maxVersion='3ds Max 2016'
        elif cmp(maxNumber,float(17))==1 or cmp(maxNumber,float(17))==0:
            maxVersion='3ds Max 2015'
        elif cmp(maxNumber,float(16))==1 or cmp(maxNumber,float(16))==0:
            maxVersion='3ds Max 2014'
        elif cmp(maxNumber,float(15))==1 or cmp(maxNumber,float(15))==0:
            maxVersion='3ds Max 2013'
        elif cmp(maxNumber,float(14))==1 or cmp(maxNumber,float(14))==0:
            maxVersion='3ds Max 2012'
        elif cmp(maxNumber,float(13))==1 or cmp(maxNumber,float(13))==0:
            maxVersion='3ds Max 2011'
        elif cmp(maxNumber,float(12))==1 or cmp(maxNumber,float(12))==0:
            maxVersion='3ds Max 2010'
        return maxVersion

    def readFile(self,file):
        codeList=['utf-8','utf-16','gbk',sys.getfilesystemencoding(),'']
        fileList=[]
        for code in codeList:
            try:
                fiileObj=codecs.open(file, 'r', 'utf-8') 
                fileList=fiileObj.readlines()
                break
            except:
                pass
        return fileList

    def maxfind(self):
        #return#
        print '----------maxfind----------'
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE)
        if  os.path.exists(self.G_PROPERTY_TXT_NODE):
            os.remove(self.G_PROPERTY_TXT_NODE)
        maxFindCmdStr=self.G_MAXFIND+r' "' +helperMaxFile.replace('\\','/')+'">>'+self.G_PROPERTY_TXT_NODE
        self.RBcmd(maxFindCmdStr.encode(sys.getfilesystemencoding()))
        
        propertyList=[]
        try:
            self.G_ANALYSE_LOG.info('--------------utf-8----------')
            propertyObj=codecs.open(self.G_PROPERTY_TXT_NODE, "r", "UTF-8")
            propertyList=propertyObj.readlines()
        except:
            try:
                self.G_ANALYSE_LOG.info('--------------sys----------')
                self.G_ANALYSE_LOG.info(sys.getfilesystemencoding())
                propertyObj=codecs.open(self.G_PROPERTY_TXT_NODE, "r", sys.getfilesystemencoding())
                propertyList=propertyObj.readlines()
            except:
                try:
                    self.G_ANALYSE_LOG.info('--------------default----------')
                    propertyObj=codecs.open(self.G_PROPERTY_TXT_NODE, "r")
                    propertyList=propertyObj.readlines()
                except:
                    pass
            
        for maxInfoLine in propertyList:
            if maxInfoLine.startswith('\t3ds Max Version:') or maxInfoLine.startswith('\t3ds max Version:') or maxInfoLine.startswith('\t3ds Max 版本:') or maxInfoLine.startswith('\t3ds Max バージョン :'):
                maxVersion=maxInfoLine.replace('\t3ds Max Version:','').replace('\t3ds max Version:','').replace('\t3ds Max 版本:','').replace('\t3ds Max バージョン :','')
                maxVersion=maxVersion.replace(',','.').replace('\r','').replace('\n','')
                maxVersionFloat=string.atof(maxVersion)
                maxVersionStr = self.getMaxVersionByNumber(maxVersionFloat)
                self.G_MAXFIND_MAX_VERSION_INT=int(maxVersionFloat)
                self.G_MAXFIND_MAX_VERSION_STR=maxVersionStr
                print '3ds max  version...',self.G_MAXFIND_MAX_VERSION_INT,'___',self.G_MAXFIND_MAX_VERSION_STR
                
            elif maxInfoLine.startswith('\tSaved As Version:') or maxInfoLine.startswith('\t另存为版本:')  or maxInfoLine.startswith('\tバージョンとして保存:'):
                maxVersion=maxInfoLine.replace('\tSaved As Version:','').replace('\t另存为版本:','').replace('\tバージョンとして保存:','')
                maxVersion=maxVersion.replace(',','.').replace('\r','').replace('\n','')
                maxVersionFloat=string.atof(maxVersion)
                maxVersionStr = self.getMaxVersionByNumber(maxVersionFloat)
                self.G_MAXFIND_MAX_VERSION_INT=int(maxVersionFloat)
                self.G_MAXFIND_MAX_VERSION_STR=maxVersionStr
                print '3ds max save as version...',self.G_MAXFIND_MAX_VERSION_INT,'___',self.G_MAXFIND_MAX_VERSION_STR
                
            elif maxInfoLine.startswith('\tRenderer Name='):
                renderer=maxInfoLine.replace('\tRenderer Name=','')
                renderer = renderer.lower().replace('v-ray ', 'vray').replace('v_ray ', 'vray').replace('adv ', '').replace('demo ', '').replace(' ', '')
                renderer = renderer.replace('\r','').replace('\n','')
                self.G_MAXFIND_RENDERER=renderer
                print '3ds max  renderer...',self.G_MAXFIND_RENDERER
                
            elif maxInfoLine.startswith('\tRender Output Gamma='):#default is 0.00
                outputGamma=maxInfoLine.replace('\tRender Output Gamma=','').replace('\r','').replace('\n','')
                self.G_MAXFIND_OUTPUT_GAMMA=outputGamma
                print '3ds max  output gamma...',self.G_MAXFIND_OUTPUT_GAMMA
        
        
        if self.G_MAXFIND_RENDERER==None or self.G_MAXFIND_MAX_VERSION_STR==None:
            tipStr='{'+str(self.TIPS_CODE.MAXINFO_FAILED)+':[]}'
            self.writeTips(tipStr)
            self.copyTipTxt()
            exit(0)
            
        if 'rt' in self.G_MAXFIND_RENDERER:
            tipStr='{'+str(self.TIPS_CODE.RENDERER_NOTSUPPORT)+':[]}'
            self.writeTips(tipStr)
            self.copyTipTxt()
            exit(0)
            
    def multiscatterAndVray(self):
    
        multiscatterStr=''
        if self.PLUGIN_DICT.has_key('plugins'):
            pluginDict=self.PLUGIN_DICT['plugins']
            if pluginDict.has_key('multiscatter'):
                multiscatterStr=pluginDict['multiscatter']
                
        if self.CONFLICT_PLUGIN.maxPluginConflict(self.G_CG_VERSION,self.G_MAXFIND_RENDERER,multiscatterStr):
            tipStr='{'+str(self.TIPS_CODE.CONFLICT_MULTISCATTER_VRAY)+':["'+self.G_CG_VERSION+'","'+self.G_MAXFIND_RENDERER+'","'+multiscatterStr+'"]}'
            self.writeTips(tipStr)
            self.copyTipTxt()
            exit(0)
        
    def configMaxPlugin(self):#config 3ds Max ,vray,plugin...and so on
        
        self.G_ANALYSE_LOG.info('[max.configMax.start.....]')
        
        self.PLUGIN_DICT={}
        print self.G_PLUGINS
        if os.path.exists(self.G_PLUGINS):
            self.PLUGIN_DICT=eval(codecs.open(self.G_PLUGINS, "r",'utf-8').read())
            if self.PLUGIN_DICT.has_key('softwareVer'):#------ config project
                self.G_CG_VERSION=self.PLUGIN_DICT['renderSoftware']+' '+self.PLUGIN_DICT['softwareVer']
                #-------------------------------max version of scene and max version of project config-------------------------------
                if self.G_CG_VERSION!=self.G_MAXFIND_MAX_VERSION_STR:
                    tipStr='"'+self.TIPS_CODE.MAX_NOTMATCH+'":[]'
                    self.TIPS_LIST.append(tipStr)
            else:#------ not config project
                self.G_CG_VERSION=self.G_MAXFIND_MAX_VERSION_STR
            
        if self.G_MAXFIND_RENDERER.startswith('vray'):
            myRenderVersion=self.G_MAXFIND_RENDERER.replace('vray','')
            if self.PLUGIN_DICT.has_key('plugins'):
                pluginDict=self.PLUGIN_DICT['plugins']
                pluginDict['vray']=myRenderVersion
            else:
                pluginDict={}
                pluginDict['vray']=myRenderVersion
                self.PLUGIN_DICT['plugins']=pluginDict

        if not self.PLUGIN_DICT.has_key('renderSoftware'):
            self.PLUGIN_DICT['renderSoftware']='3ds Max'
            
        if not self.PLUGIN_DICT.has_key('softwareVer'):
            self.PLUGIN_DICT['softwareVer']=self.G_MAXFIND_MAX_VERSION_STR.replace('3ds Max ','')
            
        print self.PLUGIN_DICT
        
           
        #-------------------------------write plugin cfg-------------------------------
        pluginCfgFile=os.path.join(self.G_HLEPER_TASK_CFG,'plugins.cfg')
        if os.path.exists(pluginCfgFile):
            os.remove(pluginCfgFile)
        pluginCfgFileObj=codecs.open(pluginCfgFile,'w','UTF-8')
        pluginCfgFileObj.write(str(self.PLUGIN_DICT))
        pluginCfgFileObj.close()
        
        #-------------------------------conflict multiscatter and vray-------------------------------
        self.multiscatterAndVray() 
        
        
        self.G_ANALYSE_LOG.info('---------------plugin--------')
        self.G_ANALYSE_LOG.info(str(self.PLUGIN_DICT))
        
        maxPlugin=MaxPlugin(self.G_ANALYSE_LOG,self.G_CG_VERSION,self.PLUGIN_DICT)
        maxPlugin.config()
        
    def RBconfig(self):#5
        #return#
        self.G_ANALYSE_LOG.info('[Max.RBconfig.start.....]')
        
        cleanMountFrom='try3 net use * /del /y'
        self.RBcmd(cleanMountFrom)
        
        
        if not os.path.exists(r'B:\plugins'):
            cmd='try3 net use B: '+self.G_PLUGIN_PATH.replace('/','\\')
            self.RBcmd(cmd)
            
        self.maxfind()
        self.configMaxPlugin()
        
        self.G_ANALYSE_LOG.info('[Max.RBconfig.end.....]')
        
    def writeMsFile(self):

        msFile=os.path.join(self.G_HLEPER_TASK_CFG,('helper.ms'))
        msFile=msFile.replace('\\','/')
        if os.path.exists(msFile):
            os.remove(msFile)
            
        msFileObject=codecs.open(msFile,'w',"utf-8")
        
        analyseTxt=self.G_ANALYSE_TXT_NODE.replace('\\','/')
        scriptMsName=self.G_MAXSCRIPT_NAME_U
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            #msFileObject=codecs.open(msFile,'w',"gbk")
            msFileObject=codecs.open(msFile,'w',sys.getfilesystemencoding())
            analyseTxt=self.G_ANALYSE_TXT_NODETEMP.replace('\\','/')
            scriptMsName=self.G_MAXSCRIPT_NAME_A
            
        userMsScript=self.G_MAXSCRIPT+'/user/'+self.G_USERID+'/'+scriptMsName
        msScript=self.G_MAXSCRIPT+'/'+scriptMsName
        if os.path.exists(userMsScript):
            msScript=userMsScript
            
        msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
        msFileObject.write('filein @"'+msScript+'"\r\n')
        
        #analyseRun "962712" "5140547" "C:/work/helper/5140547/max/要命要命不是人.max" "C:/work/helper/5140547/cfg/analyse_net.txt" 
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE) 
        mystr='analyseRun "'+self.G_USERID+'" "'+self.G_BIG_TASK_ID+'" "'+helperMaxFile.replace('\\','/')+'" "'+analyseTxt+'" "'+str(os.getpid())+'"\r\n'
        msFileObject.write(mystr)
        
        msFileObject.close()
        self.G_ANALYSE_LOG.info('[Max.writeMsFile.end.....]')
        return msFile
        
        
    def maxKill(self,parentId):
        self.G_ANALYSE_LOG.info('maxKill...start...\n')
        cmdStr='wmic process where name="3dsmax.exe" get Caption,ParentProcessId,ProcessId'
        cmdp=subprocess.Popen(cmdStr,shell = True,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while True:
            buff = cmdp.stdout.readline().strip()
            if buff == '' and cmdp.poll() != None:
                #print cmdp.poll()
                break
            #self.G_PROCESS_LOG.info(buff)
            if buff!=None and buff!='' :
                try:
                    self.G_ANALYSE_LOG.info('max process info...')
                    self.G_ANALYSE_LOG.info(buff)
                    buffArr=buff.split()
                    #print buff
                    if int(buffArr[1])==parentId:
                        #print 'kill...'+buff
                        os.system("taskkill /f /pid %s" % (buffArr[2]))
                except:
                    pass
        self.G_ANALYSE_LOG.info('maxKill...end...\n')
        
    def RBrenderCmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        self.G_ANALYSE_LOG.info(cmdStr)
        self.G_ANALYSE_LOG.info("\n\n-------------------------------------------Start max program-------------------------------------\n\n")
        
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        #cmdp.stdin.write('3/n')
        #cmdp.stdin.write('4/n')
        while True:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine == '' and cmdp.poll()!=None:
                break
                
            self.G_ANALYSE_LOG.info(resultLine)
            
            if '[End maxscript analyse]' in resultLine:
                self.maxKill(cmdp.pid)
                self.G_ANALYSE_LOG.info("\n\n-------------------------------------------End max program-------------------------------------\n\n")
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.G_ANALYSE_LOG.info('resultStr...'+resultStr)
        self.G_ANALYSE_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                sys.exit(resultCode)
        return resultStr
        
                    
    def RBanalyse(self):#7
        #return#
        self.G_ANALYSE_LOG.info('[max.RBanalyse.start.....]')
        
        
       #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms";analyseRun \"962712\" \"20628\" \"C:\work\helper\20628\max\要命要命不是人.max\" \"C:\work\helper\20628\cfg\analyse_net.txt\" "
        maxExe = self.G_PROGRAMFILES+'/'+self.G_CG_VERSION+'/3dsmax.exe'
        
        #helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE) 
        #analyseCmd = maxExe + '" -silent -ma -mxs "filein \\"'+msScript +'\\";analyseRun \\"' + self.G_USERID +'\\" \\"' + self.G_BIG_TASK_ID + '\\" \\"' + helperMaxFile.replace('\\','/') + '\\" \\"' + self.G_ANALYSE_TXT_NODE.replace('\\','/') + '\\" "'
        msFile=self.writeMsFile()
        
        pluginDict=self.PLUGIN_DICT['plugins']
        standVrayList=[]
        standVrayList.append('3ds Max 2016_vray3.30.05')
        standVrayList.append('3ds Max 2015_vray3.30.05')
        standVrayList.append('3ds Max 2014_vray3.30.05')
        standVrayList.append('3ds Max 2016_vray3.40.01')
        standVrayList.append('3ds Max 2015_vray3.40.01')
        standVrayList.append('3ds Max 2014_vray3.40.01')
        
        renderer=''
        if pluginDict.has_key('vray'):
            renderer='vray'+pluginDict['vray']
        standVrayStr=self.G_CG_VERSION+'_'+renderer
        
        self.G_ANALYSE_LOG.info('\r\n\r\n==========================')
        self.G_ANALYSE_LOG.info(standVrayStr)
        
        
        analyseCmd = '"'+maxExe +'" -silent  -U MAXScript "'+msFile+'"'
        if standVrayStr in standVrayList:
            analyseCmd = '"'+maxExe +'"   -U MAXScript "'+msFile+'"'
        analyseCmd = analyseCmd.encode(sys.getfilesystemencoding())
        self.RBrenderCmd(analyseCmd,True,True)
        self.G_ANALYSE_LOG.info('[max.RBanalyse.end.....]')
        
        
    def listToStr(self,list):
        str='['
        for item in list:
            str=str+'"'+item+'",'
        str=str.strip(',')
        str=str+']'
        return str
        
    def writeTipsList(self):
        tipStr='{\r\n'
        for item in  self.TIPS_LIST :
            tipStr=tipStr+item+',\r\n'
        tipStr=tipStr.strip(',\r\n')
        tipStr=tipStr+'\r\n}'
        self.writeTips(tipStr)
        
    def writeTips(self,tipStr):
        fl=codecs.open(self.G_TIPS_TXT_NODE, 'w', "UTF-8")
        
        fl.write(tipStr)
        fl.close()
        
    def getMissingCodeInfo(self,infoCode,infoType):
    
        if self.ANALYSE_TXT_PARSER.has_section(infoType):
            itemKeyList = self.ANALYSE_TXT_PARSER.options(infoType)
                 
            if len(itemKeyList)>0:
                resultStr='"'+infoCode+'":[\r\n'
                for index,itemKey in enumerate(itemKeyList):
                    #for itemKey in itemKeyList:
                    itemVal = self.ANALYSE_TXT_PARSER.get(infoType, itemKey)
                    if itemVal==None or itemVal=='':
                        continue
                    itemVal = itemVal.strip()
                    if self.ASSET_WEB_COOLECT_BY_PATH:
                        itemVal=self.renderbusPathObj.convertToUserPath(itemVal)
                    
                    #itemVal=self.renderbusPathObj.convertToUserPath(itemVal)
                    if index==len(itemKeyList)-1:
                        resultStr=resultStr+'\"'+itemVal+'\"\r\n'
                    else:
                        resultStr=resultStr+'\"'+itemVal+'\",\r\n'
                resultStr=resultStr+']'
                self.TIPS_LIST.append(resultStr)
            
                
    def hanTips(self):
        #------------ms tips-----------
        if self.ANALYSE_TXT_PARSER.has_section('tips'):
            dataDict={}
            itemKeyList = self.ANALYSE_TXT_PARSER.options('tips')
            for index,itemKey in enumerate(itemKeyList):
            #for itemKey in itemKeyList:
                itemVal = self.ANALYSE_TXT_PARSER.get('tips', itemKey)
                if itemVal==None or itemVal=='':
                    continue
                itemVal = itemVal.strip()
                self.TIPS_LIST.append(itemKey+':'+itemVal)

        #------------gamma-----------
        if self.ANALYSE_TXT_PARSER.has_option('common','filegamma'):
            gamma= self.ANALYSE_TXT_PARSER.get('common', 'filegamma')
            if gamma!=None and gamma.strip()=='gamma':
                gammaTip='"'+self.TIPS_CODE.GAMMA_ON+'":[]'
                self.TIPS_LIST.append(gammaTip)
        
        #------------global proxy-----------
        if self.ANALYSE_TXT_PARSER.has_option('common','globalproxy'):
            globalproxy= self.ANALYSE_TXT_PARSER.get('common', 'globalproxy')
            if globalproxy!=None and globalproxy.strip()=='true':
                globalproxyTip='"'+self.TIPS_CODE.PROXY_ENABLE+'":[]'
                self.TIPS_LIST.append(globalproxyTip)
                
        #------------check duplicate camera-----------  
        if self.ANALYSE_TXT_PARSER.has_option('common', 'allcamera'):        
            cameraList = self.ANALYSE_TXT_PARSER.get('common', 'allcamera').strip('[,]').split('[,]') 
            if self.isDuplicateList(cameraList):
                dupCameraTips='"'+self.TIPS_CODE.CAMERA_DUPLICAT+'":'+self.listToStr(cameraList)
                self.TIPS_LIST.append(dupCameraTips)
            
        #------------check duplicate elements-----------   
        if self.ANALYSE_TXT_PARSER.has_option('common', 'renderelement'):
            elemList = self.ANALYSE_TXT_PARSER.get('common', 'renderelement').strip('[,]').split('[,]') 
            if self.isDuplicateList(elemList):
                dupElemTips='"'+self.TIPS_CODE.ELEMENT_DUPLICAT+'":'+self.listToStr(elemList)
                self.TIPS_LIST.append(dupElemTips)
            
        #------------vrmesh with null type-----------
        if self.ANALYSE_TXT_PARSER.has_section('vrmesh'):
            badVrmeshList=[]
            itemKeyList = self.ANALYSE_TXT_PARSER.options('vrmesh')
            for index,itemKey in enumerate(itemKeyList):
                itemVal = self.ANALYSE_TXT_PARSER.get('vrmesh', itemKey)
                if itemVal==None or itemVal=='':
                    continue
                itemVal = itemVal.strip()
                if os.path.splitext(itemVal)[1] ==None or  os.path.splitext(itemVal)[1] =='' :
                    badVrmeshList.append(itemVal)
            if len(badVrmeshList)>0:
                badVrmeshTips='"'+self.TIPS_CODE.VRMESH_EXT_NULL+'":'+self.listToStr(badVrmeshList)
                self.TIPS_LIST.append(badVrmeshTips)
                
        #------------Missing camera-----------   
        if self.ANALYSE_TXT_PARSER.has_option('common', 'allcamera'):
            if self.ANALYSE_TXT_PARSER.get('common', 'allcamera')==None or self.ANALYSE_TXT_PARSER.get('common', 'allcamera')=='':
                missingCameraTips='"'+self.TIPS_CODE.CAMERA_NULL+'":[]'
                self.TIPS_LIST.append(missingCameraTips)
        else:
            missingCameraTips='"'+self.TIPS_CODE.CAMERA_NULL+'":[]'
            self.TIPS_LIST.append(missingCameraTips)
            
            
        #------------xref files-----------   
        if self.ANALYSE_TXT_PARSER.has_option('common', 'xrefs'):
            if self.ANALYSE_TXT_PARSER.get('common', 'xrefs')==None or self.ANALYSE_TXT_PARSER.get('common', 'xrefs')=='':
                missingCameraTips='"'+self.TIPS_CODE.CAMERA_NULL+'":[]'
                self.TIPS_LIST.append(missingCameraTips)
               
               
        #-----------VFB : \"Render to V-Ray raw image file\" Checked but *.vrimg is undefined " ------------ 
        if self.ANALYSE_TXT_PARSER.has_option('vray', 'vfb') and self.ANALYSE_TXT_PARSER.get('vray', 'vfb') =='true':
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'rendrawimgname') and self.ANALYSE_TXT_PARSER.get('vray', 'rendrawimgname') =='true':
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'rawimgname') and self.ANALYSE_TXT_PARSER.get('vray', 'rawimgname') =='':
                    vfbTips='"'+self.TIPS_CODE.VRIMG_UNDEFINED+'":[]'
                    self.TIPS_LIST.append(vfbTips)
        
        
        #-----------\"Save separate render channels Checked but channels file is error"------------ 
        if self.ANALYSE_TXT_PARSER.has_option('vray', 'savesepchannel') and self.ANALYSE_TXT_PARSER.get('vray', 'savesepchannel') =='true':
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'channelfile') and self.ANALYSE_TXT_PARSER.get('vray', 'channelfile') =='':
                SRCTips='"'+self.TIPS_CODE.CHANNEL_FILE_UNDEFINED+'":[]'
                self.TIPS_LIST.append(SRCTips)
                
                    
        #--------------------check gi------------------- 
        if self.ANALYSE_TXT_PARSER.has_option('vray', 'gi') and self.ANALYSE_TXT_PARSER.get('vray', 'gi')=='true' :
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'primarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'primarygiengine') =='0':
                #-----------Irradiance map mode :  \"Multiframe incremental\" not supported------------
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'irradiancemapmode') and self.ANALYSE_TXT_PARSER.get('vray', 'irradiancemapmode') =='1':
                    multiframeTips='"'+self.TIPS_CODE.MULTIFRAME_NOTSUPPORT+'":[]'
                    self.TIPS_LIST.append(multiframeTips)
                    
                #-----------Irradiance map mode : Add to current map not supported------------
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'irradiancemapmode') and self.ANALYSE_TXT_PARSER.get('vray', 'irradiancemapmode') =='3':
                    addtocmapTips='"'+self.TIPS_CODE.ADDTOCMAP_NOTSUPPORT+'":[]'
                    self.TIPS_LIST.append(addtocmapTips)
            
            #-----------Light cache mode : \"Progressive path tracing\" not supported------------        
            elif self.ANALYSE_TXT_PARSER.has_option('vray', 'primarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'primarygiengine') =='3':
                 if self.ANALYSE_TXT_PARSER.has_option('vray', 'lightcachemode') and self.ANALYSE_TXT_PARSER.get('vray', 'lightcachemode') =='3':
                    pptTips='"'+self.TIPS_CODE.PPT_NOTSUPPORT+'":[]'
                    self.TIPS_LIST.append(pptTips)
                    
            #-----------Light cache mode : \"Progressive path tracing\" not supported------------ 
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'secondarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'secondarygiengine') =='3':
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'lightcachemode') and self.ANALYSE_TXT_PARSER.get('vray', 'lightcachemode') =='3':
                    pptTips='"'+self.TIPS_CODE.PPT_NOTSUPPORT+'":[]'
                    self.TIPS_LIST.append(pptTips)
                    
            #-----------Irradiance map mode : \"From file\" VRMAP_MISSING------------ 
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'primarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'primarygiengine') =='0':
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'irradiancemapmode') and self.ANALYSE_TXT_PARSER.get('vray', 'irradiancemapmode') =='2':
                    if self.ANALYSE_TXT_PARSER.has_option('vray', 'irrmapfile') and self.ANALYSE_TXT_PARSER.get('vray', 'irrmapfile') =='':
                        VRMissTips='"'+self.TIPS_CODE.VRMAP_MISSING+'":[]'
                        self.TIPS_LIST.append(VRMissTips)
            
            #-----------Irradiance map mode : \"Animation rendering\" ANIMATION_MAP_MISSING------------ 
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'primarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'primarygiengine') =='0':
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'irradiancemapmode') and self.ANALYSE_TXT_PARSER.get('vray', 'irradiancemapmode') =='7':
                    if self.ANALYSE_TXT_PARSER.has_option('vray', 'irrmapfile') and self.ANALYSE_TXT_PARSER.get('vray', 'irrmapfile') =='':
                        if self.ANALYSE_TXT_PARSER.has_option('vray', 'irrmapfile') and self.ANALYSE_TXT_PARSER.get('vray', 'irrmapfile') =='':
                            AMMissTips='"'+self.TIPS_CODE.ANIMATION_MAP_MISSING+'":[]'
                            self.TIPS_LIST.append(AMMissTips)
            
            #-----------light cache mode : \"From file\" VRLMAP_MISSING------------ 
            if self.ANALYSE_TXT_PARSER.has_option('vray', 'secondarygiengine') and self.ANALYSE_TXT_PARSER.get('vray', 'secondarygiengine') =='3':
                if self.ANALYSE_TXT_PARSER.has_option('vray', 'lightcachemode') and self.ANALYSE_TXT_PARSER.get('vray', 'lightcachemode') =='2':
                    if self.ANALYSE_TXT_PARSER.has_option('vray', 'lightcachefile') and self.ANALYSE_TXT_PARSER.get('vray', 'lightcachefile') =='':
                        VRLMissTips='"'+self.TIPS_CODE.VRLMAP_MISSING+'":[]'
                        self.TIPS_LIST.append(VRLMissTips)
                        
            
                    
       
       
       
        self.VRMAP_MISSING="10023"
        self.VRLMAP_MISSING="10024"
        self.ANIMATION_MAP_MISSING="10027"
        self.VRIMG_UNDEFINED="10017"#--"\"Render to V-Ray raw image file\" Checked but *.vrimg is undefined "
        self.CHANNEL_FILE_UNDEFINED="15017"#--"Save separate render channels Checked but channels file is error"
        
        
        
        
        #------------missing-----------
        self.getMissingCodeInfo(self.TIPS_CODE.PC_MISSING,'pointcache_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.MISSING_FILE,'texture_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.XREFFILES,'xrefs')
        self.getMissingCodeInfo(self.TIPS_CODE.XREFOBJ,'xrefsobj')
        self.getMissingCodeInfo(self.TIPS_CODE.VDB_MISSING,'vdb_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.HDRI_MISSING,'hdri_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.FUMEFX_MISSING,'fumefx_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.PHOENIFX_MISSING,'phoenix_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.VRMESH_MISSING,'vrmesh_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.FIRESMOKESIM_MISSING,'firesmokesim_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.LIQUIDSIM_MISSING,'liquidsim_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.KK_MISSING,'kk_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.ABC_MISSING,'alembic_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.XMESH_MISSING,'xmesh_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.REALFLOW_MISSING,'realflow_missing')
        self.getMissingCodeInfo(self.TIPS_CODE.BAD_MATERIAL,'badmaterial')
        
            
        #------------write tips-----------    
        self.writeTipsList()
        

    def parseAnalyseTxt(self):
        
        self.ANALYSE_TXT_PARSER = ConfigParser.ConfigParser()
        try:
            self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r", "UTF-16"))
        except Exception, e:
            try:
                self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r", "UTF-8"))
            except Exception, e:
                self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r"))
        self.FRAMES=self.ANALYSE_TXT_PARSER.get('common', 'frames')
        self.ANIMATION_RANGE=self.ANALYSE_TXT_PARSER.get('common', 'animationRange') 
        
    def getItemFromSection(self, section):
        itemList = []
        if self.ANALYSE_TXT_PARSER.has_section(section):
            itemKeyList = self.ANALYSE_TXT_PARSER.options(section)
            print itemKeyList
            for itemKey in itemKeyList:
                # print itemKey
                itemPath = self.ANALYSE_TXT_PARSER.get(section, itemKey).strip()
                # print itemPath
                #if ignore:
                #    rbFile = itemPath 
                #else:
                #    rbFile = self.renderbusPathObj.convertPath(itemPath)

                #print rbFile
                #itemList.append(rbFile)
                itemList.append(itemPath)
            
        return itemList
    
    #true=duplicate,false=not duplicate
    def isDuplicateList(self, list):
        listSet = set(list)
        if len(list)==len(listSet):
            return False
        else:
            return True
            
    def getFileFromInputByName(self,file):
        fileFromInput=None
        assetInputList= self.ASSET_INPUT_DIR_DICT.keys()
        fileBaseName=os.path.basename(file)
        if fileBaseName in assetInputList:
            fileFromInput=self.ASSET_INPUT_DIR_DICT[fileBaseName]
        return fileFromInput
        
    def getPointCacheList(self,assetFile,resultList):
        wildPath=assetFile
        if self.ASSET_WEB_COOLECT_BY_PATH:
            wildPath = self.renderbusPathObj.convertPath(assetFile)
            resultList.append(wildPath)
        else:
            resultList.append(wildPath)
            wildPath=self.getFileFromInputByName(assetFile)
            
        if wildPath.endswith('.xml') and os.path.exists(wildPath):
            
            root = ET.parse(wildPath).getroot()
            
            cacheType           = root.find('cacheType').get('Type')    # OneFile | OneFilePerFrame
            format              = root.find('cacheType').get('Format')  # mcc | mcx
            time                = root.find('time').get('Range')
            cacheTimePerFrame   = root.find('cacheTimePerFrame').get('TimePerFrame')
            
            suffix      = '.mc' if format == 'mcc' else '.mcx'
            cacheStart = int(time.split('-')[0]) / int(cacheTimePerFrame)
            cacheEnd  = int(time.split('-')[1]) / int(cacheTimePerFrame)
            
            if cacheType == 'OneFilePerFrame':                        
                for i in range(cacheStart, cacheEnd + 1):
                    cacheFile = os.path.splitext(wildPath)[0] + 'Frame' + str(i) + suffix

                    resultList.append(cacheFile) 
                    
            elif cacheType == 'OneFile':
                cacheFile = wildPath.replace('.xml', suffix)
                resultList.append(cacheFile)
        

                        
    
        
    def getIflList(self,iflFile,resultList):
        
        reallyIflFile=iflFile
        if self.ASSET_WEB_COOLECT_BY_PATH:
            reallyIflFile=self.renderbusPathObj.convertPath(iflFile)
            resultList.append(reallyIflFile)
        else:
            resultList.append(iflFile)
            reallyIflFile=self.getFileFromInputByName(iflFile)
        
        
        if reallyIflFile!=None and os.path.exists(reallyIflFile): 
            #print '[exists]'
            reallyIflFileDir=os.path.dirname(reallyIflFile)
            iflFileList=self.readFile(reallyIflFile)
            assetList = []
            for line in iflFileList:
                
                # remove bom tag 
                if line==None or line.strip('')=='':
                    continue
                if bytes(line)[:3] == codecs.BOM_UTF8:
                    line = bytes(line)[3:]
                #print line.decode('utf-8').strip()
                line=line.strip()
                pos =line.rfind(' ')
                img = line
                if pos!=-1:
                    number=line[pos:].strip()
                    #print 'number...',number
                    if number.isalnum():#mm.jpg 5
                        img = line[:pos]
                #print img.decode('utf-8').strip()
                imgDir=os.path.dirname(img)
                if imgDir==None or imgDir.strip()=='':
                    img = os.path.join(reallyIflFileDir,img)
                else:
                    img = self.renderbusPathObj.convertPath(img.decode('utf-8').strip())
                
                
                resultList.append(img)
                

    def gatherAssetByFilePath(self,assetType,assetList):
        self.G_ANALYSE_LOG.info('\r\n\r\n[-----------------max.RBanalyse.gatherAssetByFilePath]')
        self.G_ANALYSE_LOG.info(assetType)
        missingCount = 1
        for asset in assetList:
            
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            
            #self.assetInputItems.append(asset)
            self.assetiInputCount = self.assetiInputCount + 1 
            
            if not os.path.exists(asset):
                self.ANALYSE_TXT_PARSER.set('asset_input_missing', ('path' + str(self.inputMissingCount)), asset)      
                self.inputMissingItems.append(asset)
                self.inputMissingCount = self.inputMissingCount + 1 
                
                self.ANALYSE_TXT_PARSER.set(assetType + '_missing', ('path' + str(missingCount)), asset)      
                missingCount = missingCount + 1 
            #self.checkIfl(assetType, asset)
            
    def gatherAssetByFileName(self,assetType,assetList):
        self.G_ANALYSE_LOG.info('\r\n\r\n[-----------------max.RBanalyse.gatherAssetByFileName]')
        self.G_ANALYSE_LOG.info(assetType)
        missingCount = 1
        
        for asset in assetList:
            
            self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            self.assetiInputCount = self.assetiInputCount + 1 
            
            assetName=os.path.basename(asset)
            assetInputList= self.ASSET_INPUT_DIR_DICT.keys()
            if  assetName  in assetInputList:
                self.G_ANALYSE_LOG.info(self.ASSET_INPUT_DIR_DICT[assetName])
            
            else:
                self.ANALYSE_TXT_PARSER.set('asset_input_missing', ('path' + str(self.inputMissingCount)), asset)      
                self.inputMissingItems.append(asset)
                self.inputMissingCount = self.inputMissingCount + 1 
                
                self.ANALYSE_TXT_PARSER.set(assetType + '_missing', ('path' + str(missingCount)), asset)      
                missingCount = missingCount + 1 
            #self.checkIfl(assetType, asset)
                
                
                
    #-----------------get input asset and missing asset--------------------
    def gatherAsset(self, assetType, assetList):
        if self.ASSET_WEB_COOLECT_BY_PATH:
            self.gatherAssetByFilePath(assetType,assetList)
        else:
            self.gatherAssetByFileName(assetType,assetList)
        
    #-----------------get all asset list(found and missing)--------------------
    def handleAsset(self, dict):
        assetsDict = dict
        def handler(key):
            resultDict = {}
            resultList = []
            assetList = assetsDict[key]
            
            # handle fumefx & realflow & pc2 & pointcache & vrmesh
            if key == 'fumefx':
                for asset in assetList:
                    splitedArray = asset.split('|')
                    startFrame  = splitedArray[0]
                    endFrame    = splitedArray[1]
                    type        = splitedArray[2] # default | wavlet | post
                    wildPath    = splitedArray[3]
                    pos         = wildPath.rfind('.fxd')

                    # build sequence number
                    start = int(startFrame);
                    end   = int(endFrame);
                    file = ''
                    for i in range(start , end+1, -1 if start > end else 1):
                        
                        if i >= 0:
                            file = wildPath[:pos] + '%04d' % i + '.fxd'
                        else:
                            file = wildPath[:pos] + str(i) + '.fxd'
                        
                        resultList.append(self.renderbusPathObj.convertPath(file)) 
            elif key == 'xmesh':
                print '-----------------------xmesh--------------------------'
                for asset in assetList:
                    print asset
                    splitedArray = asset.split('|')
                    startFrame  = splitedArray[0]
                    endFrame    = splitedArray[1]
                    limit        = splitedArray[2] # PHXSimulator | FireSmokeSim | LiquidSim
                    renderSequence    =splitedArray[3]
                    proxySequence    = splitedArray[4]
                    
                    start = int(startFrame)
                    end   = int(endFrame)
                    
                    if limit!='true':
                        frameArr=self.ANIMATION_RANGE.split('-')
                        if len(frameArr)==1:
                            start=end=int(frameArr[0])
                        elif len(frameArr)==2:
                            start=int(frameArr[0])
                            end=int(frameArr[1])
                            
                    for i in range(start , end+1, -1 if start > end else 1):
                        if renderSequence!=None and renderSequence!='':
                            file = renderSequence[:-10] + '%04d' % i + '.xmesh'
                            resultList.append(self.renderbusPathObj.convertPath(file))
                        if proxySequence!=None and proxySequence!='':
                            file = proxySequence[:-10] + '%04d' % i + '.xmesh'
                            resultList.append(self.renderbusPathObj.convertPath(file))
                    if renderSequence!=None and renderSequence!='':
                        renderSequenceFolder=os.path.dirname(self.renderbusPathObj.convertPath(renderSequence))
                        if os.path.exists(renderSequenceFolder):
                            renderSequenceList=os.listdir(renderSequenceFolder)
                            for rSeq in renderSequenceList:
                                if rSeq.endswith('.xmdat'):
                                    resultList.append(os.path.join(renderSequenceFolder,rSeq))
                    if proxySequence!=None and proxySequence!='':
                        proxySequenceFolder=os.path.dirname(self.renderbusPathObj.convertPath(proxySequence))
                        if os.path.exists(proxySequenceFolder):
                            proxySequenceList=os.listdir(proxySequenceFolder)
                            for pSeq in proxySequenceList:
                                if pSeq.endswith('.xmdat'):
                                    resultList.append(os.path.join(proxySequenceFolder,pSeq))
            elif key == 'phoenix':
                print '-----------------------phoenix--------------------------'
                
                for asset in assetList:
                    splitedArray = asset.split('|')
                    startFrame  = splitedArray[0]
                    endFrame    = splitedArray[1]
                    type        = splitedArray[2] # PHXSimulator | FireSmokeSim | LiquidSim
                    nodeName    =splitedArray[3]
                    inputFile    = splitedArray[4]
                    outputFile    = splitedArray[5]
                    start = int(startFrame);
                    end   = int(endFrame);
                    if start==0 and end==0:
                        frameArr=self.ANIMATION_RANGE.split('-')
                        if len(frameArr)==1:
                            start=end=int(frameArr[0])
                        elif len(frameArr)==2:
                            start=int(frameArr[0])
                            end=int(frameArr[1])
                        
                    if inputFile.startswith('$'):
                        inputFile=outputFile
                    if inputFile.startswith('$'):
                        resultList.append(nodeName) 
                        continue
                        
                    file = ''
                    #pos=inputFile.rfind('####.aur')
                    inputFile=inputFile.strip('.aur')
                    inputFileBaseName=os.path.basename(inputFile)
                    charCount=self.countCharInStr(inputFileBaseName,'#')
                    inputFile=inputFile.strip('#').strip('_')
                    
                    if type=='firesmokesim':
                        for i in range(start , end+1, -1 if start > end else 1):
                            if i >= 0 :
                                
                                file = inputFile +'_'+ self.getSerial(i,charCount) + '.aur'
                            else:
                                file = inputFile+'_' + str(i) + '.aur'
                            resultList.append(self.renderbusPathObj.convertPath(file)) 
                    else:
                        for i in range(start , end+1, -1 if start > end else 1):
                        
                            if i >= 0 :
                                file = inputFile  +'_'+ self.getSerial(i,charCount)  + '.aur'
                            else:
                                file = inputFile  +'_'+ str(i) + '.aur'
                            resultList.append(self.renderbusPathObj.convertPath(file)) 
            
            elif key == 'realflow':
               for asset in assetList:
                   splitedArray = asset.split('|')
                   startFrame  = splitedArray[0]
                   endFrame    = splitedArray[1]
                   paddingSize = splitedArray[2] 
                   format      = splitedArray[3]
                   baseDir     = splitedArray[4]
                   prefix      = splitedArray[5]
                   # build sequence number
                   start = int(startFrame);
                   end   = int(endFrame);
                   file = ''
                   for i in range(start , end+1, -1 if start > end else 1):
                       
                       if i >= 0:
                           seq = '%%%02dd' % int(paddingSize) % i
                       else:
                           seq = i;
                           
                       fileName =  format.replace('#', seq).replace('name', prefix).replace('ext', 'bin')  
                       file = os.path.join(baseDir, fileName)                          
                       resultList.append(self.renderbusPathObj.convertPath(file))            
                        
            elif key == 'vrmesh':
                 for asset in assetList:
                    wildPath = asset
                    if wildPath.endswith('.vrmesh'):
                        filePath = self.renderbusPathObj.convertPath(wildPath)
                        resultList.append(filePath) 
                    else:
                        print '#########################################################'
                        #self.G_ANALYSE_LOG.error('[Max vrmesh invalid: %s]' % wildPath)

            elif key == 'pointcache':
                for asset in assetList:
                    self.getPointCacheList(asset,resultList)
                    
                
            else:
                for asset in assetList:
                    if asset.endswith('.ifl'):
                        print 'resultIFL.....', asset
                        self.getIflList(asset,resultList)
                    else:
                        resultList.append(self.renderbusPathObj.convertPath(asset))
                    
            
                #resultList = map(self.renderbusPathObj.convertPath, assetList)    
               
            
            resultDict[key] = resultList
            return resultDict
            
        return handler
        
    def checkDuplicateFile(self,list):
        resultDict={}
        
        
        for item1 in list:
            if item1==None or item1.strip()=='':
                continue
            itemName1=os.path.basename(item1)
            dupList=[]
            for item2 in list:
                if item2==None or item2.strip()=='':
                    continue
                itemName2=os.path.basename(item2)
                if itemName1==itemName2:
                    dupList.append(item2)
            if len(dupList)>1:
                resultDict[itemName1]=dupList
                
        return resultDict
                    
            
        
    def getAllAsset(self):
        assetsDict = {}

        assetsDict['texture']    = self.getItemFromSection('texture')
        assetsDict['vrmesh']     = self.getItemFromSection('vrmesh')
        assetsDict['alembic']    = self.getItemFromSection('alembic')
        assetsDict['fumefx']     = self.getItemFromSection('fumefx')
        assetsDict['phoenix']     = self.getItemFromSection('phoenix')
        assetsDict['xmesh']     = self.getItemFromSection('xmesh')
        assetsDict['pc2']        = self.getItemFromSection('pc2')
        assetsDict['pointcache'] = self.getItemFromSection('pointcache')
        assetsDict['realflow']   = self.getItemFromSection('realflow')
        assetsDict['ies']        = self.getItemFromSection('ies')
        assetsDict['xrefs']      = self.getItemFromSection('xrefs')
        assetsDict['error']      = self.getItemFromSection('error')
    
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input')
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input_missing'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input_missing')
        
        # all assets
        dictList = map(self.handleAsset(assetsDict), assetsDict)
        for dict in dictList:
            for assetType, assetList in dict.items():
                if not self.ANALYSE_TXT_PARSER.has_section(assetType + '_missing'):
                    self.ANALYSE_TXT_PARSER.add_section(assetType + '_missing')
                
                self.gatherAsset(assetType, assetList)

        self.ANALYSE_TXT_PARSER.write(codecs.open(self.G_ANALYSE_TXT_NODE, "w", "UTF-16"))
        

        #------------------------------------check duplicate texture--------------------------------------
        dupTextureDict=self.checkDuplicateFile(assetsDict['texture'])
        if len(dupTextureDict)>0 :
            dupTextureList=dupTextureDict.values()
            dupStr=''
            totalDupList=[]
            for dupList in dupTextureList:
                totalDupList.extend(dupList)
            dupTextureTip='"'+self.TIPS_CODE.DUPLICATE_TEXTURE+'":'+self.listToStr(totalDupList)
            self.TIPS_LIST.append(dupTextureTip)
        return assetsDict
        
    def copyTipTxt(self):
        if os.path.exists(self.G_TIPS_TXT_NODE):
            tipTxtCmd = 'xcopy /y /f /v "' + os.path.normpath(self.G_TIPS_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(self.G_POOL_CONFIG) + '\\"'
            print tipTxtCmd
            self.RBcmd(tipTxtCmd)
        
    def loopInputAsset(self):
        if not self.ASSET_WEB_COOLECT_BY_PATH:
            listDirs = os.walk(self.ASSET_INPUT_DIR) 
            for root, dirs, files in listDirs: 
                for f in files: 
                    print f,os.path.join(root, f)
                    self.ASSET_INPUT_DIR_DICT[f]=os.path.join(root,f)
        
    def RBhanResult(self):#8
        #self.RBlog('结果处理','start')
        #self.G_ANALYSE_TXT.info('[BASE.RBhanResult.start.....]')
        #xcopy /y /f "C:\work\helper\20628\cfg\analyse_net.txt" "\\10.50.244.116\p5\config\962500\962712\20628\cfg\" 
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            if not os.path.exists(self.G_ANALYSE_TXT_NODETEMP):
                exit(-9)
            self.convertFileCode(self.G_ANALYSE_TXT_NODETEMP,self.G_ANALYSE_TXT_NODE,sys.getfilesystemencoding(),'utf-16')
            
        if not os.path.exists(self.G_ANALYSE_TXT_NODE):
            exit(-9)
        
        self.parseAnalyseTxt()
        if not self.ANALYSE_TXT_PARSER.has_section('max'):
            self.ANALYSE_TXT_PARSER.add_section('max')
        self.ANALYSE_TXT_PARSER.set('max', 'max', self.G_INPUT_CG_FILE)
        self.ANALYSE_TXT_PARSER.set('common', 'update', '20161001')
        self.ANALYSE_TXT_PARSER.set('common', 'projectSymbol', self.G_PROJECT_SYMBOL)
        self.ANALYSE_TXT_PARSER.set('common', 'sceneFile', self.G_INPUT_CG_FILE)

        self.loopInputAsset()
        
        self.getAllAsset()
        self.hanTips()
        
        analyseTxtCmd = 'xcopy /y /f /v  "' + os.path.normpath(self.G_ANALYSE_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(self.G_POOL_CONFIG) + '\\"'
        print analyseTxtCmd
        self.RBcmd(analyseTxtCmd)
        
        propertyTxtCmd = 'xcopy /y /f /v "' + os.path.normpath(self.G_PROPERTY_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(self.G_POOL_CONFIG) + '\\"'
        print propertyTxtCmd
        self.RBcmd(propertyTxtCmd)
        
        pluginCfgFile=os.path.join(self.G_HLEPER_TASK_CFG,'plugins.cfg')
        pluginCfgCmd = 'xcopy /y /f /v "' + os.path.normpath(pluginCfgFile) + '"' + ' ' + '"' + os.path.normpath(self.G_POOL_CONFIG) + '\\"'
        print pluginCfgCmd
        self.RBcmd(pluginCfgCmd)
        
        self.copyTipTxt()
        
        #self.G_ANALYSE_TXT.info('[BASE.RBhanResult.end.....]')
        #self.RBlog('done','end')
    
escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string
    
