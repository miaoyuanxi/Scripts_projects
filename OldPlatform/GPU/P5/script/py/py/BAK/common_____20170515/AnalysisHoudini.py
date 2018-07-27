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
		self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		#14.0.361
		
		#analyseCmd='c:\\Python27\\python.exe'+' B:\\plugins\houdini\\'+self.G_ANALYSEBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '
		analyseCmd='B:\\plugins\\houdini\\Enalyze.bat "'+self.G_USERID+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.end.....]')

	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.CGFILE=configJson['common']["cgFile"]
			self.CGSOFT=configJson['common']["cgSoftName"]
			self.CGV=configJson['common']["cgv"]
			self.RTASKID=configJson['common']["taskId"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))

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