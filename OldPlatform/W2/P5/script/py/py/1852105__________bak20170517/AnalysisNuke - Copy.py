import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Nuke(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "Nuke.INIT"
        self.G_ANALYSEBAT_NAME='Enalyze.py'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV=''
        
        
        print 'self.G_CONFIG-----',self.G_CONFIG
        if os.path.exists(self.G_CONFIG):
            self.RENDER_JSON=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]
            self.CGSOFT=self.RENDER_JSON['common']["cgSoftName"]
            self.CGV=self.RENDER_JSON['common']["cgv"]
            self.RTASKID=self.RENDER_JSON['common']["taskId"]
            print self.RENDER_JSON
        else:
            sys.exit(-1)
        
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_ANALYSE_LOG.info('[Nuke.RBhanFile.start.....]')

        self.G_ANALYSE_LOG.info('[Nuke.RBhanFile.end.....]')
        
    def RBconfig(self):#5
        self.G_ANALYSE_LOG.info('[Nuke.RBconfig.start.....]')
        self.G_ANALYSE_LOG.info('[Nuke.RBconfig.end.....]')
    
    def RBanalyse(self):#7
        self.G_ANALYSE_LOG.info('[Nuke.RBanalyse.start.....]')
        #TODO
        
        self.G_ANALYSE_LOG.info('[Nuke.RBanalyse.end.....]')

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
        
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]
            self.CGSOFT=self.RENDER_JSON['common']["cgSoftName"]
            self.CGV=self.RENDER_JSON['common']["cgv"]
            self.RTASKID=self.RENDER_JSON['common']["taskId"]
            
            if isinstance(self.RENDER_JSON["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in self.RENDER_JSON["mntMap"]:
                    self.RBcmd("net use "+key+" "+self.RENDER_JSON["mntMap"][key].replace('/','\\'))

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1)
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)

        self.G_ANALYSE_LOG.info('[config....]'+self.G_CONFIG)
        if os.path.exists(self.G_CONFIG):
            self.CGFILE=self.RENDER_JSON['common']["cgFile"]

            if isinstance(self.RENDER_JSON["mntMap"],dict):
                for key in self.RENDER_JSON["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd=cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+self.RENDER_JSON["mntMap"][key].replace('\\','/')+' '+key
                    self.G_ANALYSE_LOG.info(cmd)
                    self.RBcmd(cmd)

                    
        
    def RBexecute(self):#Render
        self.G_ANALYSE_LOG.info('[Houdini.RBexecute.start.....]')
        self.RBBackupPy()
        self.RBinitLog()
        self.RBmakeDir()
        if self.G_RENDEROS=='Linux':
            self.webMntPath()
        else:
            self.delSubst()
            self.webNetPath()
            
        self.RBprePy()
        self.RBcopyTempFile()#copy py.cfg max file
        self.RBreadCfg()
        self.RBhanFile()
        self.RBconfig()
        self.RBanalyse()
        self.RBpostPy()
        self.RBhanResult()
        self.G_ANALYSE_LOG.info('[Houdini.RBexecute.end.....]')