#! /usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import codecs
import string
import urllib
import urllib2
import time
import httplib

reload(sys)
sys.setdefaultencoding('utf-8')

THIS_SCRIPT_PATH=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
MS_SCRIPT_FILE=r'\\10.50.100.2\Model\script'
#Animal  Character   Transport   Technology   Architecture  Landscape
#LOOP_DIR=r'\\10.50.100.2\Model\Technology'#D:/ARCH

ENV_PATH=r'\\10.50.100.2\Model\Env'

RENDER_MAX_PY_MODEL=os.path.join(THIS_SCRIPT_PATH,'renderModelYCX.py')

MUNU_IP='10.50.5.31'
MUNU_PORT='9915'
MUNU_URL="http://10.50.5.31:9915/sys/task_create?onstarted=1&operator=yanrk&script="
workRender=r'D:\work\render'
bPath=r'\\10.50.1.22\td'
renderSilkroadPy=r'\\10.50.244.116\p5\script\py\py\silkroad20\RenderMaxYCX.py'
maxB='B:/plugins/max'
programFiles='C:/Program Files'
maxVersion='3ds Max 2014'
pluginDict={u'3rdPartyShaders': {}, u'renderSoftware': u'3ds Max',u'softwareVer': u'2014', u'plugins': {'vray': u'3.00.03'}}
logPath='C:/LOG/SILKROAD20.TXT'

#封装运行命令
def rbCmd(cmdStr,continueOnErr=False,myShell=False):
    print cmdStr
    cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
    cmdp.stdin.write('3/n')
    cmdp.stdin.write('4/n')
    while cmdp.poll()==None:
        resultLine = cmdp.stdout.readline().strip()
        if resultLine!='':
            print resultLine
        
    resultStr = cmdp.stdout.read()
    resultCode = cmdp.returncode
    
    print resultStr
    print resultCode
    
    if not continueOnErr:
        if resultCode!=0:
            sys.exit(resultCode)
    return resultStr

#获取渲染模板的内容
def getRenderPyContent(maxFolderNameList,LOOP_DIR):
    
    taskName=os.path.basename(LOOP_DIR)+'_'+time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    #POOL_PATH=LOOP_DIR
    lineStr="##NBBEGIN{\r\n"
    sourceFolder=LOOP_DIR
    lineStr+='sourceFolder=r\''+sourceFolder+'\'\r\n'
    lineStr+='scriptFile=r\''+MS_SCRIPT_FILE+'\'\r\n'
    lineStr+='workRender=r\''+workRender+'\'\r\n'
    lineStr+='envPath=r\''+ENV_PATH+'\'\r\n'
    lineStr+='bPath=r\''+bPath+'\'\r\n'
    lineStr+='renderSilkroadPy=r\''+renderSilkroadPy+'\'\r\n'
    lineStr+='maxB=r\''+maxB+'\'\r\n'
    lineStr+='programFiles=r\''+programFiles+'\'\r\n'
    lineStr+='maxVersion=r\''+maxVersion+'\'\r\n'
    lineStr+='pluginDict=r\"'+str(pluginDict)+'\"\r\n'
    lineStr+='logPath=r\''+logPath+'\'\r\n'
    pycfgObject=codecs.open(RENDER_MAX_PY_MODEL,encoding='utf-8')
    renderPyContent=pycfgObject.readlines()

    pycfgObject.close()
    lineStr+=(''.join(renderPyContent))
    
    lineStr+='\r\n'
    lineStr+= "##BEGIN\r\n"
    lineStr+= "##description=yunchuangxiang\r\n"
    lineStr+= "##name="+taskName+"\r\n"
    #lineStr+= "##requirements="+munuRequimentStr+"\r\n"
    lineStr+=  "##properties=SZ\r\n"
    lineStr+= "##level=80\r\n"
    lineStr+= "##custom=ycx\r\n"
    lineStr+= "##constraints=yunchuangxiang\r\n"
    lineStr+= "##nodelimit=1\r\n"
    lineStr+= "##nodeblacklimit=3\r\n"
    lineStr+= "##JOBS G_JOB_ID MAX_FOLDER_NAME  \r\n"
    
    
    for maxFolderName in maxFolderNameList:
        jobStr = '##\'frame_' + maxFolderName +'\' \''+maxFolderName+'\' \r\n'
        lineStr+= jobStr
    
    lineStr+= "##ENDJOBS\r\n"
    lineStr+= "##END\r\n"
    
    lineStr+= "}NBEND\r\n"

    print lineStr
    return lineStr

#请求munu，发送任务
def askMunu(pyContentStr):
    req = urllib2.urlopen(MUNU_URL,pyContentStr)

    askMunuResult= req.read()
    return askMunuResult

    
#遍历目录
#查找场景文件
def hanFile():  
    print 'list dir start'
    LOOP_DIR=sys.argv[1]
    print '--------------------------'
    print LOOP_DIR
    if LOOP_DIR!=None and LOOP_DIR!='':
        dirs = os.listdir(LOOP_DIR)
        #open(okTxt=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'ok.txt')
        print 'list dir end'
        count=0
        maxFolderNameList=[]
        for maxFolderName in dirs:
            print ''
            print maxFolderName
            
            maxFile= os.path.join(LOOP_DIR,maxFolderName, (maxFolderName + '.max'))
            print maxFile
            if os.path.exists(maxFile):
                maxFolderNameList.append(maxFolderName)
        if maxFolderNameList.count>0:
            pyContentStr=getRenderPyContent(maxFolderNameList,LOOP_DIR)
            askMunuResult=askMunu(pyContentStr)
        
print 'start......'
hanFile()
print 'end........'