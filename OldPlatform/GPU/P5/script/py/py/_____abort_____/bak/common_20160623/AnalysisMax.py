import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import *

class Max(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "Max INIT"
		self.G_MAXBAT_NAME='max.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'		
		self.G_ANALYSEBAT_NAME='analyse.bat'
		self.G_SCRIPT_NAME='renderbus.ms'
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[MAX.RBhanFile.start.....]')

		scriptMaxPath=r'script\max\new'
		maxBat=os.path.join(self.G_POOL,scriptMaxPath,self.G_MAXBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptMaxPath,self.G_PLUGINBAT_NAME)
		analyseBat=os.path.join(self.G_POOL,scriptMaxPath,self.G_ANALYSEBAT_NAME)
		analyseMs=os.path.join(self.G_POOL,scriptMaxPath,self.G_SCRIPT_NAME)
		maxscript='c:/script/max'
		
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
		copyScriptCmd3='xcopy /y /f "'+analyseBat+'" "'+maxscript+'/" '
		copyScriptCmd4='xcopy /y /f "'+analyseMs+'" "'+maxscript+'/" '
		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.RBcmd(copyScriptCmd4)
		
		#copy max
		oldMax=os.path.join(self.G_WORK_TASK,os.path.basename(self.G_PATH_INPUTFILE))
		newMax=os.path.join(self.G_WORK_TASK,self.G_WORK_FILENAME)
		if os.path.exists(oldMax)==True:
			os.remove(oldMax)
		if os.path.exists(newMax)==True:
			os.remove(newMax)
		
		copyMaxcmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_PATH_INPUTFILE.replace('/','\\')+'" /to="'+self.G_WORK_TASK.replace('/','\\')+'"'
		self.RBcmd(copyMaxcmd)
		os.rename(oldMax,newMax)
		self.G_ANALYSE_LOG.info('[MAX.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[MAX.RBconfig.start.....]')
		#multicatter = getattr(self,'G_CG_MULTISCATTER_VERSION')
		if hasattr(self,'G_CG_MULTISCATTER_VERSION'):
			configMultCmd='c:/script/max/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' multiscatter ' +self.G_CG_MULTISCATTER_VERSION
			self.RBcmd(configMultCmd)
		self.G_ANALYSE_LOG.info('[MAX.RBconfig.end.....]')
		
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[MAX.RBanalyse.start.....]')
		newMax=os.path.join(self.G_WORK_TASK,self.G_WORK_FILENAME)		
		netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		cgFile=newMax.replace('\\','/')
		netFile=netFile.replace('\\','/')
		analyseCmd='c:/script/max/'+self.G_ANALYSEBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' "' +cgFile+'" "'+netFile+'" '
		print analyseCmd
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[MAX.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_ANALYSE_LOG.info('[MAX.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()		
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBconfig()
		self.RBanalyse()
		self.RBhanResult()
		self.RBpostPy()
		self.G_ANALYSE_LOG.info('[MAX.RBexecute.end.....]')

#---------------------calss max presub--------------------
class MaxPresub(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MaxPreSub INIT"
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBcopyTempFile.start.....]')		
		tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_presub'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[MaxPresub.RBcopyTempFile.end.....]')
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[MaxPresub.RBhanFile.start.....]')
		workTaskTemp=os.path.join(self.G_WORK_TASK,'temp')
		workTaskTempFull = os.path.join(self.G_WORK_TASK,'temp.full')
		fcopyCmd = 'c:\\fcopy\\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start /srcfile="'+self.G_FCOPY_FILELIST+'" /to="'+workTaskTemp.replace('/','\\')+'\\"'
		exdupeCmd='c:/exdupe.exe -t16f '+workTaskTemp +'\\ '+workTaskTempFull
		#delcmd='c:/fcopy/FastCopy.exe /cmd=delete /speed=full /force_close  /no_confirm_stop /no_confirm_del /force_start ' +self.G_POOL_TEMP_TEMP
		
		poolTempTask=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_RENDER_TASKID+'_render'))
		copyToPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+workTaskTempFull.replace('/','\\')+'" /to="'+poolTempTask.replace('/','\\')+'"'		
		self.RBcmd(fcopyCmd)
		self.RBcmd(exdupeCmd)
		self.RBcmd(copyToPoolCmd)
		
		#self.RBcmd(delcmd)
		self.G_ANALYSE_LOG.info('[MaxPresub.RBhanFile.end.....]')
		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBprePy()
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')
		
