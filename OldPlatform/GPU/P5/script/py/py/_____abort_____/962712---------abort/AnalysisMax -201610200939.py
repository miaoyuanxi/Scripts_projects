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
        
        self.assetInputDict = {}
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
        
        
        
    def maxfindCmd(self,cmdStr,continueOnErr=False,myShell=1):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        self.G_ANALYSE_LOG.info(cmdStr)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine == '' and cmdp.poll()!=None:
                break
            self.G_ANALYSE_LOG.info(resultLine)
               
                
    def maxfind(self):
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE)
        
        maxFindCmdStr=r'B:/plugins/max/maxfind/GetMaxProperty.exe "' +helperMaxFile.replace('\\','/')+'"'
        self.maxfindCmd(maxFindCmdStr.encode(sys.getfilesystemencoding()))
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
        
        
        self.maxfind()
        
        
        
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
                # print itemKey
                itemPath = self.ANALYSE_TXT_PARSER.get(section, itemKey).strip()
                # print itemPath
                if itemPath.startswith('startframe') or itemPath.startswith('endframe'):
                    rbFile = itemPath 
                else:
                    rbFile = self.renderbusPathObj.convertPath(itemPath)

                print rbFile
                itemList.append(rbFile)
            
        return itemList
        
    #def checkType(self, ext):
    #    if asset.endswith('.ifl'):
            
    
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

                    self.gatherAsset('texture', assetList)
                    
    def checkFumeFX(self, asset):
        if asset.endswith('.fxd'):
            for fxfile in asset:
                print fxfile
                
                
            #error...self.gatherAsset(assetList)
                
                               
    def gatherAsset(self, assetName, assetList):
        # handle fumefx & realflow & pc2 & pointcache
        if assetName == 'fumefx':
            index = 0
            while index < len(assetList):
                asset = assetList[index]
                
                print index, asset
                if not os.path.isfile(asset):
                    # not exist then check sequence frames
                    if asset.startswith('startframe'):
                        startFrame = assetList[index].split('=')[1]
                        if assetList[index + 1].startswith('endframe'):
                            endFrame = assetList[index + 1].split('=')[1]
                        # build sequence number
                        start = int(startFrame);
                        end   = int(endFrame);

                        for i in range(start - 1, end + 1, -1 if start > end else 1):
                            if i >= 0:
                                print assetList[index + 2].replace('*', '%04d' % i)
                            else:
                                print assetList[index + 2].replace('*', str(i))
                        index += 3
                    else:
                        self.inputMissingItems.append(asset)
                        index += 1
                        continue
                else:
                    # exist then append
                    assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
                    
                    self.assetInputItems.append(asset)
                    self.assetiInputCount = self.assetiInputCount + 1
                    
                    index += 1
            #for asset in assetList:          
            #    if not os.path.exists(asset):
            #        # sequence frames
            #        if asset.startswith('startframe'):
            #            print '*******************'
            #            startFrame = asset.split('=')[1]
            #        elif asset.startswith('endframe'):
            #            endFrame = asset.split('=')[1]
            #        else:
            #            self.inputMissingItems.append(asset)
            #            continue
            #    else:
            #        assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            #        
            #        self.assetInputItems.append(asset)
            #        self.assetiInputCount = self.assetiInputCount + 1 
            
        elif assetName == 'realflow':
            for asset in assetList:
                assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
                
                self.assetInputItems.append(asset)
                self.assetiInputCount = self.assetiInputCount + 1 
                
                if not os.path.exists(asset):
                    self.inputMissingItems.append(asset)
        elif assetName == 'pc2':
            for asset in assetList:
                assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
                
                self.assetInputItems.append(asset)
                self.assetiInputCount = self.assetiInputCount + 1 
                
                if not os.path.exists(asset):
                    self.inputMissingItems.append(asset)
        elif assetName == 'pointcache':
            for asset in assetList:
                assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
                
                self.assetInputItems.append(asset)
                self.assetiInputCount = self.assetiInputCount + 1 
                
                if not os.path.exists(asset):
                    self.inputMissingItems.append(asset)
        else:
            for asset in assetList:
                assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
                
                self.assetInputItems.append(asset)
                self.assetiInputCount = self.assetiInputCount + 1 
                
                if not os.path.exists(asset):
                    self.inputMissingItems.append(asset)
                
                self.checkIfl(asset)
                #error---------self.fumeFX(asset)
              
    def getAllAsset(self):
        assetDict = {}
        
        self.assetInputDict['texture']    = self.getItemFromSection('texture')
        self.assetInputDict['vrmesh']     = self.getItemFromSection('vrmesh')
        self.assetInputDict['alembic']    = self.getItemFromSection('alembic')
        self.assetInputDict['fumefx']     = self.getItemFromSection('fumefx')
        self.assetInputDict['pc2']        = self.getItemFromSection('pc2')
        self.assetInputDict['error']      = self.getItemFromSection('error')
        self.assetInputDict['pointcache'] = self.getItemFromSection('pointcache')
        self.assetInputDict['realflow']   = self.getItemFromSection('realflow')
        self.assetInputDict['ies']        = self.getItemFromSection('ies')
        
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input')
            
        for (key, value) in  self.assetInputDict.items():
            self.gatherAsset(key, value)
        
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
    
