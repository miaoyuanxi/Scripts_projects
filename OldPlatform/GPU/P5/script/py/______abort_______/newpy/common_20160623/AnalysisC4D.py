import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class C4D(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "c4d.INIT"
		
		self.CGV=''
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[c4d.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[c4d.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[c4d.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[c4d.RBconfig.end.....]')

	def copyPyp(self):
		code="R13_05DFD2A0";
		if self.CGV=="R14":
			code="R14_4A9E4467"
		if self.CGV=="R15":
			code="R15_53857526"
		if self.CGV=="R16":
			code="R16_14AF56B1"
		if self.CGV=="R17":
			code="R17_8DE13DAD"
		path="C:\\users\\enfuzion\\AppData\\Roaming\\MAXON\\CINEMA 4D "+code+"\\plugins\\"
		source="B:\\plugins\\C4D\\script\\Analys.pyp"
		self.pythonCopy(source,path)

	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[c4d.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')

		myCgVersion = "CINEMA 4D "+self.CGV
		c4dbat='B:\plugins\C4D\script\C4D.bat'
		#14.0.361
		c4dExePath=os.path.join(r'C:\Program Files\MAXON',myCgVersion,'CINEMA 4D 64 Bit.exe')

		analyseCmd=c4dbat+' "'+myCgVersion+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[c4d.RBanalyse.end.....]')

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
					self.RBcmd("net use "+key+" "+configJson["mntMap"][key])
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[c4d.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.webNetPath()
		self.RBprePy()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBconfig()	
		self.copyPyp()	
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[c4d.RBexecute.end.....]')