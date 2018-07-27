import os,sys,subprocess,string,logging,time

import logging

class Base():

	def __init__(self,**paramDict):
		print 'Base.init...-------------------'
		
		self.G_LOG_WORK='C:/log/render'
		self.G_RENDER_WORK='C:/work/render'
		self.G_RENDER_TXT_NAME='rb.txt'
		
		
		self.G_USERID=paramDict['G_USERID']
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
		
		
		self.G_RENDER_WORK_TASK=os.path.join(self.G_RENDER_WORK,self.G_TASKID)
		self.G_RENDER_TXT=os.path.join(self.G_RENDER_WORK_TASK,self.G_RENDER_TXT_NAME)#c:/renderwork/12343/renderbus/render.txt
		
		#log
		self.G_RENDER_LOG=logging.getLogger('renderLog')
		self.G_FEE_LOG=logging.getLogger('renderLog')
		
		self.G_RENDER_WORK_OUTPUT = os.path.join(self.G_RENDER_WORK,self.G_TASKID,'output')
		self.G_RENDER_WORK_OUTPUTBAK = os.path.join(self.G_RENDER_WORK,self.G_TASKID,'outputbak')
		
		'''
		G_KG=0
		G_CG_VERSION='3ds Max 2012'
		G_CG_RENDER_VERSION='vray2.10.01'
		G_CG_MULTISCATTER_VERSION='multiscatter1.1.07a'
		G_CG_FILE='310239.max'
		G_PATH_SMALL=r'\\10.50.10.5\d\outputData\small'
		G_PATH_USER_OUTPUT=r'\\10.50.10.5\d\outputData'
		G_PATH_COST=r'\\10.50.10.5\d\transfer\txt\test'
		G_SINGLE_FRAME_CHECK='singleFrameCheck.exe'
		'''
		
		
	def RBmakeDir(self):#1
		print 'makeDir ....log.....'
		#log
		renderLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
		if not os.path.exists(renderLogDir):
			os.makedirs(renderLogDir)
			
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
			
			
	def RBinitLog(self):#2
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		renderLogPath=os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'.txt'))
		self.G_RENDER_LOG.setLevel(logging.DEBUG)
		renderLogHandler=logging.FileHandler(renderLogPath)
		renderLogHandler.setFormatter(fm)
		self.G_RENDER_LOG.addHandler(renderLogHandler)
		console = logging.StreamHandler()  
		console.setLevel(logging.INFO)  
		self.G_RENDER_LOG.addHandler(console)
		
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		self.G_FEE_LOG.setLevel(logging.DEBUG)
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		feeLogHandler=logging.FileHandler(feeTxt)
		feeLogHandler.setFormatter(fm)
		self.G_FEE_LOG.addHandler(feeLogHandler)
		
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_RENDER_LOG.info('base.hanfile.....')

		maxBat=os.path.join(self.G_POOL,r'script\max\max.bat')
		pluginBat=os.path.join(self.G_POOL,r'script\max\plugin.bat')
		maxscript='c:/script/max'
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		
		copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
		
		self.G_RENDER_LOG.info(copyScriptCmd1)
		self.RBcmd(copyScriptCmd1)
		
		self.G_RENDER_LOG.info(copyScriptCmd2)
		self.RBcmd(copyScriptCmd2)
		
		
		
		if not os.path.exists(os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt')):
			tempFull=os.path.join(self.G_POOL,'temp',self.G_USERID,(self.G_TASKID+'p'),'temp.full')
			copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFull.replace('/','\\')+'" /to="'+self.G_RENDER_WORK_TASK.replace('/','\\')+'"'
			self.G_RENDER_LOG.info(copyPoolCmd)
			self.RBcmd(copyPoolCmd)
			
			unpackCmd='c:\\exdupe.exe -Rf "'+ os.path.join(self.G_RENDER_WORK_TASK,'temp.full')+ '" "' + self.G_RENDER_WORK_TASK +'/" '
			self.G_RENDER_LOG.info(unpackCmd)
			self.RBcmd(unpackCmd,True)
			
			delPackCmd='del /q /f "'+os.path.join(self.G_RENDER_WORK_TASK,'temp.full').replace('\\','/')+'"'
			self.G_RENDER_LOG.info(os.path.join(self.G_RENDER_WORK_TASK,'temp.full'))
			
			os.remove(os.path.join(self.G_RENDER_WORK_TASK,'temp.full'))
			
			echoCmd = 'echo ...>>'+os.path.join(self.G_RENDER_WORK_TASK,'zzz.txt').replace('\\','/')
			self.G_RENDER_LOG.info(echoCmd)
			self.RBcmd(echoCmd,False,True)
		
		
	def RBreadRenderTxt(self):#4
		print 'readrenderTxt....'
		renderTxt=self.G_RENDER_TXT
		txtFile=open(renderTxt, 'r')
		allLines=txtFile.readlines()

		for eachLine in allLines:
			if eachLine.startswith('#') or eachLine=='\n':
				continue
			execStr='self.'+eachLine.strip()
			print execStr
			exec(execStr)
			
			
	def RBrenderConfig(self):#5
		print 'Base..renderConfig....'
		#multicatter = getattr(self,'G_CG_MULTISCATTER_VERSION')
		if hasattr(self,'G_CG_MULTISCATTER_VERSION'):
			configMultCmd='c:/script/max/plugin.bat "'+self.G_CG_VERSION+'" '+' multiscatter ' +self.G_CG_MULTISCATTER_VERSION
			self.RBcmd(configMultCmd)
		
		#configVrayCmd = 'c:/script/max/max.bat "'+self.G_CG_VERSION+'" ' +self.G_CG_RENDER_VERSION+ ' config'
		#self.RBcmd(configVrayCmd)
		#print self.__dict__
		
		
	def RBwriteConsumeTxt(self):#6
		print 'Base..writeConsumeTxt....'
		
	def RBrender(self):#7
		print 'Base...render...'
		startTime = time.time()
		
		print 'max...render....'
		cgFile = os.path.join(self.G_RENDER_WORK_TASK,self.G_CG_FILE)
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		renderCmd='c:/script/max/render.bat "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' '+self.G_KG+' ' +self.G_CG_START_FRAME  +' 0 "' +cgFile+'"'
		self.G_RENDER_LOG.info(renderCmd)
		#os.system(renderCmd)
		self.RBcmd(renderCmd)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('Render completed!')
		
		
	def RBhanResult(self):#8
		print 'Base...hanResult....'
		#RB_small
		outputSamll = os.path.join(self.G_PATH_SMALL,self.G_USERID,self.G_TASKID)
		if not os.path.exists(outputSamll):
			os.makedirs(outputSamll)
		frameCheck = os.path.join(self.G_POOL,'tools',self.G_SINGLE_FRAME_CHECK)
		
		userOutput = os.path.join(self.G_PATH_USER_OUTPUT,self.G_USERID,self.G_TASKID)
		convertCmd='cscript /nologo c:\\script\\vbs\\convert2.vbs  '+self.G_USERID+' '+self.G_TASKID + ' "'+ self.G_JOB_NAME  +'" "'+outputSamll +'\" '
		cmd1='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\') +'" /to="'+userOutput.replace('/','\\')+'"'
		cmd2='"' +frameCheck + '" "' + self.G_RENDER_WORK_OUTPUT + '" "'+ userOutput+'"'
		cmd3='c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start "' +self.G_RENDER_WORK_OUTPUT.replace('/','\\')+'\*.*" /to="'+self.G_RENDER_WORK_OUTPUTBAK.replace('/','\\')+'"'
		
		feeLogFile=self.G_USERID+'-'+self.G_TASKID+'-'+self.G_JOB_NAME+'.txt'
		feeTxt=os.path.join(self.G_RENDER_WORK_TASK,feeLogFile)
		cmd4='xcopy /y /f "'+feeTxt+'" "'+self.G_PATH_COST+'/" '
		self.RBcmd(convertCmd)
		self.RBcmd(cmd1)
		self.RBcmd(cmd2)
		self.RBcmd(cmd3)
		self.RBcmd(cmd4)
		
	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		print str(continueOnErr)+'--->>>'+str(myShell)
		self.G_RENDER_LOG.info(cmdStr)
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			if resultLine!='':
				self.G_RENDER_LOG.info(resultLine)
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		self.G_RENDER_LOG.info(resultStr)
		self.G_RENDER_LOG.info(str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(0)
		return resultStr
		
	def RBexecute(self):#total
		print 'Base...execute.....'
		self.G_RENDER_LOG.info('Render...')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBhanFile()
		self.RBreadRenderTxt()
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBhanResult()
		
		self.G_FEE_LOG.info('Completed!')


#---------------------calss max--------------------
class Max(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print 'Max-------------------'
		print "Max INIT"
		
	'''
	def RBrender(self):#Render command
		print 'Max...render...'		
	'''
	
	def RBexecute(self):#Render
		
		print 'Max...execute.....'
		self.G_RENDER_LOG.info('Render...')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBhanFile()
		self.RBreadRenderTxt()
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBhanResult()
		
		self.G_FEE_LOG.info('Completed!')
		
		

#---------------------calss maya--------------------		
class Maya(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "Maya INIT"
		
	def RBrender(self):#Render command
		print 'maya...render....'
		
	def RBexecute(self):#Render
		print 'Maya...exec....'

		
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