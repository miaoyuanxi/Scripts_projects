import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Houdini(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "Houdini.INIT"
        self.G_ANALYSEBAT_NAME='Enalyze.py'
        self.G_DRIVERC_7Z='c:/7-Zip/7z.exe'
        self.CGV=''
        print "sys.path"+str(sys.path)
        
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.start.....]')

        self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.end.....]')
        
    def RBconfig(self):#5
        self.G_ANALYSE_LOG.info('[Houdini.RBconfig.start.....]')
        self.G_ANALYSE_LOG.info('[Houdini.RBconfig.end.....]')
    
    def RBanalyse(self):#7
        
        
        # ADD BY CHENZHONG
        os.environ['CID_INPUT_ROOT'] = self.INPUTPROJECT
        os.environ['TID_OUTPUT_ROOT'] = self.USEROUTPUTPATH
        # ADD BY CHENZHONG
        
        
        self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.start.....]')
        python_used = "C:/Python27/python.exe"
        analysePath = python_used+' B:\\plugins\\houdini\\Enalyze.py'

        ##-----------------------------------------------------------------
        ## Edit by shen, RS render 
        _RS_render = True
        if not self.G_RENDEROS=='Linux':
            json_path = r"B:\plugins\houdini\lib"
            sys.path.append(json_path)
            import dojson
            if os.path.exists("D:/work/helper/%s" % self.G_TASKID):
                p_info = dojson.main(self.G_TASKID,'helper')
                if len(p_info):
                    if p_info[0] == "RS":
                        _RS_render = True

        ##-----------------------------------------------------------------

        netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
        netFile=netFile.replace('\\','/')
        _log_file = "C:/log/helper/%s/%s_analyse.log"%(self.G_TASKID,self.G_JOB_NAME)
        if _RS_render:
            analysePath = python_used + ' B:\\plugins\\houdini\\bin\\RSLogin.py'
            analyseCmd=analysePath+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '+_log_file+' Analyse'
            self.G_ANALYSE_LOG.info("Input: %s"%self.INPUTPROJECT)
            self.G_ANALYSE_LOG.info("Output: %s"%self.USEROUTPUTPATH)
            self.G_ANALYSE_LOG.info("RS_Cmds: %s"%analyseCmd)
        else:
            #analyseCmd='c:\\Python27\\python.exe'+' B:\\plugins\houdini\\'+self.G_ANALYSEBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '
            if self.G_RENDEROS=='Linux':
                analysePath='/B/plugins/houdini/Linux/Enalyze.sh'
            analyseCmd=analysePath+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" "'+self.INPUTPROJECT+'" "'+self.USEROUTPUTPATH+'" '
            self.G_ANALYSE_LOG.info("Cmds: %s"%analyseCmd)

        ## if self.G_RENDEROS=='Linux':
            ## self.RBcmd(analyseCmd,True,1)
        _Runing = 1
        if _Runing:
            #analyseCmd=analysePath+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" "'+self.INPUTPROJECT+'" "'+self.USEROUTPUTPATH+'" '
            ## ------------------------------------------------------------------------------------

            TL_result = subprocess.Popen(analyseCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            TL_result.stdin.write('3/n')
            TL_result.stdin.write('4/n')
            r_err = ''
            while TL_result.poll()==None:
                r_info = TL_result.stdout.readline().strip()
                if not r_info == "":
                    self.G_ANALYSE_LOG.info(r_info)
                    r_err = r_info
            #r_result = TL_result.wait()
            r_code = TL_result.returncode
            self.G_ANALYSE_LOG.info("AnalyseCmd return:"+str(r_code))
            if r_code:
                self.G_ANALYSE_LOG.info("Error Print :")
                self.G_ANALYSE_LOG.info("\n"+r_err+"\n")
            ## ----------------------------------------------------------------------------------

        self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.end.....]')

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=""#configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            self.INPUTPROJECT=configJson['common']['inputProject']
            self.USEROUTPUTPATH=configJson['common']['userOutputPath']
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y")
                for key in configJson["mntMap"]:
                    # self.RBcmd("net use "+key+" "+"\""+configJson["mntMap"][key].replace('/','\\')+"\"")
                    mnt_value = configJson["mntMap"][key].replace('/','\\')
                    if os.path.exists(mnt_value):
                        self.RBcmd("net use "+key+" "+"\""+mnt_value+"\"")
                    else:
                        self.G_ANALYSE_LOG.info('[warn]The path is not exist:%s' % mnt_value)

    def webMntPath(self):
        # mountFrom='{"Z:":"//192.168.0.94/d"}'
        mtabCmd='rm -f /etc/mtab~*'
        self.RBcmd(mtabCmd,False,1)
        exitcode = subprocess.call("mount | grep -v '/mnt_rayvision' | awk '/cifs/ {print $3} ' | xargs umount", shell=1)
        if exitcode not in(0,123):
            sys.exit(exitcode)

        self.G_ANALYSE_LOG.info('[config....]'+self.G_CONFIG)
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.INPUTPROJECT=configJson['common']['inputProject']
            self.USEROUTPUTPATH=configJson['common']['userOutputPath']
            print configJson
            if isinstance(configJson["mntMap"],dict):
                for key in configJson["mntMap"]:
                    if not os.path.exists(key):
                        os.makedirs(key)
                    cmd=cmd='mount -t cifs -o username=enfuzion,password=ruiyun2016,codepage=936,iocharset=gb2312 '+configJson["mntMap"][key].replace('\\','/')+' '+key
                    # self.G_ANALYSE_LOG.info(cmd)
                    self.RBcmd(cmd)


    def copyHoudiniFile(self):
        cgvName =self.CGV.replace(".","")
        pluginPath="B:\\plugins\\houdini\\apps\\7z\\"+cgvName+".7z"
        localPath = "D:\\plugins\\houdini\\";
        localPluginPath=""
        if not os.path.exists(localPath+cgvName+"\\") or not os.listdir(localPath+cgvName+"\\"):
            if not os.path.exists(localPath+cgvName+".7z"):
                copyCmd = 'c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +pluginPath +'" /to="'+localPath+'"'
                self.RBcmd(copyCmd)

            unpackCmd=self.G_DRIVERC_7Z+' x "'+localPath+cgvName+".7z"+'" -y -aos -o"'+localPath+cgvName+'\\"' 
            self.RBcmd(unpackCmd)
        
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
        #self.copyHoudiniFile()
        self.RBprePy()
        self.RBcopyTempFile()#copy py.cfg max file
        self.RBreadCfg()
        self.RBhanFile()
        self.RBconfig()		
        self.RBanalyse()
        self.RBpostPy()
        self.RBhanResult()
        self.G_ANALYSE_LOG.info('[Houdini.RBexecute.end.....]')