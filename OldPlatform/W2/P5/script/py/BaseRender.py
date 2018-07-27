import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import codecs

class Base():

	def __init__(self,**paramDict):
		print 'Base.init...-------------------'
		
		self.G_LOG_WORK='C:/log/render'
		self.G_RENDER_WORK='C:/work/render'
		self.G_CFG_PY_NAME='py.cfg'
		self.G_CONVERTVBS_NAME='convertNew.vbs'
		self.G_PRE_PYNAME='pre.py'
		self.G_POST_PYNAME='post.py'
		
		self.G_USERID=paramDict['G_USERID']
		self.G_USERID_PARENT=paramDict['G_USERID_PARENT']
		self.G_TASKID=paramDict['G_TASKID']
		self.G_POOL=paramDict['G_POOL']
		
		self.G_CG_START_FRAME=paramDict['G_CG_START_FRAME']
		self.G_CG_END_FRAME=paramDict['G_CG_END_FRAME']
		self.G_CG_BY_FRAME=paramDict['G_CG_BY_FRAME']
		self.G_CG_LAYER_NAME=paramDict['G_CG_LAYER_NAME']
		self.G_CG_OPTION=paramDict['G_CG_OPTION']

		self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
		self.G_JOB_NAME=self.G_SYS_ARGVS[3]
		self.G_NODE_NAME=self.G_SYS_ARGVS[5]
		
		#self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',self.G_USERID_PARENT,self.G_USERID,(self.G_TASKID+'_render'))
		self.G_POOL_TASK=os.path.join(self.G_POOL,'temp',(self.G_TASKID+'_render'))
		
		self.G_RENDER_WORK_TASK=os.path.join(self.G_RENDER_WORK,self.G_TASKID)
		self.G_RENDER_WORK_TASK_CFG=os.path.join(self.G_RENDER_WORK,self.G_TASKID,'CFG')
		self.G_CFG_PYNAME=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_CFG_PY_NAME)#c:/renderwork/12343/renderbus/render.txt
		
		self.G_PRE_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_PRE_PYNAME)
		self.G_PRE_PY=self.G_PRE_PY.replace('\\','/')
		self.G_POST_PY=os.path.join(self.G_RENDER_WORK_TASK_CFG,self.G_POST_PYNAME)
		self.G_POST_PY=self.G_POST_PY.replace('\\','/')
		#log
		self.G_RENDER_LOG=logging.getLogger('renderLog')
		self.G_FEE_LOG=logging.getLogger('feeLog')
		
		self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK_TASK,'output')
		self.G_RENDER_WORK_OUTPUTBAK = os.path.join(self.G_RENDER_WORK_TASK,'outputbak')
		'''
		try:
			os.system('xcopy /y /v /f  "\\\\10.50.1.3\\p\\script\\py\\cleanNode.py" "c:/script/py/"')
			os.system('c:/python27/python.exe c:/script/py/cleanNode.py')
		except:
			print 'cleanNode Error'		
		'''
	def RBBackupPy(self): #
		print '[BASE.RBBackupPy.start.....]'
		# runPyPath = C:\agent\tmp\,runPyName= script_2014060400007_4
		runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
		tempRunPy=os.path.join(runPyPath,runPyName)
		if not os.path.exists(self.G_RENDER_WORK_TASK_CFG):
			os.makedirs(self.G_RENDER_WORK_TASK_CFG)
		workTaskRunPy=os.path.join(self.G_RENDER_WORK_TASK_CFG,runPyName)
		if not os.path.exists(workTaskRunPy):
			shutil.copyfile(tempRunPy,workTaskRunPy)
		#copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_RENDER_WORK_TASK_CFG+'/" '
		
		print '-----------===-----------------'
		print self.G_SYS_ARGVS
		for arg in self.G_SYS_ARGVS:
			print '------'+arg
		runBatName=os.path.basename(runPyName)+'.bat'
		runBat=os.path.join(self.G_RENDER_WORK_TASK_CFG,runBatName)
		#if  os.path.exists(runBat):
		#	os.remove(runBat)
		fileHandle=open(runBat,'w')
		batCmd='c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5]+'"'
		fileHandle.write(batCmd)
		fileHandle.close()
		print '[BASE.RBBackupPy.end.....]'
		
	def RBinitLog(self):#2
		renderLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
		if not os.path.exists(renderLogDir):
			os.makedirs(renderLogDir)
			
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		#feeFm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		renderLogPath=os.path.join(renderLogDir,(self.G_JOB_NAME+'.txt'))
		self.G_RENDER_LOG.setLevel(logging.DEBUG)
		renderLogHandler=logging.FileHandler(renderLogPath)
		renderLogHandler.setFormatter(fm)
		self.G_RENDER_LOG.addHandler(renderLogHandler)
		console = logging.StreamHandler()  
		console.setLevel(logging.INFO)  
		self.G_RENDER_LOG.addHandler(console)
		
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		self.G_FEE_LOG.setLevel(logging.DEBUG)
		if not os.path.exists(self.G_RENDER_WORK_TASK):
			os.makedirs(self.G_RENDER_WORK_TASK)
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		feeLogHandler=logging.FileHandler(feeTxt)
		#feeLogHandler.setFormatter(fm)
		self.G_FEE_LOG.addHandler(feeLogHandler)		
	
	def RBprePy(self):#pre custom
		self.G_RENDER_LOG.info('[BASE.RBprePy.start.....]')
		self.G_RENDER_LOG.info(self.G_PRE_PY)
		if os.path.exists(self.G_PRE_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			#execfile(self.G_PRE_PY)
			os.system('c:/python27/python.exe ' + self.G_PRE_PY)
		self.G_RENDER_LOG.info('[BASE.RBprePy.end.....]')
		
			
	def RBmakeDir(self):#1
		self.G_RENDER_LOG.info('[BASE.RBmakeDir.start.....]')
		
		#renderwork
		if not os.path.exists(self.G_RENDER_WORK_TASK):
			os.makedirs(self.G_RENDER_WORK_TASK)
		
		#renderwork/output
		if not os.path.exists(self.G_RENDER_WORK_OUTPUT):
			os.makedirs(self.G_RENDER_WORK_OUTPUT)
			
		#renderwork/outputbak
		if not os.path.exists(self.G_RENDER_WORK_OUTPUTBAK):
			os.makedirs(self.G_RENDER_WORK_OUTPUTBAK)

		#RB_small
		rbSamll = os.path.join(self.G_RENDER_WORK,self.G_TASKID,'RB_small')
		if not os.path.exists(rbSamll):
			os.makedirs(rbSamll)
		self.G_RENDER_LOG.info('[BASE.RBmakeDir.end.....]')
			
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[BASE.RBhanFile.start.....]')
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		self.RBcmd(copyVBSCmd)
		#"c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start C:\enfwork\\212869\output\*.*  /to=C:\enfwork\\212869\outputbak"
		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		self.G_RENDER_LOG.info('[BASE.RBhanFile.end.....]')
	
	def RBcopyTempFile(self):
		self.G_RENDER_LOG.info('[BASE.RBcopyTempFile.start.....]')
		#copy temp file
		#if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		tempFull=os.path.join(self.G_POOL_TASK,'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
		self.RBcmd(copyPoolCmd)
		echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
		self.RBcmd(echoCmd,False,True)
		self.G_RENDER_LOG.info('[BASE.RBcopyTempFile.end.....]')
			
	def RBreadCfg(self):#4
		self.G_RENDER_LOG.info('[BASE.RBreadCfg.start.....]')
	
		renderTxt=self.G_CFG_PYNAME
		txtFile=open(renderTxt, 'r')
		allLines=txtFile.readlines()
		for eachLine in allLines:
			if eachLine.startswith('#') or eachLine=='\n':
				continue
			execStr='self.'+eachLine.strip()
			print execStr
			exec(execStr)
		self.G_RENDER_LOG.info('[BASE.RBreadCfg.end.....]')			
			
	def RBrenderConfig(self):#5
		self.G_RENDER_LOG.info('[BASE.RBrenderConfig.start.....]')
		self.G_RENDER_LOG.info('[BASE.RBrenderConfig.end.....]')		
		
	def RBwriteConsumeTxt(self):#6
		self.G_RENDER_LOG.info('[BASE.RBwriteConsumeTxt.start.....]')
		self.G_FEE_LOG.info('zone='+self.G_ZONE)
		self.G_FEE_LOG.info('nodeName='+self.G_NODE_NAME)
		if hasattr(self,'G_FIRST_FRAME'):
			self.G_FEE_LOG.info('firstFrame='+self.G_FIRST_FRAME)
		self.G_FEE_LOG.info('frames='+self.G_CG_START_FRAME)
		self.G_RENDER_LOG.info('[BASE.RBwriteConsumeTxt.end.....]')
		
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[BASE.RBrender.start.....]')
		self.G_RENDER_LOG.info('[BASE.RBrender.end.....]')
	
	def RBpostPy(self):#pre custom
		self.G_RENDER_LOG.info('[BASE.RBpostPy.start.....]')
		if os.path.exists(self.G_POST_PY):
			sys.argv=[self.G_USERID,self.G_TASKID]
			#execfile(self.G_POST_PY)
			os.system('c:/python27/python.exe ' + self.G_POST_PY)
		self.G_RENDER_LOG.info('[BASE.RBpostPy.end.....]')
	
	def RBconvertSmallPic(self):	
		self.G_RENDER_LOG.info('[BASE.RBconvertSmallPic.start.....]')
		smallSize='200'
		if self.G_KG=='1':
			smallSize='40'
			
		workSmallPath=os.path.join(self.G_RENDER_WORK_TASK,'small')		
		if not os.path.exists(workSmallPath):
			os.makedirs(workSmallPath)
			
		list_dirs = os.walk(self.G_RENDER_WORK_OUTPUT) 
		for root, dirs, files in list_dirs: 
			
			for name in files:
				workBigPic =os.path.join(root, name)
				smallName=workBigPic.replace(self.G_RENDER_WORK_OUTPUT+'\\','')
				smallName=self.G_JOB_NAME+"_"+smallName.replace('\\','[_]').replace('.','[-]')+'.jpg'
				workSmallPic=os.path.join(workSmallPath,smallName)
				convertCmd='c:/ImageMagick/nconvert.exe  -out jpeg -ratio -resize '+smallSize+' 0 -overwrite -o "'+workSmallPic +'" "'+workBigPic+'"'
				#print workBigPic
				self.RBcmd(convertCmd,True,False)
				self.G_FEE_LOG.info('smallPic='+smallName)
				
				
		moveCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +workSmallPath.replace('/','\\')+'\*.*" /to="'+self.G_PATH_SMALL.replace('/','\\')+'"'
		self.RBcmd(moveCmd,True,False)	
		#convertCmd='cscript /nologo c:\\script\\vbs\\' + self.G_CONVERTVBS_NAME + '  '+self.G_USERID+' '+self.G_TASKID + ' "'+ self.G_JOB_NAME  +'" "'+self.G_PATH_SMALL +'\" '
		self.G_RENDER_LOG.info('[BASE.RBconvertSmallPic.end.....]')

	def RBresultAction(self):
		self.G_RENDER_LOG.info('[BASE.RBresultAction.start.....]')
		#RB_small
		if not os.path.exists(self.G_PATH_SMALL):
			os.makedirs(self.G_PATH_SMALL)
		frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
		cmd1='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+self.G_PATH_USER_OUTPUT+'"'
		cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ self.G_PATH_USER_OUTPUT+'"'
		cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
		
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
		
		self.RBcmd(cmd1)
		self.RBcmd(cmd2)
		self.RBcmd(cmd3)
		self.RBcmd(cmd4)
		self.G_RENDER_LOG.info('[BASE.RBresultAction.end.....]')
		
	def RBhanResult(self):#8
		self.G_RENDER_LOG.info('[BASE.RBhanResult.start.....]')
		
		
		if hasattr(self,'G_KG'):
			if self.G_KG=='2' or self.G_KG=='3':#inc or animation 
			
				workMap=os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
				renderTemp=os.path.join(self.G_POOL,'temp',(self.G_FATHERID+'_render'))
				copyCmdStr='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+workMap.replace('/','\\')+'" /to="'+renderTemp.replace('/','\\')+'\\"'
				self.RBcmd(copyCmdStr)
				
				self.RBresultAction()
			elif self.G_KG=='4':#fast photon
				print 'fast photon'
				workMap = os.path.join(self.G_RENDER_WORK_OUTPUT,'*.vrmap')
				mergePoolTemp=os.path.join(self.G_POOL,'temp',(self.G_MERGE_TASKID+'_mergephoton'),'temp')
				cmdStr='c:\\fcopy\\FastCopy.exe  /speed=full /force_close  /no_confirm_stop /force_start "' +workMap.replace('/','\\') +'" /to="'+mergePoolTemp+'"'
				self.RBcmd(cmdStr)
				frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
				cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ mergePoolTemp+'"'
				cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
				
				feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
				feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
				cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
				
				self.RBcmd(cmd2)
				self.RBcmd(cmd3)
				self.RBcmd(cmd4)
				self.G_RENDER_LOG.info('[BASE.RBresultAction.end.....]')
			else:
				self.RBresultAction()
		else:
			self.RBresultAction()
		
		self.G_RENDER_LOG.info('[BASE.RBhanResult.end.....]')
		
	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		print str(continueOnErr)+'--->>>'+str(myShell)
		self.G_RENDER_LOG.info('cmd...'+cmdStr)
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			if resultLine!='':
				self.G_RENDER_LOG.info(resultLine)
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		self.G_RENDER_LOG.info('resultStr...'+resultStr)
		self.G_RENDER_LOG.info('resultCode...'+str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(resultCode)
		return resultStr

	def RBgetPluginDict(self):
		self.G_RENDER_LOG.info('[Max.RVgetPluginDict start]')
		self.G_RAYVISION_PLUGINSCFG=os.path.join(self.G_RENDER_WORK_TASK,'plugins.cfg')
		self.G_RENDER_LOG.info(self.G_RAYVISION_PLUGINSCFG)
		print self.G_RAYVISION_PLUGINSCFG
		plginInfoDict=None
		if  os.path.exists(self.G_RAYVISION_PLUGINSCFG):
			fp = open(self.G_RAYVISION_PLUGINSCFG)
			
			if fp:
				self.G_RENDER_LOG.info('plugins file is exists')
				listOfplgCfg = fp.readlines()
				removeNL = [(i.rstrip('\n')) for i in listOfplgCfg]
				combinedText = ''.join(removeNL)
				plginInfoDict = eval('dict(%s)' % combinedText)
				print plginInfoDict
				self.G_RENDER_LOG.info(plginInfoDict)
				for i in plginInfoDict.keys():
					print i
					print plginInfoDict[i]
		self.G_RENDER_LOG.info('[Max.RVgetPluginDict end]')
		return plginInfoDict
		
	def RBexecute(self):#total
	
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[BASE.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[BASE.RBexecute.end.....]')
		
#---------------------calss max--------------------
class Max(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print 'Max.init...'
		self.G_MAXBAT_NAME='max.bat'
		self.G_RENDERBAT_NAME='render.bat'		
		self.G_PLUGINBAT_NAME='plugin.bat'
		self.G_SCRIPT_NAME='crender.ms'
		
		self.G_CG_FILE=self.G_TASKID+'.max'
	
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Max.RBhanFile.start.....]')
		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		
		scriptmax=r'script\max'
		msFile=os.path.join(self.G_POOL,scriptmax,self.G_SCRIPT_NAME)
		maxBat=os.path.join(self.G_POOL,scriptmax,self.G_MAXBAT_NAME)
		renderBat=os.path.join(self.G_POOL,scriptmax,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptmax,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		maxscript='c:/script/max'
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
		copyScriptCmd3='xcopy /y /f "'+msFile+'" "'+maxscript+'/" '
		copyScriptCmd4='xcopy /y /f "'+renderBat+'" "'+maxscript+'/" '
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		
		
		self.RBcmd(copyScriptCmd1)
		
		self.RBcmd(copyScriptCmd2)
		
		self.RBcmd(copyScriptCmd3)
		
		self.RBcmd(copyScriptCmd4)
		
		self.RBcmd(copyVBSCmd)
		
		
		oldMax=os.path.join(self.G_RENDER_WORK_TASK,os.path.basename(self.G_PATH_INPUTFILE))
		newMax=os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		#if  os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		if  os.path.exists(oldMax) and not os.path.exists(newMax):
			oldMax = oldMax.replace('\\','/')
			newMax = newMax.replace('\\','/')
			print oldMax
			print newMax
			os.rename(oldMax,newMax)
		self.G_RENDER_LOG.info('[Max.RBhanFile.end.....]')
	
	def RBcopyTempFile(self):
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.start.....]')
	#copy temp file
		#if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		tempFull=os.path.join(self.G_POOL_TASK,'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
		self.RBcmd(copyPoolCmd)
		
		unpackCmd='c:\\exdupe.exe -Rf "'+ os.path.join(self.G_RENDER_WORK_TASK,'temp.full')+ '" "' + self.G_RENDER_WORK_TASK +'/" '
		self.RBcmd(unpackCmd,True)
		
		delPackCmd='del /q /f "'+os.path.join(self.G_RENDER_WORK_TASK,'temp.full').replace('\\','/')+'"'
		os.remove(os.path.join(self.G_RENDER_WORK_TASK,'temp.full'))
		echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
		self.RBcmd(echoCmd,False,True)
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.end.....]')

	def RBrenderConfig(self):#5
		self.G_RENDER_LOG.info('[Max.RBrenderConfig.start.....]')
		#multicatter = getattr(self,'G_CG_SCATTER')
		if hasattr(self,'G_CG_SCATTER'):
			if self.G_CG_SCATTER.startswith('multiscatter'):			
				configMultCmd='c:/script/max/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' multiscatter "' +self.G_CG_SCATTER+'"'
				self.RBcmd(configMultCmd)
		self.G_RENDER_LOG.info('[Max.RBrenderConfig.end.....]')
	
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Max.RBrender.start.....]')
		startTime = time.time()
		cgFile = os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		cgFile = cgFile.replace('\\' , '/')
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		renderCmd='c:/script/max/'+self.G_RENDERBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' 0 \"' +self.G_CG_START_FRAME  +'\" '+self.G_KG+' "'+self.G_JOB_NAME+'" "' +cgFile+'"'
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Max.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Max...execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Max.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()
		
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Max.RBexecute.end.....]')
	

