#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import os,sys,subprocess,string,logging,time,shutil
import glob
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
        self.G_PROPERTY_TXT_NODE=os.path.join(self.G_HLEPER_TASK,'cfg','property.txt').replace('\\','/')
        self.G_TIPS_TXT_NODE=os.path.join(self.G_HLEPER_TASK,'cfg','tips.txt').replace('\\','/')
        self.G_INPUT_CG_FILE=raw(configJson['common']["inputCgFile"]).decode("utf-8") 
        self.G_CG_VERSION='3ds Max '+configJson['common']["cgv"]
        self.G_PROGRAMFILES='C:/Program Files/Autodesk'
        self.G_MAXFIND='B:/plugins/max/maxfind/GetMaxProperty.exe'
        self.G_MAXFIND_MAX_VERSION_STR=None
        self.G_MAXFIND_MAX_VERSION_INT=None
        self.G_MAXFIND_RENDERER=None
        self.G_MAXFIND_OUTPUT_GAMMA=None
        #self.G_CHECKIFL=os.path.join(self.G_INPUT_CG_FILE.replace('/','\\')) + '.ifl'
        
        self.assetInputDict     = {}
        self.renderbusPathObj   = RenderbusPath()
        self.checkIflItems      = []
        self.assetInputItems    = []
        self.assetiInputCount   = 1
        self.inputMissingItems  = []
        self.inputMissingCount  = 1
    
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
        print '----------maxfind----------'
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE)
        if not os.path.exists(self.G_PROPERTY_TXT_NODE):
            maxFindCmdStr=self.G_MAXFIND+r' "' +helperMaxFile.replace('\\','/')+'">>'+self.G_PROPERTY_TXT_NODE
            #self.RBcmd(maxFindCmdStr.encode(sys.getfilesystemencoding()))
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
            exit(-9)
            
    def conflict(self):
        pass
        
    def configMax(self):#config 3ds Max ,vray,plugin...and so on
        return
        self.G_ANALYSE_LOG.info('[max.configMax.start.....]')
        
        self.maxfind()
        
        configJsonDict=eval(codecs.open(self.G_PLUGINS, "r",'utf-8').read())
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
        maxPlugin=MaxPlugin(self.G_ANALYSE_LOG,self.G_CG_VERSION,configJsonDict)
        maxPlugin.config()
        self.G_ANALYSE_LOG.info('[max.configMax.end.....]')
            
    def RBconfig(self):#5
        self.G_ANALYSE_LOG.info('[Max.RBconfig.start.....]')
        self.configMax()
        self.G_ANALYSE_LOG.info('[Max.RBconfig.end.....]')
        
    def RBanalyse(self):#7
        self.G_ANALYSE_LOG.info('[max.RBanalyse.start.....]')
        
        
        #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms\";analyseRun \"962712\" \"20628\" \"C:/work/helper/20628/max/要命要命不是人.max\" \"c:/work/helper/20628/cfg/analyse_net.txt\" "
        #"C:/Program Files/Autodesk/3ds Max 2014/3dsmax.exe" -silent -ma -mxs "filein \"B:/plugins/max/script/analyseU.ms";analyseRun \"962712\" \"20628\" \"C:\work\helper\20628\max\要命要命不是人.max\" \"C:\work\helper\20628\cfg\analyse_net.txt\" "
        maxExe = '"'+self.G_PROGRAMFILES+'/'+self.G_CG_VERSION+'/3dsmax.exe'+'"'+' -silent -ma -mxs "filein '+'\\"'
        scriptBpath = self.G_MAXSCRIPT+'/analyseU.ms\\";'+'analyseRun '
        helperMaxFile = self.G_HLEPER_TASK + '\\max\\' + os.path.basename(self.G_INPUT_CG_FILE.replace('/','\\')) + '\\" '
        #cfgtxt = os.path.join(self.G_HLEPER_TASK.replace('/','\\')) + '/cfg/analyse_net.txt\\" "'
        
        analyseCmd = maxExe + scriptBpath +'\\"' + self.G_USERID +'\\" \\"' + self.G_TASKID + '\\" \\"' + helperMaxFile.replace('/','\\') + '\\"' + self.G_ANALYSE_TXT_NODE.replace('/','\\') + '\\" \\"'+self.G_TIPS_TXT_NODE.replace('/','\\') +'\\" "'
        #print analyseCmd
        analyseCmd = analyseCmd.encode(sys.getfilesystemencoding())
        #self.RBcmd(analyseCmd)
        self.G_ANALYSE_LOG.info('[max.RBanalyse.end.....]')
        
        
    def hanTips(self):
        tipsList = self.getItemFromSection('tips')
        
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

                    self.gatherAsset(assetList)    
                               
    def gatherAsset(self, assetList):
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input')
        for asset in assetList:
            assetInputKey = self.ANALYSE_TXT_PARSER.set('asset_input', ('path' + str(self.assetiInputCount)), asset)
            
            self.assetInputItems.append(asset)
            self.assetiInputCount = self.assetiInputCount + 1 
            
            if not os.path.exists(asset):
                self.inputMissingItems.append(asset)
            
            self.checkIfl(asset)

    def filterAsset(self, dict):
        assetsDict = dict
        def handler(key):
            list = []
            assetList = assetsDict[key]
            
            # handle fumefx & realflow & pc2 & pointcache
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
                    for i in range(start - 1, end, -1 if start > end else 1):
                        
                        if i >= 0:
                            file = wildPath[:pos] + '%04d' % i + '.fxd'
                        else:
                            file = wildPath[:pos] + str(i) + '.fxd'
                        
                        list.append(self.renderbusPathObj.convertPath(file)) 
                        
            elif key == 'realflow':
                 for asset in assetList:
                    wildPath = asset
                    fileNames = glob.glob(self.renderbusPathObj.convertPath(wildPath))
                    for file in fileNames:
                        list.append(self.renderbusPathObj.convertPath(file)) 
                    
            else:
                list = map(self.renderbusPathObj.convertPath, assetList)    
                
            return list  
            
        return handler
        
    def getAllAsset(self):
        assetsDict = {}
        
        assetsDict['texture']    = self.getItemFromSection('texture')
        assetsDict['vrmesh']     = self.getItemFromSection('vrmesh')
        assetsDict['alembic']    = self.getItemFromSection('alembic')
        assetsDict['fumefx']     = self.getItemFromSection('fumefx')
        assetsDict['pc2']        = self.getItemFromSection('pc2')
        #assetsDict['error']      = self.getItemFromSection('error')
        assetsDict['pointcache'] = self.getItemFromSection('pointcache')
        assetsDict['realflow']   = self.getItemFromSection('realflow')
        assetsDict['ies']        = self.getItemFromSection('ies')

        assetList = map(self.filterAsset(assetsDict), assetsDict)
        for assets in assetList:
            self.gatherAsset(assets)
  
        if not self.ANALYSE_TXT_PARSER.has_section('asset_input_missing'):
            self.ANALYSE_TXT_PARSER.add_section('asset_input_missing')
        
        for item in self.inputMissingItems:
            self.ANALYSE_TXT_PARSER.set('asset_input_missing', ('path' + str(self.inputMissingCount)), item)
            self.inputMissingCount = self.inputMissingCount + 1        
            
        self.ANALYSE_TXT_PARSER.write(open(self.G_ANALYSE_TXT_NODE, 'w'))   
        
        return assetsDict
        
        
    def RBhanResult(self):#8
        #self.RBlog('结果处理','start')
        #self.G_ANALYSE_TXT.info('[BASE.RBhanResult.start.....]')
        #xcopy /y /f "C:\work\helper\20628\cfg\analyse_net.txt" "\\10.50.244.116\p5\config\962500\962712\20628\cfg\" 
        if not os.path.exists(self.G_ANALYSE_TXT_NODE):
            exit(-9)

        self.parseAnalyseTxt()
        self.getAllAsset()
        self.hanTips()
        
        dstDir = self.G_POOL + '/config/' + os.path.join(self.G_USERID_PARENT, self.G_USERID) + '/' + self.G_TASKID 
        analyseTxtCmd = 'xcopy /y /f "' + os.path.normpath(self.G_ANALYSE_TXT_NODE) + '"' + ' ' + '"' + os.path.normpath(dstDir) + '\\cfg\\"'
        print analyseTxtCmd
        #self.RBcmd(analyseTxtCmd)
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
    
