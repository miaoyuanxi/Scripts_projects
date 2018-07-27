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

LOOP_DIR=r'\\10.50.100.2\Model\indoor'#D:/ARCH

ENV_PATH=r'\\10.50.100.2\Model\Env'
POOL_PATH=LOOP_DIR
RENDER_MAX_PY_MODEL=os.path.join(THIS_SCRIPT_PATH,'renderSilkroadModel.py')
BATCH_COUNT=8000

MUNU_IP='10.50.5.31'
MUNU_PORT='9915'
MUNU_URL="http://10.50.5.31:9915/sys/task_create?onstarted=1&operator=yanrk&script="
workRender=r'D:\work\render'
bPath=r'\\10.50.1.22\td'
renderSilkroadPy=r'\\10.50.244.116\p5\script\py\py\silkroad20\RenderSilkroadMax.py'
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
def getRenderPyContent(maxFolderName):
    
    maxFileName=(maxFolderName + '.max')
    maxFile= os.path.join(LOOP_DIR,maxFolderName,maxFileName )
    
    lineStr="##NBBEGIN{\r\n"
    sourceFolder=os.path.join(POOL_PATH,maxFolderName)
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
    lineStr+= "##name="+maxFileName+"\r\n"
    #lineStr+= "##requirements="+munuRequimentStr+"\r\n"
    lineStr+=  "##properties=SZ\r\n"
    lineStr+= "##level=80\r\n"
    lineStr+= "##custom=ycx\r\n"
    lineStr+= "##constraints=yunchuangxiang\r\n"
    lineStr+= "##nodelimit=1\r\n"
    lineStr+= "##nodeblacklimit=3\r\n"
    lineStr+= "##JOBS G_JOB_ID G_CG_RENDER_FRAME  \r\n"
    
    myFrame='1'
    jobStr = '##\'frame' + myFrame +'\' \''+myFrame+'\' \r\n'
    lineStr+= jobStr
    
    lineStr+= "##ENDJOBS\r\n"
    lineStr+= "##END\r\n"
    
    lineStr+= "}NBEND\r\n"

    #print lineStr
    return lineStr

#请求munu，发送任务
def askMunu(pyContentStr):
    req = urllib2.urlopen(MUNU_URL,pyContentStr)

    askMunuResult= req.read()
    return askMunuResult

def writeOKTxt(maxFile,taskIdStr):
    okTxt=os.path.join(THIS_SCRIPT_PATH,'ok.txt')
    okTxtObj=open(okTxt,'a')
    okTxtObj.write(maxFile+'\r\n')
    okTxtObj.close()
    
    
    taskTxt=os.path.join(THIS_SCRIPT_PATH,'tasklist.txt')
    taskTxtObj=open(taskTxt,'a')
    taskTxtObj.write(taskIdStr+maxFile+'\r\n')
    taskTxtObj.close()
    '''
    f = open(r'G:\huling\python\project\Model\pu\\'+files+'_silkroad_max_render.py','a')
    ff = maxFile
    f.write(ff)
    f.write('\r\n')
    f.close()
    '''

def writeErrTxt(maxFile):
    errTxt=os.path.join(THIS_SCRIPT_PATH,'err.txt')
    errTxtObj=open(errTxt,'a')
    errTxtObj.write(maxFile+'\r\n')
    errTxtObj.close()
    
#遍历目录
#查找场景文件
def hanFile():  
    print 'list dir start'
    dirs = os.listdir(LOOP_DIR)
    #open(okTxt=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'ok.txt')
    print 'list dir end'
    count=0
    for maxFolderName in dirs:
        print ''
        print maxFolderName
        if count>BATCH_COUNT:
            break
            
        print '------oktxt------'
        okTxt=os.path.join(THIS_SCRIPT_PATH,'ok.txt')
        okListTemp=[]
        okList=[]
        if os.path.exists(okTxt):
            okTxtObj=open(okTxt,'r')
            okListTemp=okTxtObj.readlines()
            okTxtObj.close()
            for okLine in okListTemp:
                okLine=okLine.replace('\r\n','')
                okList.append(okLine)
                
        print '------errtxt------'
        errTxt=os.path.join(THIS_SCRIPT_PATH,'err.txt')
        errList=[]
        errListTemp=[]
        if os.path.exists(errTxt):
            errTxtObj=open(errTxt,'r')
            errListTemp=errTxtObj.readlines()
            errTxtObj.close()
            for errLine in errListTemp:
                errLine=errLine.replace('\r\n','')
                errList.append(errLine)
        
        
        maxFile= os.path.join(LOOP_DIR,maxFolderName, (maxFolderName + '.max'))
        print maxFile
        if os.path.exists(maxFile):
            if (maxFile not in okList) and  maxFile not in errList:
                print '[ok]',maxFile
                pyContentStr=getRenderPyContent(maxFolderName)
                askMunuResult=askMunu(pyContentStr)
                writeOKTxt(maxFile,askMunuResult)
                count=count+1
                time.sleep(3)
            else:
                pass
        else:
            if  maxFile not in errList:
                print '[err2]',maxFile
                writeErrTxt(maxFile) 
                count=count+1
        
        
print 'start......'
hanFile()
print 'end........'