import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

class Maya(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MAYA.INIT"
		self.G_CHECKBAT_NAME='check.bat'
		self.G_CHECKMEL_NAME='checkNet.mel'
		self.G_PLUGINBAT_NAME='plugin.bat'
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Maya.RBhanFile.start.....]')

		scriptMayaPath=r'script\maya\new'
		checkBat=os.path.join(self.G_POOL,scriptMayaPath,self.G_CHECKBAT_NAME)
		checkMel=os.path.join(self.G_POOL,scriptMayaPath,self.G_CHECKMEL_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptMayaPath,self.G_PLUGINBAT_NAME)
		mayascript='c:/script/maya'
		
		copyScriptCmd1='xcopy /y /f "'+checkBat+'" "'+mayascript+'/" '
		copyScriptCmd2='xcopy /y /f "'+checkMel+'" "'+mayascript+'/" '
		copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+mayascript+'/" '
		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.G_ANALYSE_LOG.info('[Maya.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Maya.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.start.....]')
		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/maya.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		
		netFile = os.path.join(self.G_WORK_TASK,self.G_CG_TXTNAME)
		netFile=netFile.replace('\\','/')
		
		cgProject = self.G_PATH_INPUTROJECT.replace('\\','\\\\')
		cgFile=self.G_PATH_INPUTFILE.replace('\\','\\\\')
		
		analyseCmd='c:/script/maya/'+self.G_CHECKBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + mayaExePath+'" "'+cgProject + '" "' +cgFile+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBinitLog()
		self.RBmakeDir()
		self.RBprePy()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBconfig()
		
		self.RBanalyse()
		self.RBpostPy()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.end.....]')