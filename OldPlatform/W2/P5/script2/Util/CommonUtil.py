#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os

# class FileHandle

class Common(object):
    '''
        获取插件配置文件的字典
    ''' 
    @classmethod
    def GetPluginDict(self,pluginCfgPath):
        print '[GetPluginDict start]'
        print pluginCfgPath
        pluginInfoDict=None
        if  os.path.exists(pluginCfgPath):
            with open(pluginCfgPath,'r') as fp:
                print 'plugins file is exists'
                listOfplgCfg = fp.readlines()
                removeNL = [(i.rstrip('\n')) for i in listOfplgCfg]
                combinedText = ''.join(removeNL)
                pluginInfoDict = eval('dict(%s)' % combinedText)
                print pluginInfoDict
                for i in pluginInfoDict.keys():
                    print i
                    print pluginInfoDict[i]
        print '[GetPluginDict end]'
        return pluginInfoDict
