import os,sys,subprocess,string,logging,time

import logging

class Base():

	def __init__(self,**paramDict):
		print '[BASE.init.start.....]'
		
		self.G_DOPY_NAME='do.py'
		
		self.G_USERID=paramDict['G_USERID']
		self.G_USERID_PARENT=paramDict['G_USERID_PARENT']
		self.G_TASKID=paramDict['G_TASKID']
		self.G_POOL=paramDict['G_POOL']

		self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
		self.G_JOB_NAME=self.G_SYS_ARGVS[3]
		self.G_NODE_NAME=self.G_SYS_ARGVS[5]
		
		self.G_LOG_WORK='C:/LOG/analyse'
		self.G_ANALYSE_WORK='C:/WORK/analyse'
		
		self.G_ANALYSE_WORK_TASK=os.path.join(self.G_ANALYSE_WORK,self.G_TASKID)
		self.G_WORK_TASK_CFG=os.path.join(self.G_ANALYSE_WORK_TASK,'cfg')
		self.G_CFG_PY=os.path.join(self.G_WORK_TASK_CFG,'py.cfg')
		self.G_PRE_PY=os.path.join(self.G_WORK_TASK_CFG,'pre.py')
		self.G_POST_PY=os.path.join(self.G_WORK_TASK_CFG,'post.py')
		
		#log
		self.G_ANALYSE_LOG=logging.getLogger('analyseLog')
		
		'''
		G_KG=0
		G_CG_VERSION='3ds Max 2012'
		G_CG_RENDER_VERSION='vray2.10.01'
		G_CG_MULTISCATTER_VERSION='multiscatter1.1.07a'
		G_PATH_INPUTFILE
		G_CG_PROJECT
		G_WORK_FILENAME='310239.max'
		G_CG_TXTNAME='fdfdabc_max'
		G_PATH_SMALL=r'\\10.50.10.5\d\outputData\small'
		G_PATH_USER_OUTPUT=r'\\10.50.10.5\d\outputData'
		G_PATH_COST=r'\\10.50.10.5\d\transfer\txt\test'
		G_SINGLE_FRAME_CHECK='singleFrameCheck.exe'
		'''
		print '[BASE.init.end.....]'

	def RBBackupPy(self):
		print '[BASE.RBBackupPy.start.....]'
		runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
		tempRunPy=os.path.join(runPyPath,runPyName)
		
		copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_WORK_TASK_CFG+'/" '
		workTaskRunPy=os.path.join(self.G_WORK_TASK_CFG,runPyName)
		runBatName=os.path.basename(runPyName)+'.bat'
		runBat=os.path.join(self.G_WORK_TASK_CFG,runBatName)
		fileHandle=open(runBat,'a')
		fileHandle.write('c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5])+'"'
		fileHandle.close()
		print '[BASE.RBBackupPy.end.....]'
			
	def RBmakeDir(self):#1
		print '[BASE.RBmakeDir.start.....]'
					
		#renderwork
		if not os.path.exists(self.G_ANALYSE_WORK_TASK):
			os.makedirs(self.G_ANALYSE_WORK_TASK)
		print '[BASE.RBmakeDir.end.....]'	
			
	def RBinitLog(self):#2
		print '[BASE.RBinitLog.start.....]'
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		analyseLogPath = os.path.join(self.G_LOG_WORK,self.G_TASKID)
		analyseLog=os.path.join(analyseLogPath,(self.G_JOB_NAME+'.txt'))
		if not os.path.exists(analyseLogPath):
			os.makedirs(analyseLogPath)
		self.G_ANALYSE_LOG.setLevel(logging.DEBUG)
		renderLogHandler=logging.FileHandler(analyseLog)
		renderLogHandler.setFormatter(fm)
		self.G_ANALYSE_LOG.addHandler(renderLogHandler)
		console = logging.StreamHandler()  
		console.setLevel(logging.INFO)  
		self.G_ANALYSE_LOG.addHandler(console)		
		print '[BASE.RBinitLog.end.....]'
		

		
	def RBprePy(self):#pre custom
		self.G_ANALYSE_LOG.info('[BASE.RBprePy.start.....]')	
		if os.path.exists(self.G_PRE_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			execfile(self.G_PRE_PY)
		self.G_ANALYSE_LOG.info('[BASE.RBprePy.end.....]')
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[BASE.RBhanFile.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBhanFile.end.....]')
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.start.....]')		
		tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_analyse'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.end.....]')	
	
	def RBreadCfg(self):#4
		self.G_ANALYSE_LOG.info('[BASE.RBreadCfg.start.....]')		
		txtFile=open(self.G_CFG_PY, 'r')
		allLines=txtFile.readlines()

		for eachLine in allLines:
			if eachLine.startswith('#') or eachLine=='\n':
				continue
			execStr='self.'+eachLine.strip()
			print execStr
			exec(execStr)
		self.G_ANALYSE_LOG.info('[BASE.RBreadCfg.end.....]')
			
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[BASE.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[BASE.RBanalyse.start.....]')
		self.G_ANALYSE_LOG.info('[BASE.RBanalyse.end.....]')
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		errFile = os.path.join(self.G_ANALYSE_WORK_TASK,(self.G_CG_TXTNAME+'_err.txt'))
		
		if  os.path.exists(netFile) and (not os.path.exists(errFile)):#copy ok
			copyCmd='xcopy /y /f "'+netFile+'" "'+self.G_PATH_INPUTTXT+'\\" '
			self.RBcmd(copyCmd)
		else:
			#error
			sys.exit(-1)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')

	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		self.G_ANALYSE_LOG.info(cmdStr)
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			if resultLine!='':
				self.G_ANALYSE_LOG.info(resultLine)
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		self.G_ANALYSE_LOG.info('resultStr...'+resultStr)
		self.G_ANALYSE_LOG.info('resultCode...'+str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(resultCode)
		return resultStr
	
	def RBpostPy(self):#post custom
		self.G_ANALYSE_LOG.info('[BASE.RBpostPy.start.....]')
		if os.path.exists(self.G_POST_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			execfile(self.G_POST_PY)
		self.G_ANALYSE_LOG.info('[BASE.RBpostPy.end.....]')
		
	def RBexecute(self):#total
		print 'BASE.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_ANALYSE_LOG.info('[BASE.RBexecute.start.....]')
		self.RBprePy()		
		self.RBmakeDir()	
		self.RBcopyTempFile()
		self.RBreadCfg()		
		self.RBhanFile()
		self.RBconfig()		
		self.RBanalyse()
		self.RBhanResult()		
		self.RBpostPy()
		self.G_ANALYSE_LOG.info('[BASE.RBexecute.end.....]')
		

#---------------------calss max--------------------
class Max(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
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
		oldMax=os.path.join(self.G_ANALYSE_WORK_TASK,os.path.basename(self.G_PATH_INPUTFILE))
		newMax=os.path.join(self.G_ANALYSE_WORK_TASK,self.G_WORK_FILENAME)
		if os.path.exists(oldMax)==True:
			os.remove(oldMax)
		if os.path.exists(newMax)==True:
			os.remove(newMax)
		
		copyMaxcmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_PATH_INPUTFILE.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'
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
		newMax=os.path.join(self.G_ANALYSE_WORK_TASK,self.G_WORK_FILENAME)		
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		cgFile=newMax.replace('\\','/')
		netFile=netFile.replace('\\','/')
		analyseCmd='c:/script/max/'+self.G_ANALYSEBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' "' +cgFile+'" "'+netFile+'" '
		print analyseCmd
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[MAX.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
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
class MaxPresub(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "MaxPreSub INIT"
	
	def RBcopyTempFile(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBcopyTempFile.start.....]')		
		tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_presub'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[MaxPresub.RBcopyTempFile.end.....]')
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[MaxPresub.RBhanFile.start.....]')
		
		fcopyCmd = 'c:\\fcopy\\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start /srcfile="'+self.G_FCOPY_FILELIST+'" /to="'+self.G_POOL_TEMP_TEMP+'\\"'
		exdupeCmd='c:/exdupe.exe -t16f '+self.G_POOL_TEMP_TEMP +'\\ '+self.G_TEMP_FULL
		delcmd='c:/fcopy/FastCopy.exe /cmd=delete /speed=full /force_close  /no_confirm_stop /no_confirm_del /force_start ' +self.G_POOL_TEMP_TEMP
		
		self.RBcmd(fcopyCmd)
		self.RBcmd(exdupeCmd)
		self.RBcmd(delcmd)
		self.G_ANALYSE_LOG.info('[MaxPresub.RBhanFile.end.....]')
		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')
		
class MaxMergePic(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "MaxMergePic INIT"
		self.G_MAXBAT_NAME='max.bat'
		self.G_MERGEPIC_SCRIPT_NAME='mergepic.ms'
		self.G_MERGEPIC_BAT_NAME='mergepic.bat'
		self.G_WORK_TASK_TEMP = os.path.join(self.G_ANALYSE_WORK_TASK,'temp')
		self.G_WORK_TASK_RESULT=os.path.join(self.G_ANALYSE_WORK_TASK,'result')
		
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
		tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_mergepic'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'		
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
		mergePicCmd='c:/script/max/'+self.G_MERGEPIC_BAT_NAME+' "'+self.G_CG_VERSION+'" "scanline" "'+  self.G_USERID+'" "'+self.G_TASKID +'" "'+ self.G_IMAGE_FRAME+'" "'+ self.G_IMAGE_WIDTH+'" "'+ self.G_IMAGE_HEIGHT+'" "'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'//"'
		self.RBcmd(mergePicCmd,True,False)
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_WORK_TASK_RESULT.replace('/','\\')+'\\*.*" /to="'+self.G_PATH_USER_OUTPUT.replace('/','\\')+'"'
		self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')
		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBmergePic()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')

		
		
class MaxMergePhoton(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "MaxMergePic INIT"
		self.G_WORK_TASK_TEMP = os.path.join(self.G_ANALYSE_WORK_TASK,'temp')
		self.G_WORK_TASK_RESULT=os.path.join(self.G_ANALYSE_WORK_TASK,'result')
		
		
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
		tempFile=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_mergepic'),'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBcopyTempFile.end.....]')
	

		
	
	def RBhanFile(self):
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.start.....]')
		
		
		imvPool=os.path.join(self.G_POOL,r'plugins\vray',self.G_CG_RENDER_VERSION,'imapviewer.exe')
		imvLocalPath=os.path.join(r'c:\plugins\vray',self.G_CG_RENDER_VERSION)
		copyImvCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+imvPool.replace('/','\\')+'" /to="'+imvLocalPath.replace('/','\\')+'"'
		self.RBcmd(copyImvCmd)
		
		userOutput=os.path.join(self.G_PATH_USER_OUTPUT,'*.vrmap')
		copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+userOutput.replace('/','\\')+'" /to="'+self.G_WORK_TASK_TEMP.replace('/','\\')+'"'
		self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[MaxMergePic.RBhanFile.end.....]')
		
	def RBmergePhoton(self):
		imvCmd=os.path.join(r'c:\plugins\vray',self.G_CG_RENDER_VERSION,'imapviewer.exe')+' '
		resultVrmap=os.path.join(slef.G_WORK_TASK_RESULT,(self.G_VRMAP_NAME+'.vrmap'))
		for myfile in os.listdir(self.G_WORK_TASK_TEMP): 
			path = os.path.join(self.G_WORK_TASK_TEMP, myfile)
			imvCmd=imvCmd+' -load '+path
		imvCmd=imvCmd+' -save '+resultVrmap+' -nodisplay'
		
		self.RBcmd(imvCmd,True,False)
		
		
	def RBhanResult(self):#8
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.start.....]')
		copyCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+self.G_WORK_TASK_RESULT.replace('/','\\')+'\\*.*" /to="'+self.G_PATH_USER_OUTPUT.replace('/','\\')+'"'
		self.RBcmd(copyCmd)
		self.G_ANALYSE_LOG.info('[BASE.RBhanResult.end.....]')

		
	def RBexecute(self):
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.start.....]')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBcopyTempFile()#copy py.cfg max file
		self.RBreadCfg()
		self.RBhanFile()
		self.RBmergePhoton()
		self.RBhanResult()
		self.G_ANALYSE_LOG.info('[MaxPresub.RBexecute.end.....]')

#---------------------calss maya--------------------		
class Maya(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
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
		
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,self.G_CG_TXTNAME)
		netFile=netFile.replace('\\','/')
		
		cgProject = self.G_PATH_INPUTROJECT.replace('\\','\\\\')
		cgFile=self.G_PATH_INPUTFILE.replace('\\','\\\\')
		
		analyseCmd='c:/script/maya/'+self.G_CHECKBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + mayaExePath+'" "'+cgProject + '" "' +cgFile+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Maya.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Maya.RBexecute.start.....]')
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

		
		

#---------------------calss Houdini--------------------		
class Houdini(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "Houdini.INIT"
		self.G_ANALYSEBAT_NAME='nCZHoudini_Analysis.bat'
		self.G_ANALYSECMD_NAME='nCZHoudini_Analysis.cmd'
		self.G_ANALYSEPY_NAME='nCZHoudini_Analysis.py'
		
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.start.....]')

		scriptHoudiniPath=r'script\houdini\new'
		analyseBat=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSEBAT_NAME)
		analyseCmd=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSECMD_NAME)
		analysePy=os.path.join(self.G_POOL,scriptHoudiniPath,self.G_ANALYSEPY_NAME)
		
		houdiniScript='c:/script/houdini'
		copyScriptCmd1='xcopy /y /f "'+analyseBat+'" "'+houdiniScript+'/" '
		copyScriptCmd2='xcopy /y /f "'+analyseCmd+'" "'+houdiniScript+'/" '
		copyScriptCmd3='xcopy /y /f "'+analysePy+'" "'+houdiniScript+'/" '
		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.G_ANALYSE_LOG.info('[Houdini.RBhanFile.end.....]')
		
	def RBconfig(self):#5
		self.G_ANALYSE_LOG.info('[Houdini.RBconfig.start.....]')
		self.G_ANALYSE_LOG.info('[Houdini.RBconfig.end.....]')
	
	def RBanalyse(self):#7
		self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.start.....]')
		
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
		netFile=netFile.replace('\\','/')
		
		analyseCmd='c:/script/Houdini/'+self.G_ANALYSEBAT_NAME+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "' + self.G_CG_VERSION+'"  "' +self.G_PATH_INPUTFILE+'" "'+netFile+'" '
		self.RBcmd(analyseCmd,True,False)
		self.G_ANALYSE_LOG.info('[Houdini.RBanalyse.end.....]')
		
	def RBexecute(self):#Render
		self.G_ANALYSE_LOG.info('[Houdini.RBexecute.start.....]')
		
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
		self.G_ANALYSE_LOG.info('[Houdini.RBexecute.end.....]')
		
#-----------------------Render----------------------------------------
class AnalyseAction():
	def __init__(self,**paramDict):
		cgName=paramDict['G_CG_NAME']
		print 'cgName=================='+cgName
		exec('AnalyseAction.__bases__=('+cgName+',)')
		exec(cgName+'.__init__(self,**paramDict)')
	'''
	def RBrender(self):#Render command
		print 'AnalyseAction..max...render....'
	'''
#-----------------------main-------------------------------
def main(**paramDict):
	analyse=AnalyseAction(**paramDict)
	print 'G_POOL_NAME___'+analyse.G_POOL
	analyse.RBexecute()