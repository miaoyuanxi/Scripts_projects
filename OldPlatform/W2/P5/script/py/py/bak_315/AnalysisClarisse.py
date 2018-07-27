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
		if self.G_RENDEROS=='Linux':
			exePath=r'/usr/isotropix/'+self.CGSOFT[:-1]+'/clarisse_'+self.CGV+'/clarisse/cnode'
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
				resultLine = self.proc.stdout.readline().strip()
				if resultLine.startWith("<"):
					
						xFile.write(resultLine)
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
			self.CGV=configJson['common']["cgv"]
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
		cmd = 'python "B:\\plugins\\clarisee\\lib\\python\\Setupapps_win.py" "'+self.CGSOFT.replace("_"," ")+self.CGV +'"' 
		self.G_ANALYSE_LOG.info('[cmd....]'+cmd)
		self.RBcmd(cmd,False,1)
		
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
		self.createXml()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Clarisse.RBexecute.end.....]')