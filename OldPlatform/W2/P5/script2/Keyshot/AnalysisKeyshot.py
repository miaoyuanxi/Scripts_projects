import os,sys,subprocess,string,logging,time,shutil
import logging
import codecs
from AnalysisBase import AnalysisBase
import json

class Keyshot(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[KeyShot.RBhanFile.start.....]')

		self.G_ANALYSE_LOG.info('[KeyShot.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[KeyShot.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[KeyShot.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.start.....]')

		#myCgVersion=self.cgName + self.cgv
		#exePath=os.path.join(r'D:\Program Files',myCgVersion,r'bin\keyshot6.exe')
		#scriptPath = "B:\\plugins\\KeyShot\\lib\\python\\ks_analy.py"

		#analyseCmd='"'+exePath+'" -script "'+scriptPath.replace("\\","/")+'" '
		mainPyCmd='C:\\Python34\\python.exe "B:\plugins\KeyShot\lib\python\KeyShotJob\JOBIN.py"'
		mainPyCmd += " function=Analyse"
		mainPyCmd += " task=%s"%str(self.G_TASKID)
		mainPyCmd += " log=C:/log/helper/%s/%s_analyse.log"%(self.G_TASKID,self.G_JOB_NAME)
		mainPyCmd += " soft=%s%s"%(self.cgName,self.cgv)

		self.G_ANALYSE_LOG.info('cmds: %s'%mainPyCmd)
		TL_result = subprocess.Popen(mainPyCmd,stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		TL_result.stdin.write('3/n')
		TL_result.stdin.write('4/n')
		writfilt = ["[pyout]",":","[C]","[W]","CPU feature level"]
		while TL_result.poll()==None:
			r_info = TL_result.stdout.readline().strip().strip("\n")
			if not r_info == "":
				if writfilt[1] in r_info and not writfilt[2] in r_info and not writfilt[3] in r_info:
					if writfilt[0] in r_info:
						r_info = r_info.replace(writfilt[0],"")
					inde = 0
					for i in xrange(len(r_info)):
						if ord(r_info[i])>32:
							inde=i
							break
					if inde:
						print(inde)
						r_info = r_info[inde:]
					self.G_ANALYSE_LOG.info(r_info.strip())

		r_code = TL_result.returncode
		self.G_ANALYSE_LOG.info("RenderCmd return:"+str(r_code))

		## self.RBcmd(mainPyCmd,True,False)
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.end.....]')

	def bulidFile(self):
		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.start.....]')
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		infoFolder = "D:\\KS\\"
		analyseFolder = "C:\\work\\render\\"+self.G_TASKID+"\\KS\\"
		infoPath = infoFolder+"INFO.txt"

		if not os.path.exists(infoFolder):
			os.mkdir(infoFolder)

		if not os.path.exists(analyseFolder):
			os.makedirs(analyseFolder)

		if os.path.exists(infoPath):
			os.remove(infoPath)

		AnalyseFilePath = analyseFolder+"FilePath.txt"
		info=codecs.open(infoPath,'w')
		AnalyseFile=codecs.open(AnalyseFilePath,'w')
		try :
			info.write(self.G_TASKID.encode("UTF-8"))
			AnalyseFile.write(self.CGFILE.encode("UTF-8")+"\n")
			AnalyseFile.write(netFile.encode("UTF-8"))
		finally :
			info.close()
			AnalyseFile.close()

		self.G_ANALYSE_LOG.info('[KeyShot.RBanalyse.end.....]')

	def EXJsonFile(self):
		self.G_ANALYSE_LOG.info('[KeyShot.EXJsonFile.start.....]')
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		analyseFolder = self.G_WORK_TASK+"\\KS\\"
		AnalyseFilePath = analyseFolder+"renderinfo.json"

		if not os.path.exists(analyseFolder):
			os.makedirs(analyseFolder)

		## AnalyseFile=codecs.open(AnalyseFilePath,'w')
		_info_adict = {"IOs":[self.CGFILE,netFile]}
		try :
			with open(AnalyseFilePath,"w")as f:
				json.dump(_info_adict,f)
				f.close()
			## AnalyseFile.write(self.CGFILE.encode("UTF-8")+"\n")
			## AnalyseFile.write(netFile.encode("UTF-8"))
		finally :
			print("Writ IOs info failed!")
			##AnalyseFile.close()

		self.G_ANALYSE_LOG.info('[KeyShot.EXJsonFile.end.....]')

	def plugin(self):
		self.G_ANALYSE_LOG.info('[self.G_PLUGINS.....]'+self.G_PLUGINS)
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
			delCmd='B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "del"'
			self.RBcmd(delCmd,True,False)
			if isinstance(configJson["plugins"],dict):
				for key in configJson["plugins"]:
					cmd = 'B:\\plugins\\Sketchup\\script\\plugin.bat "'+myCgVersion+'" "'+key+'" "'+key+configJson["plugins"][key]+'"'
					self.RBcmd(cmd,True,False)
					self.G_ANALYSE_LOG.info(cmd)

	def webNetPath(self):
		self.G_ANALYSE_LOG.info("WebNetPath\n")
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			self.cgv=configJson['common']["cgv"]
			self.cgName=configJson['common']["cgSoftName"]
			self.CGFILE=configJson['common']["cgFile"]
			print configJson
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:

					# self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
					cmds = 'net use %s "%s"'%(key,configJson["mntMap"][key].replace('/','\\'))
					self.RBcmd(cmds)
					self.G_ANALYSE_LOG.info(cmds)

	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[KeyShot.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.delSubst()
		self.webNetPath()
		self.RBprePy()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		## self.bulidFile()
		self.EXJsonFile()
		#self.plugin()
		self.RBconfig()
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[KeyShot.RBexecute.end.....]')