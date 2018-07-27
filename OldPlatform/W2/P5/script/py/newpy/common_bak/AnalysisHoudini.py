import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Houdini(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "Houdini.INIT"
		self.G_ANALYSEBAT_NAME='Eanalyz_HD.bat'
		#self.G_ANALYSECMD_NAME='nCZHoudini_Analysis.cmd'
		#self.G_ANALYSEPY_NAME='nCZHoudini_Analysis.py'
		self.CGV=''
		
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.start.....]')

		#scriptHoudiniPath=r'script\houdini\new'
		#analyseBat=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSEBAT_NAME)
		#analyseCmd=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSECMD_NAME)
		#analysePy=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSEPY_NAME)
		
		#houdiniScript='c:/script/houdini'
		#copyScriptCmd1='xcopy /y /f "'+analyseBat+'" "'+houdiniScript+'/" '
		#copyScriptCmd2='xcopy /y /f "'+analyseCmd+'" "'+houdiniScript+'/" '
		#copyScriptCmd3='xcopy /y /f "'+analysePy+'" "'+houdiniScript+'/" '
		
		#self.RBcmd(copyScriptCmd1)
		#self.RBcmd(copyScriptCmd2)
		#self.RBcmd(copyScriptCmd3)
		self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Houdini.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Houdini.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		#14.0.361
		
		analyseCmd=self.G_POOL+'\\script\\Houdini\\'+self.G_ANALYSEBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + self.CGV+'"  "' +self.CGFILE+'" "'+netFile+'" '
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
					mntPath =configJson["mntMap"][key]
					self.RBcmd("net use "+key+" "+mntPath.replace(self.inputIp,self.ip))
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Houdini.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
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