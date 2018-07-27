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


class RenderbusPath():
    def __init__(self,userPath):
        self.G_INPUT_USER=userPath
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
        
        self.G_HLEPER='C:/work/helper'
        
        configJson=eval(open(self.G_CONFIG, "r").read())
        self.G_ANALYSE_TXT_SERVER=configJson['common']["analyseTxt"]
        self.G_INPUT_USER=configJson['common']["inputUserPath"]
        self.G_BIG_TASK_ID=str(configJson['common']["taskId"])
        self.G_PROJECT_SYMBOL=str(configJson['common']["projectSymbol"])
        
        self.G_PLUGIN_PATH=configJson['mntMap']["B:"]
        
        self.G_HLEPER_TASK=os.path.join(self.G_HLEPER,self.G_BIG_TASK_ID).replace('\\','/')
        self.G_HLEPER_TASK_CFG=os.path.join(self.G_HLEPER_TASK,'cfg').replace('\\','/')
        self.G_ANALYSE_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'analyse_net.txt').replace('\\','/')
        self.G_PROPERTY_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'property.txt').replace('\\','/')
        self.G_TIPS_TXT_NODE=os.path.join(self.G_HLEPER_TASK_CFG,'tips.json').replace('\\','/')
        self.G_INPUT_CG_FILE=raw(configJson['common']["inputCgFile"]).decode("utf-8") 
        self.G_CG_VERSION='3ds Max '+configJson['common']["cgv"]
        self.G_PROGRAMFILES='C:/Program Files/Autodesk'
        self.G_POOL_CONFIG = self.G_POOL + '/config/' + os.path.join(self.G_USERID_PARENT, self.G_USERID) + '/' + self.G_BIG_TASK_ID
        
        
        self.G_MAXFIND='B:/plugins/max/maxfind/GetMaxProperty.exe'
        self.G_MAXFIND_MAX_VERSION_STR=None
        self.G_MAXFIND_MAX_VERSION_INT=None
        self.G_MAXFIND_RENDERER=None
        self.G_MAXFIND_OUTPUT_GAMMA=None
        
        
        self.assetInputDict     = {}
        self.renderbusPathObj   = RenderbusPath(self.G_INPUT_USER)
        self.checkIflItems      = []
        self.assetInputItems    = []
        self.assetiInputCount   = 1
        self.inputMissingItems  = []
        self.inputMissingCount  = 1
        
        self.TIPS_DICT={}
        self.ERRCODE_NO_INFO=100444
        self.WARNCODE_MAX_VERSION=103494
        print '\r\n==================================================\r\n'
        print 'G_CONFIG=',self.G_CONFIG 
        print 'G_PLUGINS=',self.G_PLUGINS
        print 'G_USERID=',self.G_USERID 
        print 'G_USERID_PARENT=',self.G_USERID_PARENT 
        print 'G_TASKID=',self.G_TASKID 
        print 'G_BIG_TASK_ID=',self.G_BIG_TASK_ID
        print 'G_POOL=',self.G_POOL
        print 'G_CG_VERSION=',self.G_CG_VERSION
        print 'G_INPUT_CG_FILE=',self.G_INPUT_CG_FILE        
        print 'G_HLEPER_TASK=',self.G_HLEPER_TASK 
        print 'G_ANALYSE_TXT_SERVER=',self.G_ANALYSE_TXT_SERVER
        print 'G_ANALYSE_TXT_NODE=',self.G_ANALYSE_TXT_NODE
        
        print '\r\n==================================================\r\n'
           

        if not os.path.exists(self.G_HLEPER_TASK_CFG):
            os.makedirs(self.G_HLEPER_TASK_CFG)
    
    def RBBackupPy(self):
        print '[MAX.RBBackupPy.start.....]'

        print '[MAX.RBBackupPy.end.....]'
        
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

    def maxfind(self):
        return#
        print '----------maxfind----------'
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE)
        if  os.path.exists(self.G_PROPERTY_TXT_NODE):
            os.remove(self.G_PROPERTY_TXT_NODE)
        maxFindCmdStr=self.G_MAXFIND+r' "' +helperMaxFile.replace('\\','/')+'">>'+self.G_PROPERTY_TXT_NODE
        self.RBcmd(maxFindCmdStr.encode(sys.getfilesystemencoding()))
        propertyObj=codecs.open(self.G_PROPERTY_TXT_NODE, "r", "UTF-8")
        
        
        for maxInfoLine in propertyObj.readlines():
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
            
            self.TIPS_DICT[self.ERRCODE_NO_INFO]=[]
            self.writeTips()
            self.copyTipTxt()
            exit(0)
            
    def conflict(self):
        pass
        
    def configMax(self):#config 3ds Max ,vray,plugin...and so on
        
        self.G_ANALYSE_LOG.info('[max.configMax.start.....]')
        
        self.maxfind()
        
        configJsonDict=eval(codecs.open(self.G_PLUGINS, "r",'utf-8').read())
        if self.G_CG_VERSION!=self.G_MAXFIND_MAX_VERSION_STR:
            self.TIPS_DICT[self.WARNCODE_MAX_VERSION]=[]
        
        if self.G_MAXFIND_RENDERER.startswith('vray'):
            myRenderVersion=self.G_MAXFIND_RENDERER.replace('vray','')
            if configJsonDict.has_key('plugins'):
                pluginDict=configJsonDict['plugins']
                pluginDict['vray']=myRenderVersion
            else:
                pluginDict={}
                pluginDict['vray']=myRenderVersion
                configJsonDict['plugins']=pluginDict
                        
        print configJsonDict
        '''
        pluginDict=configJsonDict["plugins"]
        if self.G_MAXFIND_RENDERER.startswith('vray'):
            pluginDict['vray']=str(self.G_MAXFIND_RENDERER.replace('vray',''))
        print pluginDict
        '''
        
        pluginCfgFile=os.path.join(self.G_HLEPER_TASK_CFG,'plugins.cfg')
        pluginCfgFileObj=codecs.open(pluginCfgFile,'a','UTF-8')
        pluginCfgFileObj.write(str(configJsonDict))
        pluginCfgFileObj.close()
        
        maxPlugin=MaxPlugin(self.G_ANALYSE_LOG,self.G_CG_VERSION,configJsonDict)
        maxPlugin.config()
        self.G_ANALYSE_LOG.info('[max.configMax.end.....]')
            
  
    def RBconfig(self):#5
        self.testMode()
        return#
        self.G_ANALYSE_LOG.info('[Max.RBconfig.start.....]')
        
        cleanMountFrom='try3 net use * /del /y'
        self.RBcmd(cleanMountFrom)
        
        
        if not os.path.exists(r'B:\plugins'):
            cmd='try3 net use B: '+self.G_PLUGIN_PATH.replace('/','\\')
            self.RBcmd(cmd)
            
            
        self.configMax()
        self.G_ANALYSE_LOG.info('[Max.RBconfig.end.....]')
        
    def RBanalyse(self):#7
        self.testMode()
        return#
        self.G_ANALYSE_LOG.info('[max.RBanalyse.start.....]')
        
        userMsScript=self.G_MAXSCRIPT+'/user/'+self.G_USERID+'/analyseU.ms'
        msScript=self.G_MAXSCRIPT+'/analyseU.ms'
        if os.path.exists(userMsScript):
            msScript=userMsScript
       #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms";analyseRun \"962712\" \"20628\" \"C:\work\helper\20628\max\要命要命不是人.max\" \"C:\work\helper\20628\cfg\analyse_net.txt\" "
        maxExe = '"'+self.G_PROGRAMFILES+'/'+self.G_CG_VERSION+'/3dsmax.exe'
        
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE) 
        #cfgtxt = os.path.join(self.G_HLEPER_TASK.replace('/','\\')) + '/cfg/analyse_net.txt\\" "'
        
        analyseCmd = maxExe + '" -silent -ma -mxs "filein \\"'+msScript +'\\";analyseRun \\"' + self.G_USERID +'\\" \\"' + self.G_BIG_TASK_ID + '\\" \\"' + helperMaxFile.replace('\\','/') + '\\" \\"' + self.G_ANALYSE_TXT_NODE.replace('\\','/') + '\\" "'
        #print analyseCmd
        analyseCmd = analyseCmd.encode(sys.getfilesystemencoding())
        self.RBcmd(analyseCmd)
        self.G_ANALYSE_LOG.info('[max.RBanalyse.end.....]')
        
    def writeTips(self):
        fl=codecs.open(self.G_TIPS_TXT_NODE, 'w', "UTF-8")
        fl.write(str(self.TIPS_DICT))
        fl.close()
        
    def hanTips(self):
        tipsList = self.getItemFromSection('tips')
        
        
        if self.ANALYSE_TXT_PARSER.has_section('tips'):
            dataDict={}
            itemKeyList = self.ANALYSE_TXT_PARSER.options('tips')
            
            for itemKey in itemKeyList:
                itemValList=[]
                itemVal = self.ANALYSE_TXT_PARSER.get('tips', itemKey).strip()
                if itemVal!=None and itemVal!='':
                    itemValList=itemVal.split('|')
                self.TIPS_DICT[int(itemKey.strip())]=itemValList
            #data = {10001:["aaa","bbb"],10004:[],12345:["ccc"]}
            jsonStr = json.dumps(self.TIPS_DICT,sort_keys=True,indent=4)
            print self.G_TIPS_TXT_NODE
            self.writeTips()

        
        
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
                #if ignore:
                #    rbFile = itemPath 
                #else:
                #    rbFile = self.renderbusPathObj.convertPath(itemPath)

                #print rbFile
                #itemList.append(rbFile)
                itemList.append(itemPath)
            
        return itemList
        

    def checkIfl(self, assetType, asset):
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
                        
                    self.gatherAsset(assetType, assetList)
                
    def gatherAsset(self, assetType, assetList):
        missingCount = 1
        for asset in assetList:
            
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            
            self.assetInputItems.append(asset)
            self.assetiInputCount = self.assetiInputCount + 1 
            
            if not os.path.exists(asset):
                self.ANALYSE_TXT_PARSER.set('asset_input_missing', ('path' + str(self.inputMissingCount)), asset)      
                self.inputMissingItems.append(asset)
                self.inputMissingCount = self.inputMissingCount + 1 
                
                self.ANALYSE_TXT_PARSER.set(assetType + '_missing', ('path' + str(missingCount)), asset)      
                missingCount = missingCount + 1 
            
            self.checkIfl(assetType, asset)

    def filterAsset(self, dict):
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
                    wildPath = self.renderbusPathObj.convertPath(asset)
                    resultList.append(wildPath)

                    if wildPath.endswith('.xml') and os.path.exists(wildPath):
                        root = ET.parse(wildPath).getroot()
                        
                        cacheType           = root.find('cacheType').get('Type')    # OneFile | OneFilePerFrame
                        format              = root.find('cacheType').get('Format')  # mcc | mcx
                        time                = root.find('time').get('Range')
                        cacheTimePerFrame   = root.find('cacheTimePerFrame').get('TimePerFrame')
                        
                        suffix      = '.mc' if format == 'mcc' else '.mcx'
                        cacheCount  = int(time.split('-')[1]) / int(cacheTimePerFrame)
                        
                        if cacheType == 'OneFilePerFrame':                        
                            for i in range(1, cacheCount + 1):
                                cacheFile = os.path.splitext(wildPath)[0] + 'Frame' + str(i) + suffix

                                resultList.append(cacheFile) 
                                
                        elif cacheType == 'OneFile':
                            cacheFile = wildPath.replace('.xml', suffix)
                            resultList.append(cacheFile)
                        
                
            else:
                resultList = map(self.renderbusPathObj.convertPath, assetList)    
               
            
            resultDict[key] = resultList
            return resultDict
            
        return handler
        
    def getAllAsset(self):
        assetsDict = {}

        assetsDict['texture']    = self.getItemFromSection('texture')
        assetsDict['vrmesh']     = self.getItemFromSection('vrmesh')
        assetsDict['alembic']    = self.getItemFromSection('alembic')
        assetsDict['fumefx']     = self.getItemFromSection('fumefx')
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
        dictList = map(self.filterAsset(assetsDict), assetsDict)
        for dict in dictList:
            for assetType, assetList in dict.items():
                if not self.ANALYSE_TXT_PARSER.has_section(assetType + '_missing'):
                    self.ANALYSE_TXT_PARSER.add_section(assetType + '_missing')
                
                self.gatherAsset(assetType, assetList)

        self.ANALYSE_TXT_PARSER.write(open(self.G_ANALYSE_TXT_NODE, 'w'))   
        
        return assetsDict
        
    def copyTipTxt(self):
        if os.path.exists(self.G_TIPS_TXT_NODE):
            tipTxtCmd = 'xcopy /y /f /v "' + os.path.normpath(self.G_TIPS_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(self.G_POOL_CONFIG) + '\\"'
            print tipTxtCmd
            self.RBcmd(tipTxtCmd)
        
    def RBhanResult(self):#8
        #self.RBlog('结果处理','start')
        #self.G_ANALYSE_TXT.info('[BASE.RBhanResult.start.....]')
        #xcopy /y /f "C:\work\helper\20628\cfg\analyse_net.txt" "\\10.50.244.116\p5\config\962500\962712\20628\cfg\" 
        if not os.path.exists(self.G_ANALYSE_TXT_NODE):
            exit(-9)

        self.parseAnalyseTxt()
        if not self.ANALYSE_TXT_PARSER.has_section('max'):
            self.ANALYSE_TXT_PARSER.add_section('max')
        self.ANALYSE_TXT_PARSER.set('max', 'max', self.G_INPUT_CG_FILE)
        self.ANALYSE_TXT_PARSER.set('common', 'update', '20161001')
        self.ANALYSE_TXT_PARSER.set('common', 'projectSymbol', self.G_PROJECT_SYMBOL)
        self.ANALYSE_TXT_PARSER.set('common', 'sceneFile', self.G_INPUT_CG_FILE)
        
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
    
