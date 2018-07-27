#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import os,sys,subprocess,string,logging,time,shutil
import logging
import codecs
import ConfigParser

from AnalysisBase import AnalysisBase
from MaxPlugin import MaxPlugin

class RenderbusPath():
    def __init__(self):
        self.G_INPUT_USER=r'\\10.50.241.1\d\inputdata5\962500\962712'
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

        absPath=[['a:/','/a/'],
            ['b:/','/b/'],
            ['c:/','/c/'],
            ['d:/','/d/']]
            
        resultMaxFile = itemPath
        src_max_lowercase = os.path.normpath(itemPath.lower()).replace('\\', '/')
        is_abcd_path = False;
        is_InterPath = False;
        
        if self.InterPath(src_max_lowercase):
            start,rest = self.parseInterPath(src_max_lowercase)
            resultMaxFile= self.G_INPUT_USER + '/net' + start.replace('//', '/') + rest.replace('\\', '/') 
        else:
            resultMaxFile= self.G_INPUT_USER + '\\' + itemPath.replace('\\', '/').replace(':','')

        return os.path.normpath(resultMaxFile)
        

class Max(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "max.INIT"

        self.G_MAX_B='B:/plugins/max'
        self.G_MAXSCRIPT=self.G_MAX_B+'/script'
        self.G_MAXSCRIPT_NAME='analyseU.ms'#max2013,max204,max2015
        self.G_INPUT_USER=r'\\10.50.241.1\d\inputdata5\962500\962712'
        self.G_HLEPER='C:/work/helper'
        self.G_HLEPER_TASK=os.path.join(self.G_HLEPER,self.G_TASKID).replace('\\','/')
        configJson=eval(open(self.G_CONFIG, "r").read())
        self.G_ANALYSE_TXT_SERVER=configJson['common']["analyseTxt"]
        self.G_ANALYSE_TXT_NODE=os.path.join(self.G_HLEPER_TASK,'cfg','analyse_net.txt').replace('\\','/')
        self.G_INPUT_CG_FILE=raw(configJson['common']["inputCgFile"]).decode("utf-8") 
        self.G_CG_VERSION='3ds Max '+configJson['common']["cgv"]
        self.G_PROGRAMFILES='C:/Program Files/Autodesk'
        
        
        self.renderbusPathObj = RenderbusPath()
        self.checkIflItems    = []
        self.assetInputItems  = []
        self.assetiInputCount = 1
        self.inputMissingItems = []
        self.inputMissingCount = 1
    
        print '\r\n==================================================\r\n'
        print 'G_CONFIG=',self.G_CONFIG 
        print 'G_PLUGINS=',self.G_PLUGINS
        print 'G_USERID=',self.G_USERID 
        print 'G_USERID_PARENT=',self.G_USERID_PARENT 
        print 'G_TASKID=',self.G_TASKID 
        print 'G_POOL=',self.G_POOL
        print 'G_CG_VERSION=',self.G_CG_VERSION
        print 'G_INPUT_CG_FILE=',self.G_INPUT_CG_FILE        
        print 'G_HLEPER_TASK=',self.G_HLEPER_TASK 
        print 'G_ANALYSE_TXT_SERVER=',self.G_ANALYSE_TXT_SERVER
        print 'G_ANALYSE_TXT_NODE=',self.G_ANALYSE_TXT_NODE
        
        print '\r\n==================================================\r\n'
           

                
    def RBreadCfg(self):#4
        self.G_ANALYSE_LOG.info('[Max.RBreadCfg.start.....]')
        self.G_ANALYSE_LOG.info('[Max.RBreadCfg.end.....]')
        
    def RBhanFile(self):#3copy max file
        self.G_ANALYSE_LOG.info('[max.RBhanFile.start.....]')
        #C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "\\10.50.241.1\d\inputdata5\962500\962712\d\NONO\test_scene\0simpleTest\max2012-2014复杂贴图打包\要命要命不是人.max" /to="C:\work\helper\20628\max\"
        copyCmdStr = r'C:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "' + os.path.join(self.G_INPUT_CG_FILE.replace('/','\\'))+'" /to="'+self.G_HLEPER_TASK.replace('/','\\')+'\\max\\"'
        print copyCmdStr
        copyCmdStr=copyCmdStr.encode(sys.getfilesystemencoding())
        #self.RBcmd(copyCmdStr)
        self.G_ANALYSE_LOG.info('[max.RBhanFile.end.....]')
        
        
    def maxfind(self):
        pass
        
    def conflict(self):
        pass
        
    def configMax(self):#config 3ds Max ,vray,plugin...and so on
        self.G_ANALYSE_LOG.info('[max.configMax.start.....]')
        configJson=eval(open(self.G_PLUGINS, "r").read())
        pluginDict=configJson["plugins"]
        print pluginDict
        maxPlugin=MaxPlugin(self.G_ANALYSE_LOG,self.G_CG_VERSION,pluginDict)
        #maxPlugin.config()
        self.G_ANALYSE_LOG.info('[max.configMax.end.....]')
        
        
    def RBanalyse(self):#7
        self.G_ANALYSE_LOG.info('[max.RBanalyse.start.....]')
        #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms\";analyseRun \"962712\" \"20628\" \"C:/work/helper/20628/max/要命要命不是人.max\" \"c:/work/helper/20628/cfg/analyse_net.txt\" "
        #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms";analyseRun \"962712\" \"20628\" \"C:\work\helper\20628\max\要命要命不是人.max\" \"C:\work\helper\20628\cfg\analyse_net.txt\" "
        maxExe = '"'+self.G_PROGRAMFILES+'/'+self.G_CG_VERSION+'/3dsmax.exe'+'"'+' -silent -ma -mxs "filein '+'\\"'
        scriptBpath = self.G_MAXSCRIPT+'/analyseU.ms\\";'+'analyseRun '
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE.replace('/','\\')) + '\\" '
        cfgtxt = os.path.join(self.G_HLEPER_TASK.replace('/','\\')) + '/cfg/analyse_net.txt\\" "'
        analyseCmd = maxExe + scriptBpath +'\\"' + self.G_USERID +'\\" \\"' + self.G_TASKID + '\\" \\"' + helperMaxFile.replace('/','\\') + '\\"' + cfgtxt.replace('/','\\')
        #print analyseCmd
        analyseCmd = analyseCmd.encode(sys.getfilesystemencoding())
        #self.RBcmd(analyseCmd)
        self.G_ANALYSE_LOG.info('[max.RBanalyse.end.....]')
    
    def parseAnalyseTxt(self):
        
        self.ANALYSE_TXT_PARSER = ConfigParser.ConfigParser()
        try:
            self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r", "UTF-16"))
        except Exception, e:
            try:
                self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r", "UTF-8"))
            except Exception, e:
                self.ANALYSE_TXT_PARSER.readfp(codecs.open(self.G_ANALYSE_TXT_NODE, "r"))
             
    def getItemFromSection(self, section):
        itemList = []
        if self.ANALYSE_TXT_PARSER.has_section(section):
            itemKeyList = self.ANALYSE_TXT_PARSER.options(section)
            print itemKeyList
            for itemKey in itemKeyList:
                print itemKey
                itemPath = self.ANALYSE_TXT_PARSER.get(section,itemKey)
                print itemPath
                rbFile = self.renderbusPathObj.convertPath(itemPath)
                print rbFile
                itemList.append(rbFile)
            
        return itemList
    
    def checkIfl(self, asset):
        if asset.endswith('.ifl'):
            if os.path.exists(asset):
                with codecs.open(asset, 'r', 'utf-8') as iflFile:
                    assetList = []
                    for line in iflFile:
                        # remove bom tag 
                        if bytes(line)[:3] == codecs.BOM_UTF8:
                            line = bytes(line)[3:]

                        normalPath = self.renderbusPathObj.convertPath(line.decode('utf-8').strip())
                        assetList.append(normalPath)

                    self.gatherAsset(assetList)
                    
                    
                            
    def gatherAsset(self, assetList):
        for asset in assetList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            self.assetInputItems.append(asset)
            self.assetiInputCount = self.assetiInputCount + 1 
            
            if not os.path.exists(asset):
                self.inputMissingItems.append(asset)
            
            self.checkIfl(asset)
              
            
    def getAllAsset(self):
        assetDict = {}
        
        textureList    = self.getItemFromSection('texture')
        vrmeshList     = self.getItemFromSection('vrmesh')
        alembicList    = self.getItemFromSection('alembic')
        fumefxList     = self.getItemFromSection('fumefx')
        pc2List        = self.getItemFromSection('pc2')
        errorList      = self.getItemFromSection('error')
        pointcachelist = self.getItemFromSection('pointcache')
        realflowList   = self.getItemFromSection('realflow')
        iesList        = self.getItemFromSection('ies')
        
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input')
        
        # 1
        self.gatherAsset(textureList);
        # 2
        self.gatherAsset(vrmeshList);
        # 3
        self.gatherAsset(alembicList);
        # 4
        self.gatherAsset(fumefxList);
        # 5
        self.gatherAsset(pc2List);
        # 6
        self.gatherAsset(errorList);
        # 7
        self.gatherAsset(pointcachelist);
        # 8
        self.gatherAsset(realflowList);
        # 9
        self.gatherAsset(iesList);
        
        """
        for texture in textureList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), texture)
            assetInputItems.append(texture)
            assetiInputCount = assetiInputCount + 1  
        for vrmesh in vrmeshList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), vrmesh)
            assetInputItems.append(vrmesh)
            assetiInputCount = assetiInputCount + 1
        for alembic in alembicList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), alembic)
            assetInputItems.append(alembic)
            assetiInputCount = assetiInputCount + 1
        for fumefx in fumefxList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), fumefx)
            assetInputItems.append(fumefx)
            assetiInputCount = assetiInputCount + 1
        for pc2 in pc2List:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), pc2)
            assetInputItems.append(pc2)
            assetiInputCount = assetiInputCount + 1
        for error in errorList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), error)
            assetInputItems.append(error)
            assetiInputCount = assetiInputCount + 1
        for pointcache in pointcachelist:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), pointcache)
            assetInputItems.append(pointcache)
            assetiInputCount = assetiInputCount + 1
        for realflow in realflowList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), realflow)
            assetInputItems.append(realflow)
            assetiInputCount = assetiInputCount + 1
        for ies in iesList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(assetiInputCount)), ies)
            assetInputItems.append(ies)
            assetiInputCount = assetiInputCount + 1            
        """
        
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input_missing'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input_missing')
        
        for item in self.inputMissingItems:
            self.ANALYSE_TXT_PARSER.set('asset_input_missing', ('path' + str(self.inputMissingCount)), item)
            self.inputMissingCount = self.inputMissingCount + 1        
            
        self.ANALYSE_TXT_PARSER.write(open(self.G_ANALYSE_TXT_NODE, 'w'))   
        
        return assetDict
        
        
    def RBhanResult(self):#8
        #self.RBlog('结果处理','start')
        #self.G_ANALYSE_TXT.info('[BASE.RBhanResult.start.....]')
        #xcopy /y /f "C:\work\helper\20628\cfg\analyse_net.txt" "\\10.50.244.116\p5\config\962500\962712\20628\cfg\" 
        
        #self.checkIfl()
        self.parseAnalyseTxt()
        self.getAllAsset()
        
        dstDir = self.G_POOL + '/config/' + os.path.join(self.G_USERID_PARENT, self.G_USERID) + '/' + self.G_TASKID 
        analyseTxtCmd = 'xcopy /y /f "' + os.path.normpath(self.G_ANALYSE_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(dstDir) + '\\cfg\\"'
        print analyseTxtCmd
        self.RBcmd(analyseTxtCmd)
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
    
