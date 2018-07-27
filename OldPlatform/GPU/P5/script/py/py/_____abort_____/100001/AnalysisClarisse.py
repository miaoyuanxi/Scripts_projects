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

		myCgVersion = "Clarisse iFX "+self.CGV

		#14.0.361r'C:\Program Files\Isotropix\Clarisse iFX 3.0 RC3\Clarisse\cnode.exe
		exePath=os.path.join(r'C:\Program Files\Isotropix',myCgVersion,'Clarisse\cnode.exe')
		#analyseCmd=exePath + ' ' + self.clarisseFile + ' -info'
		#self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Clarisse.RBanalyse.exe.....]'+exePath)
		try:
			self.proc = subprocess.Popen([exePath, self.CGFILE, '-info'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)	
		except:
			print 'Run Analysis Failed!'
			sys.exit(-1)
		self.G_ANALYSE_LOG.info('[Clarisse.RBanalyse.end.....]')

	def createXml(self): 
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		try:
			if self.proc:
				with open(netFile, 'w') as xFile:
					xFile.write(self.proc.stdout.read())
		except:
			print "Generate XML Failed!"
			sys.exit(-1)

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
		self.G_ANALYSE_LOG.info('[Clarisse.RBexecute.start.....]')
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
		self.createXml()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Clarisse.RBexecute.end.....]')