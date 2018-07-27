import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Clarisse(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)

    def RBanalyse(self):
        self.G_ANALYSE_LOG.info('[Clarisse.RBanalyse.start.....]')
        
        netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
        netFile=netFile.replace('\\','/')

        # myCgVersion = self.CGSOFT.replace("_"," ")+self.CGV
        # myCgVersion = self.CGSOFT.replace("_"," ")

        #14.0.361r'C:\Program Files\Isotropix\Clarisse iFX 3.0 RC3\Clarisse\cnode.exe
        exePath=os.path.join(r'D:\plugins\clarisse',self.CGSOFT,r'Clarisse\cnode.exe')
        if self.G_RENDEROS=='Linux':
            exePath=r'/usr/isotropix/'+self.CGSOFT+'/clarisse/cnode'
        #analyseCmd=exePath + ' ' + self.clarisseFile + ' -info'
        #self.RBcmd(analyseCmd,True,False)
        if os.path.exists(self.CGFILE):
            self.G_ANALYSE_LOG.info('[Clarisse.RBanalyse.exe.....]'+exePath)
            try:
                self.proc =""
                cmdp= subprocess.Popen([exePath, self.CGFILE, '-info'],stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
                while True:
                    resultLine = cmdp.stdout.readline()
                    if resultLine == '' and cmdp.poll()!=None:
                        break
                    if resultLine!='' and resultLine.strip().startswith("<") and "<file>" not in resultLine:
                        self.proc =self.proc +resultLine
                        self.G_ANALYSE_LOG.info(resultLine)
                    
            except:
                print 'Run Analysis Failed!'
                self.G_ANALYSE_LOG.info('Run Analysis Failed!')
                self.clean()
                sys.exit(-1)
        else:
            self.G_ANALYSE_LOG.info('Error: The .project file is not exist.')
        self.G_ANALYSE_LOG.info('[Clarisse.RBanalyse.end.....]')

    def clean(self):
        myCgVersion = self.CGSOFT.replace("_"," ")
        cleanCmd='"C:/Python27/python.exe" "B:\\plugins\\clarisee\\lib\\python\\clearnlic.py" "'+myCgVersion+'"'
        # self.RBcmd(cleanCmd,True)

    def createXml(self): 
        netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
        netFile=netFile.replace('\\','/')
        try:
            if self.proc:
                with open(netFile, 'w') as xFile:
                    xFile.write(self.proc)
        except:
            print "Generate XML Failed!"
            self.clean()
            sys.exit(-1)

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGSOFT=self.CGSOFT.lower()
            # self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    # self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
                    self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"")

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)
        #self.RBcmd(umountcmd)

        self.G_ANALYSE_LOG.info('[config....]'+self.G_CONFIG)
        self.G_CONFIG = self.G_CONFIG.replace("\\","/")
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            # self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                for key in configJson["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
                    self.G_ANALYSE_LOG.info(cmd)
                    self.RBcmd(cmd,False,1)

    def copySoft(self):
        plant = "linux" if self.G_RENDEROS=='Linux' else "win"
        py_source = "B:\\plugins\\clarisse\\lib\\python\\SetupSoftvar.py "if not self.G_RENDEROS=='Linux' else "/B/plugins/clarisse/lib/python/SetupSoftvar.py "
        cmds = "c:\\python27\\python.exe " if not self.G_RENDEROS=='Linux' else "python "
        cmds += py_source
        cmds += "soft=%s "%self.CGSOFT
        cmds += "plant=%s"%plant
        self.G_ANALYSE_LOG.info('[cmd....]'+cmds)
        self.RBcmd(cmds,False,1)

    def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
        print str(continueOnErr)+'--->>>'+str(myShell)
        # self.G_ANALYSE_LOG.info('cmd...'+cmdStr)
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        while cmdp.poll()==None:
            resultLine = cmdp.stdout.readline().strip()
            if resultLine!='':
                self.G_ANALYSE_LOG.info(resultLine)
            
        resultStr = cmdp.stdout.read()
        resultCode = cmdp.returncode
        
        self.G_ANALYSE_LOG.info('resultStr...'+resultStr)
        self.G_ANALYSE_LOG.info('resultCode...'+str(resultCode))
        
        if not continueOnErr:
            if resultCode!=0:
                self.clean()
                sys.exit(resultCode)
        return resultStr

    def RBexecute(self):#Render
        self.G_ANALYSE_LOG.info('[Clarisse.RBexecute.start.....]')
        self.RBBackupPy()
        self.RBinitLog()
        self.RBmakeDir()
        if self.G_RENDEROS=='Linux':
            self.webMntPath();
        else:
            self.delSubst()
            self.webNetPath()
        self.copySoft()
        self.RBprePy()
        self.RBcopyTempFile()#copy py.cfg max file
        self.RBreadCfg()
        self.RBhanFile()
        
        self.RBconfig()
        self.RBanalyse()
        self.clean()
        self.createXml()
        self.RBpostPy()
        self.RBhanResult()
        self.G_ANALYSE_LOG.info('[Clarisse.RBexecute.end.....]')