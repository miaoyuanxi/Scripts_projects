#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import codecs
import ConfigParser
import threading
import time
reload(sys)
sys.setdefaultencoding('utf-8')


def parseAnalyseTxt():
    G_ANALYSE_TXT_NODE=r'c:/nono/render.cfg'
    ANALYSE_TXT_PARSER = ConfigParser.ConfigParser()
    try:
    
        ANALYSE_TXT_PARSER.readfp(codecs.open(G_ANALYSE_TXT_NODE, "r", "UTF-16"))
        print '16'
    except Exception, e:
        try:
            ANALYSE_TXT_PARSER.readfp(codecs.open(G_ANALYSE_TXT_NODE, "r", "UTF-8"))
            print '8'
        except Exception, e:
            ANALYSE_TXT_PARSER.readfp(codecs.open(G_ANALYSE_TXT_NODE, "r"))
            print 'ee'
    return ANALYSE_TXT_PARSER
             
                     
def writeTips(str):
    fl=codecs.open('c:/nono/tips.json', 'w', "UTF-8")
    fl.write(str)
    fl.close()
    
def hanTips():
    ANALYSE_TXT_PARSER=parseAnalyseTxt()
    if ANALYSE_TXT_PARSER.has_section('tips'):
        dataDict={}
        itemKeyList = ANALYSE_TXT_PARSER.options('tips')
        resultStr=''
        for itemKey in itemKeyList:
            itemValList=[]
            itemVal = ANALYSE_TXT_PARSER.get('tips', itemKey).strip()
            if itemVal!=None and itemVal!='':
                resultStr=resultStr+itemKey+':'+itemVal+'\r\n'
             
        
        #resultStr=resultStr.encode(sys.getfilesystemencoding())
        #resultStr=resultStr.decode(sys.getfilesystemencoding(), 'utf-8')
        #resultStr=resultStr.decode('gbk', 'utf-8')
        #resultStr=resultStr.decode(sys.getfilesystemencoding())
        #print resultStr
        writeTips(resultStr)
        
hanTips()
        
        
        
        
             