class MaxMergePic(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MaxMergePic INIT"
		self.G_MAXBAT_NAME='max.bat'
		self.G_MERGEPIC_SCRIPT_NAME='mergepic.ms'
		self.G_MERGEPIC_BAT_NAME='mergepic.bat'
		self.G_WORK_TASK_TEMP = os.path.join(self.G_WORK_TASK,'temp')
		self.G_WORK_TASK_RESULT=os.path.join(self.G_WORK_TASK,'result')
		
	def RBmakeDir(self):#1
		Base.RBmakeDir(self)
		print '[MaxMergePic.RBmakeDir.start.....]'
		
		#renderwork
		if not os.path.exists(self.G_WORK_TASK_TEMP):
			os.makedirs(self.G_WORK_TASK_TEMP)
			
		if not os.path.exists(self.G_WORK_TASK_RESULT):
			os.makedirs(self.G_WORK_TASK_RESULT)
		print '[BASE.RBmakeDir.end.....]'
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.start.....]')		
		tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_mergepic'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.end.....]')
		
	def RBhanFile(self):
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.start.....]')
		

		scriptMaxPath=r'script\max\new'
		maxBat=os.path.join(self.G_POOL,scriptMaxPath,self.G_MAXBAT_NAME)
		mergePicMs = os.path.join(self.G_POOL,scriptMaxPath,self.G_MERGEPIC_SCRIPT_NAME)
		mergePicBat = os.path.join(self.G_POOL,scriptMaxPath,self.G_MERGEPIC_BAT_NAME)
		
		maxscript='c:/script/max'		
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		copyScriptCmd2='xcopy /y /f "'+mergePicMs+'" "'+maxscript+'/" '
		copyScriptCmd3='xcopy /y /f "'+mergePicBat+'" "'+maxscript+'/" '
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		
		userOutput=os.path.join(self.G_PATH_USER_OUTPUT,'*.*')
		copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+userOutput.replace('/','\\')+'" /to="'+self.G_WORK_TASK_TEMP.replace('/','\\')+'"'
		self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.end.....]')
		
	def RBmergePic(self):
		scriptMaxPath=r'script\max\new'
		mergePicCmd='c:/script/max/'+self.G_MERGEPIC_BAT_NAME+' "'+self.G_CG_VERSION+'" "scanline" "'+  self.G_USERID+'" "'+self.G_TASKID +'" "'+ self.G_IMAGE_FRAME+'" "'+ self.G_IMAGE_WIDTH+'" "'+ self.G_IMAGE_HEIGHT+'" "'+self.G_WORK_TASK.replace('/','\\')+'//"'
		self.RBcmd(mergePicCmd,True,False)
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_WORK_TASK_RESULT.replace('/','\\')+'\\*.*" /to="'+self.G_PATH_USER_OUTPUT.replace('/','\\')+'"'
		self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')
		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBmergePic()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')

		
		
class MergePhoton(AnalysisBase):
	def __init__(self,**paramDict):
		AnalysisBase.__init__(self,**paramDict)
		print "MaxMergePic INIT"
		self.G_WORK_TASK_TEMP = os.path.join(self.G_WORK_TASK,'temp')
		self.G_WORK_TASK_RESULT=os.path.join(self.G_WORK_TASK,'result')
		
		
	def RBmakeDir(self):#1
		Base.RBmakeDir(self)
		print '[MaxMergePic.RBmakeDir.start.....]'
		
		#renderwork
		if not os.path.exists(self.G_WORK_TASK_TEMP):
			os.makedirs(self.G_WORK_TASK_TEMP)
			
		if not os.path.exists(self.G_WORK_TASK_RESULT):
			os.makedirs(self.G_WORK_TASK_RESULT)
		print '[BASE.RBmakeDir.end.....]'
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.start.....]')		
		tempFile=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_mergephoton'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.end.....]')
	

		
	
	def RBhanFile(self):
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.start.....]')
		
		
		imvPool=os.path.join(self.G_POOL,r'plugins\vray',self.G_CG_RENDER_VERSION,'imapviewer.exe')
		imvLocalPath=os.path.join(r'c:\plugins\vray',self.G_CG_RENDER_VERSION)
		copyImvCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+imvPool.replace('/','\\')+'" /to="'+imvLocalPath.replace('/','\\')+'"'
		self.RBcmd(copyImvCmd)
		
		#userOutput=os.path.join(self.G_PATH_USER_OUTPUT,'*.vrmap')
		#copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+userOutput.replace('/','\\')+'" /to="'+self.G_WORK_TASK_TEMP.replace('/','\\')+'"'
		#self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.end.....]')

		
	def RBmergePhoton(self):
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBmergePhoton.start.....]')
		fileList=os.listdir(self.G_WORK_TASK_TEMP)
		vrName=''
		for vrFileName in fileList:
			if vrFileName.endswith('.vrmap'):
				myLen=len(vrFileName)
				vrName=vrFileName[0:(myLen-10)]
				print vrName
				break
		print ("....."+vrName)
		imvCmd=os.path.join(r'c:\plugins\vray',self.G_CG_RENDER_VERSION,'imapviewer.exe')+' '
		resultVrmap=os.path.join(self.G_WORK_TASK_RESULT,(vrName+'.vrmap'))
		for myfile in os.listdir(self.G_WORK_TASK_TEMP): 
			path = os.path.join(self.G_WORK_TASK_TEMP, myfile)
			imvCmd=imvCmd+' -load '+path
		imvCmd=imvCmd+' -save '+resultVrmap+' -nodisplay'
		
		self.RBcmd(imvCmd,True,False)
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBmergePhoton.end.....]')
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		#inputProjectMap=os.path.join(self.G_PATH_INPUTPROJECT,(self.G_RENDER_TASKID+'_map'))
		
		renderTemp=os.path.join(self.G_POOL,'temp',(self.G_FATHERID+'_render'))
		copyCmd1='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_WORK_TASK_RESULT.replace('/','\\')+'\\*.*" /to="'+renderTemp.replace('/','\\')+'\\"'
		copyCmd2='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_WORK_TASK_RESULT.replace('/','\\')+'\\*.*" /to="'+self.G_PATH_USER_OUTPUT.replace('/','\\')+'\\"'
		self.RBcmd(copyCmd1)
		self.RBcmd(copyCmd2)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')

		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBBackupPy()
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBmergePhoton()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')