#---------------------calss maxclient--------------------
class MaxClient(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print 'Max.init...'
		self.G_MAXBAT_NAME='max.bat'
		self.G_RENDERBAT_NAME='crender.bat'		
		self.G_PLUGINBAT_NAME='plugin.bat'
		self.G_SCRIPT_NAME='crender.ms'
		
		self.G_CG_FILE=self.G_TASKID+'.max'
	
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Max.RBhanFile.start.....]')
		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		
		scriptmax=r'script\max'
		msFile=os.path.join(self.G_POOL,scriptmax,self.G_SCRIPT_NAME)
		maxBat=os.path.join(self.G_POOL,scriptmax,self.G_MAXBAT_NAME)
		renderBat=os.path.join(self.G_POOL,scriptmax,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptmax,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		maxscript='c:/script/max'
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
		copyScriptCmd3='xcopy /y /f "'+msFile+'" "'+maxscript+'/" '
		copyScriptCmd4='xcopy /y /f "'+renderBat+'" "'+maxscript+'/" '
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		
		
		#self.RBcmd(copyScriptCmd1)
		
		#self.RBcmd(copyScriptCmd2)
		
		#self.RBcmd(copyScriptCmd3)
		
		#self.RBcmd(copyScriptCmd4)
		
		self.RBcmd(copyVBSCmd)
		
		
		oldMax=os.path.join(self.G_RENDER_WORK_TASK,os.path.basename(self.G_PATH_INPUTFILE))
		newMax=os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		#if  os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		if  os.path.exists(oldMax) and not os.path.exists(newMax):
			oldMax = oldMax.replace('\\','/')
			newMax = newMax.replace('\\','/')
			print oldMax
			print newMax
			os.rename(oldMax,newMax)
		self.G_RENDER_LOG.info('[Max.RBhanFile.end.....]')
	
	def RBcopyTempFile(self):
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.start.....]')
	#copy temp file
		#if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		tempFull=os.path.join(self.G_POOL_TASK,'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
		self.RBcmd(copyPoolCmd)
		
		unpackCmd='c:\\exdupe.exe -Rf "'+ os.path.join(self.G_RENDER_WORK_TASK,'temp.full')+ '" "' + self.G_RENDER_WORK_TASK +'/" '
		self.RBcmd(unpackCmd,True)
		oldMax=os.path.join(self.G_RENDER_WORK_TASK,'submit.max')
		newMax=os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		#if  os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		if  os.path.exists(oldMax) and not os.path.exists(newMax):
			oldMax = oldMax.replace('\\','/')
			newMax = newMax.replace('\\','/')
			print oldMax
			print newMax
			os.rename(oldMax,newMax)
			
		delPackCmd='del /q /f "'+os.path.join(self.G_RENDER_WORK_TASK,'temp.full').replace('\\','/')+'"'
		os.remove(os.path.join(self.G_RENDER_WORK_TASK,'temp.full'))
		echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
		self.RBcmd(echoCmd,False,True)
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.end.....]')

	def RBloadPlugin(self):
		self.G_RENDER_LOG.info('[Max.RVloadPlugin start]')
		self.G_RENDER_LOG.info('\n\n------------------------------------------------------------[Start Config plugin]--------------------------------------------------------\n\n')
		
		pluginDelCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "del"'
		self.G_RENDER_LOG.info('pluginDelCmd------'+pluginDelCmd)
		self.G_RENDER_LOG.info(pluginDelCmd+'\n')
		
		self.RBcmd(pluginDelCmd)
		
		if 'vray' in self.G_CG_RENDER_VERSION:
			pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "vray" "'+  self.G_CG_RENDER_VERSION+'"'
			self.G_RENDER_LOG.info('vraypluginCmd------'+pluginCmd)
			self.G_RENDER_LOG.info(pluginCmd+'\n')
			self.RBcmd(pluginCmd)

		allPlugDict=self.RBgetPluginDict()
		if allPlugDict and allPlugDict.has_key('plugins'):
			pluginDict=allPlugDict['plugins']
			for pluginName in pluginDict:
				pluginVersion=pluginDict[pluginName]
				self.G_RENDER_LOG.info('pluginName...'+ pluginName)
				self.G_RENDER_LOG.info('pluginVersion...'+ pluginVersion)
				pluginCmd=self.G_RAYVISION_PLUGINBAT +' "'+self.G_CG_VERSION+'" "'+ pluginName +'" "'+  pluginName+pluginVersion+'"'
				self.G_RENDER_LOG.info('pluginCmd------'+pluginCmd)
				self.G_RENDER_LOG.info(pluginCmd+'\n')
				self.RBcmd(pluginCmd)
		maxCmd=self.G_RAYVISION_MAXBAT+' "'+self.G_CG_VERSION+'" "config"'
		self.G_RENDER_LOG.info('maxCmd------'+maxCmd)
		self.G_RENDER_LOG.info(maxCmd+'\n')
		self.RBcmd(maxCmd)

	def RBrenderConfig(self):#5
		self.G_RENDER_LOG.info('[Max.RBrenderConfig.start.....]')
		#multicatter = getattr(self,'G_CG_SCATTER')
		#---------------------------------
		maxscriptPath='B:/plugins/max/script'
		maxscriptName='renderU3_0_1.ms'
		pluginBatName='plugin.bat'
		maxBatName='max.bat'
		customBatName='custom.bat'
		pluginPool=r'\\10.50.1.22\td'
		#-----------------------------------
		os.system('net use * /delete /y')
		os.system('net use B: '+pluginPool)
		
		
		customerScriptPath=os.path.join(maxscriptPath,self.G_USERID).replace('\\','/')
		
		if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
			maxscriptName='renderA3_0_1.ms'
		customerMs=os.path.join(customerScriptPath,maxscriptName).replace('\\','/')
		customerPluginBat=os.path.join(customerScriptPath,pluginBatName).replace('\\','/')
		customerMaxBat=os.path.join(customerScriptPath,maxBatName).replace('\\','/')
		customBat=os.path.join(customerScriptPath,customBatName).replace('\\','/')
		self.G_RENDER_LOG.info('customBat------'+customBat)
		
		self.G_RAYVISION_MAXMS=os.path.join(maxscriptPath,maxscriptName).replace('\\','/')
		if os.path.exists(customerMs):
			self.G_RAYVISION_MAXMS=customerMs
			
		self.G_RAYVISION_PLUGINBAT=os.path.join(maxscriptPath,pluginBatName).replace('\\','/')
		if os.path.exists(customerPluginBat):
			self.G_RAYVISION_PLUGINBAT=customerPluginBat
		
		self.G_RAYVISION_MAXBAT=os.path.join(maxscriptPath,maxBatName).replace('\\','/')
		if os.path.exists(customerMaxBat):
			self.G_RAYVISION_MAXBAT=customerMaxBat
		
		if os.path.exists(customBat):
			self.G_RENDER_LOG.info('customCmd------>>>>')
			customCmd=customBat+' "'+self.G_TASKID+'"'
			self.G_RENDER_LOG.info('customCmd------'+customCmd)
			self.RBcmd(customCmd)
		
		self.RBloadPlugin()
		self.G_RENDER_LOG.info('[Max.RBrenderConfig.end.....]')
		
	def writeMsFile(self,sceneFile,renderFrame,mySonid):
		self.G_RENDER_LOG.info('[Max.writeMsFile.start.....]')
		#C:\users\enfuzion\AppData\Roaming\RenderBus\Profiles\users\cust\enfuzion\maxscript
		msFile=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.ms')
		msFile=msFile.replace('\\','/')
		self.G_RENDER_LOG.info('msFile...'+msFile)
		print msFile
		# cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_RAYVISION_USER_ID+'\\" \\"'+self.G_RAYVISION_TASK_ID+'\\" \\"0\\" \\"'+framenum['startFrame']+'\\" \\"0\\" \\"'+self.G_RAYVISION_STARTFRAME+'\\" \\"'+sceneFile+'\\" \\"'+output+'\\" "'
		sceneFile=sceneFile.decode('utf-8').encode('gbk')
		msFileObject=codecs.open(msFile,'a')
		msFileObject.write('(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"\r\n')
		msFileObject.write('filein @"'+self.G_RAYVISION_MAXMS+'"\r\n')
		msFileObject.write('fn renderRun = (\r\n')
		mystr='rvRender "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+mySonid+'" "'+renderFrame+'" "'+self.G_KG+'" "'+self.G_JOB_NAME+'" "'+sceneFile+'" "'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/" "1005" ""\r\n'
		
		msFileObject.write(mystr)
		msFileObject.write(')\r\n')
		msFileObject.close()
		self.G_RENDER_LOG.info('[Max.writeMsFile.end.....]')
		return msFile
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Max.RBrender.start.....]')
		startTime = time.time()
		cgFile = os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		cgFile = cgFile.replace('\\' , '/')
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		mySonid='0'
		if hasattr(self,'G_SONID'):
			mySonid=self.G_SONID
		#renderCmd='c:/script/max/'+self.G_RENDERBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' '+mySonid+' ' +self.G_CG_START_FRAME  +' '+self.G_KG+' "'+self.G_JOB_NAME+'" "' +cgFile+'"'
		#self.RBcmd(renderCmd,True,False)
		maxRenderExe='"C:/Program Files/Autodesk/'+ self.G_CG_VERSION+'/3dsmax.exe"'
		if self.G_CG_VERSION=='3ds Max 2010':
			renderMsFile=self.writeMsFile(cgFile,self.G_CG_START_FRAME,mySonid)
			cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+renderMsFile+'\\";renderRun() "'
		else:
			cmdStr = maxRenderExe+' -silent  -mxs "filein \\"'+self.G_RAYVISION_MAXMS+'\\";rvRender \\"'+self.G_USERID+'\\" \\"'+self.G_TASKID+'\\" \\"'+mySonid+'\\" \\"'+self.G_CG_START_FRAME+'\\" \\"'+self.G_KG+'\\" \\"'+self.G_JOB_NAME+'\\" \\"'+cgFile+'\\" \\"'+self.G_RENDER_WORK_OUTPUT.replace('\\','/')+'/\\" \\"1005\\" \\"\\""'
		
		self.RBcmd(cmdStr.decode('utf-8').encode('gbk'),True,False)
		
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Max.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Max...execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Max.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()
		
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Max.RBexecute.end.....]')
	


	
#---------------------max express--------------------
class MaxExpress(Max):
	def RBcopyTempFile(self):
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.start.....]')
	    #copy temp file
		#if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
		tempFull=os.path.join(self.G_POOL_TASK,'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /cmd=diff /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
		self.RBcmd(copyPoolCmd)
		echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
		self.RBcmd(echoCmd,False,True)
		self.G_RENDER_LOG.info('[Max.RBcopyTempFile.end.....]')
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Max.RBrender.start.....]')
		startTime = time.time()
		cgFile = self.G_PATH_INPUTFILE;
		cgFile = cgFile.replace('\\' , '/')
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		renderCmd='c:/script/max/'+self.G_RENDERBAT_NAME+' "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' 0 ' +self.G_CG_START_FRAME  +' '+self.G_KG+' "'+self.G_JOB_NAME+'" "' +cgFile+'"'
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Max.RBrender.end.....]')
#---------------------calss maya--------------------		
class Maya(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "MAYA INIT"
		self.G_SCRIPT_NAME='maya_preRender5.mel'
		self.G_RENDERBAT_NAME='render5.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'

	
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')
		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		
		scriptmaya=r'script\maya'
		melFile=os.path.join(self.G_POOL,scriptmaya,self.G_SCRIPT_NAME)
		renderBat=os.path.join(self.G_POOL,scriptmaya,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(self.G_POOL,scriptmaya,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		
		mayascript='c:/script/maya'
		copyScriptCmd1='xcopy /y /f "'+melFile+'" "'+mayascript+'/" '
		copyScriptCmd2='xcopy /y /f "'+renderBat+'" "'+mayascript+'/" '
		copyScriptCmd3='xcopy /y /f "'+pluginBat+'" "'+mayascript+'/" '
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.RBcmd(copyVBSCmd)
		self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
		
		
	def RBrenderConfig(self):#5
		self.G_RENDER_LOG.info('[Maya.RBrenderConfig.start.....]')
		#multicatter = getattr(self,'G_CG_SCATTER')
		if hasattr(self,'G_CG_RENDER_VERSION'):
			if self.G_CG_RENDER_VERSION.startswith('arnold'):
				self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.start.....]')
				shortRenderVersion=self.G_CG_RENDER_VERSION.replace('arnold','')
				configMultCmd='c:/script/maya/'+self.G_PLUGINBAT_NAME+' "'+self.G_CG_VERSION+'" '+' "arnold" "' +shortRenderVersion+'"'
				self.RBcmd(configMultCmd)
				self.G_RENDER_LOG.info('[Maya.RBrenderConfig.arnold.end.....]')
		self.G_RENDER_LOG.info('[Maya.RBrenderConfig.end.....]')
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		renderTxtFile = os.path.join(self.G_RENDER_WORK_TASK_CFG,os.path.basename(self.G_RENDER_TXTNAME))
		renderTxtFile=renderTxtFile.replace('\\','/')
		
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[MAYA.RBexecute.start...]')
		self.RBprePy()
		self.RBmakeDir()
		
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Maya.RBexecute.end.....]')

#--------------------- maya express--------------------	
class MayaExpress(Maya):
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		mayaExePath=mayaExePath.replace('\\','/')
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
		
#--------------------- maya Client--------------------	
class MayaClient(Maya):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "MAYA INIT"
		self.G_SCRIPT_NAME='maya_preRender5.mel'
		self.G_RENDERBAT_NAME='crender.bat'
		self.G_PLUGINBAT_NAME='plugin.bat'
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+self.G_CG_VERSION)
		mayaExePath=os.path.join('C:/Program Files/Autodesk',self.G_CG_VERSION,'bin/Render.exe')
		self.G_RENDER_LOG.info('[G_CG_VERSION.....]'+mayaExePath)
		mayaExePath=mayaExePath.replace('\\','/')
		mayascript='c:/script/maya'
		melFile=os.path.join(mayascript,self.G_SCRIPT_NAME)
		renderBat=os.path.join(mayascript,self.G_RENDERBAT_NAME)
		pluginBat=os.path.join(mayascript,self.G_PLUGINBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		 #C:/script/maya/Render4.bat "$userId"  "$taskId"  "$enginePath/bin/Render.exe" "C:/enfwork/$taskId/sc13_bg_scenes_TXCQ_SQ013_bg_lt_color_0210_cam_M.mb_20140210154833_487211732" $frame  $frame 1  "$projectPath"  "$filePath"  >>$logDir$ENFJOBNAME.txt 2>&1  
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" '
		
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')



#---------------------calss Houdini--------------------		
class Houdini(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "Houdini INIT"
		self.G_RENDERBAT_NAME='Erender.bat'

	
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('[Maya.RBhanFile.start.....]')

		moveOutputCmd='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start '+self.G_RENDER_WORK_OUTPUT.replace('/','\\')+' /to='+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')
		self.RBcmd(moveOutputCmd)
		
		scriptHoudini=r'script\houdini\new'
		renderBat=os.path.join(self.G_POOL,scriptHoudini,self.G_RENDERBAT_NAME)
		
		vbsFile=os.path.join(self.G_POOL,r'script\vbs',self.G_CONVERTVBS_NAME)
		
		houdiniScript='c:/script/houdini'
		copyScriptCmd='xcopy /y /f "'+renderBat+'" "'+houdiniScript+'/" '
		copyVBSCmd='xcopy /y /f "'+vbsFile+'" "c:/script/vbs/" '
		
		self.RBcmd(copyScriptCmd)
		self.RBcmd(copyVBSCmd)
		self.G_RENDER_LOG.info('[Maya.RBhanFile.end.....]')
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[Maya.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		houdiniScript='c:/script/houdini'
		renderBat=os.path.join(houdiniScript,self.G_RENDERBAT_NAME)
		vbsFile=os.path.join(r'c:/script/vbs',self.G_CONVERTVBS_NAME)
		# "c:/script/Houdini/Erender.bat" "$userId" "$taskId" "$startFrame" "$endFrame" "$frameStep" "$cgv" "$projectPath" "$filePath" "$output"  "$layerName" "$option"" 
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+self.G_CG_VERSION+'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "' +self.G_RENDER_WORK_OUTPUT+'"  "'+self.G_CG_LAYER_NAME+'" "'+self.G_CG_OPTION+'"' 
		
		self.G_RENDER_LOG.info(renderCmd)
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[Maya.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'Houdini.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')
		self.RBprePy()
		self.RBmakeDir()		
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[Maya.RBexecute.start.....]')



#---------------------calss C4d--------------------		
class C4D(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "C4d INIT"
		
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		myCgVersion = self.G_CG_VERSION
		if myCgVersion.endswith('.64') :
			myCgVersion=myCgVersion.replace('.64','')
		if myCgVersion.endswith('.32') :
			myCgVersion=myCgVersion.replace('.32','')
			
		c4dExePath=os.path.join(r'C:\Program Files\MAXON',myCgVersion,'CINEMA 4D 64 Bit.exe')
		outFilePath=os.path.join(self.G_RENDER_WORK_OUTPUT,self.G_OUTPUT_FILENMAE)
		outFilePath.replace('/','\\')
		 #C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe -noopengl -nogui -frame 1 1 -render \\10.50.1.4\dd\inputData\c4d\162686\Warehouse\pipi\pipi.c4d -oresolution 1920 1080 -oformat TGA -oimage C:\enfwork\213282\output\warehouse_4   
		renderCmd='"'+c4dExePath +'" -noopengl -nogui  -frame '+self.G_CG_START_FRAME+' ' + self.G_CG_END_FRAME +' -render "'+ self.G_PATH_INPUTFILE +'" -oresolution '+self.G_IMAGE_WIDTH+' '+self.G_IMAGE_HEIGHT +' -oformat '+self.G_IFORMAT  +' -oimage "'+outFilePath+'"'
		
		self.G_RENDER_LOG.info(renderCmd)
		#os.system(renderCmd)
		self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[C4D.RBrender.end.....]')
		
	def RBexecute(self):#Render
		
		print 'C4d.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[C4D.RBexecute.start.....]')
		
		self.RBprePy()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_RENDER_LOG.info('[C4D.RBexecute.end.....]')

#-----------------------Render----------------------------------------
class RenderAction():
	def __init__(self,**paramDict):
		cgName=paramDict['G_CG_NAME']
		print 'cgName=================='+cgName
		exec('RenderAction.__bases__=('+cgName+',)')
		exec(cgName+'.__init__(self,**paramDict)')
	'''
	def RBrender(self):#Render command
		print 'RenderAction..max...render....'
	'''
#-----------------------main-------------------------------
def main(**paramDict):
	render=RenderAction(**paramDict)
	print 'G_POOL_NAME___'+render.G_POOL
	render.RBexecute()