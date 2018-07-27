import os,sys,subprocess,string,logging,time

import logging

class Base():

	def __init__(self,**paramDict):
		print 'Base.init...-------------------'
		
		self.G_LOG_WORK='C:/LOG/analyse'
		self.G_ANALYSE_WORK='C:/WORK/analyse'
		self.G_ANALYSE_TXT_NAME='rb.txt'
		
		
		self.G_USERID=paramDict['G_USERID']
		self.G_TASKID=paramDict['G_TASKID']
		self.G_POOL=paramDict['G_POOL']

		self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
		self.G_JOB_NAME=self.G_SYS_ARGVS[3]
		self.G_NODE_NAME=self.G_SYS_ARGVS[5]
		
		
		self.G_ANALYSE_WORK_TASK=os.path.join(self.G_ANALYSE_WORK,self.G_TASKID)
		self.G_ANALYSE_TXT=os.path.join(self.G_ANALYSE_WORK_TASK,self.G_ANALYSE_TXT_NAME)#c:/renderwork/12343/renderbus/render.txt
		
		#log
		self.G_ANALYSE_LOG=logging.getLogger('analyseLog')
		
		'''
		G_KG=0
		G_CG_VERSION='3ds Max 2012'
		G_CG_RENDER_VERSION='vray2.10.01'
		G_CG_MULTISCATTER_VERSION='multiscatter1.1.07a'
		G_CG_PROJECT
		G_CG_FILE='310239.max'
		G_CG_TXT='fdfdabc_max'
		G_PATH_SMALL=r'\\10.50.10.5\d\outputData\small'
		G_PATH_USER_OUTPUT=r'\\10.50.10.5\d\outputData'
		G_PATH_COST=r'\\10.50.10.5\d\transfer\txt\test'
		G_SINGLE_FRAME_CHECK='singleFrameCheck.exe'
		'''
		
		
	def RBmakeDir(self):#1
		print 'makeDir ....log.....'
		#log
		analyseLogDir=os.path.join(self.G_LOG_WORK,self.G_TASKID)
		if not os.path.exists(analyseLogDir):
			os.makedirs(analyseLogDir)
			
		#renderwork
		if not os.path.exists(self.G_ANALYSE_WORK_TASK):
			os.makedirs(self.G_ANALYSE_WORK_TASK)
			
			
	def RBinitLog(self):#2
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		renderLogPath=os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'.txt'))
		self.G_ANALYSE_LOG.setLevel(logging.DEBUG)
		renderLogHandler=logging.FileHandler(renderLogPath)
		renderLogHandler.setFormatter(fm)
		self.G_ANALYSE_LOG.addHandler(renderLogHandler)
		console = logging.StreamHandler()  
		console.setLevel(logging.INFO)  
		self.G_ANALYSE_LOG.addHandler(console)		
		
		
	def RBhanFile(self):#3 copy script,copy from pool,#unpack
		self.G_ANALYSE_LOG.info('base.hanfile.....')

		maxBat=os.path.join(self.G_POOL,r'script\max\max.bat')
		pluginBat=os.path.join(self.G_POOL,r'script\max\plugin.bat')
		analyseBat=os.path.join(self.G_POOL,r'script\max\analyse.bat')
		analyseMs=os.path.join(self.G_POOL,r'script\max\renderbus2.ms')
		maxscript='c:/script/max'
		
		copyScriptCmd1='xcopy /y /f "'+maxBat+'" "'+maxscript+'/" '
		copyScriptCmd2='xcopy /y /f "'+pluginBat+'" "'+maxscript+'/" '
		copyScriptCmd3='xcopy /y /f "'+analyseBat+'" "'+maxscript+'/" '
		copyScriptCmd4='xcopy /y /f "'+analyseMs+'" "'+maxscript+'/" '
		
		self.RBcmd(copyScriptCmd1)
		self.RBcmd(copyScriptCmd2)
		self.RBcmd(copyScriptCmd3)
		self.RBcmd(copyScriptCmd4)
		
		tempFile=os.path.join(self.G_POOL,r'temp',self.G_USERID,'analyse',self.G_TASKID,'*.*')
		copyPoolCmd='c:\\fcopy\\FastCopy.exe /speed=full /force_close  /no_confirm_stop /force_start "'+tempFile.replace('/','\\')+'" /to="'+self.G_ANALYSE_WORK_TASK.replace('/','\\')+'"'		
		self.RBcmd(copyPoolCmd)
		
		
	def RBreadanalyseTxt(self):#4
		print 'read Txt....'
		renderTxt=self.G_ANALYSE_TXT
		txtFile=open(renderTxt, 'r')
		allLines=txtFile.readlines()

		for eachLine in allLines:
			if eachLine.startswith('#') or eachLine=='\n':
				continue
			execStr='self.'+eachLine.strip()
			print execStr
			exec(execStr)
			
			
	def RBanalyseConfig(self):#5
		print 'Base..renderConfig....'
		#multicatter = getattr(self,'G_CG_MULTISCATTER_VERSION')
		if hasattr(self,'G_CG_MULTISCATTER_VERSION'):
			configMultCmd='c:/script/max/plugin.bat "'+self.G_CG_VERSION+'" '+' multiscatter ' +self.G_CG_MULTISCATTER_VERSION
			self.RBcmd(configMultCmd)
		
		
	def RBanalyse(self):#7
		print 'Base...render...'
		
		cgFile = os.path.join(self.G_ANALYSE_WORK_TASK,self.G_CG_FILE)
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,(self.G_CG_TXT+'_net.txt'))
		
		cgFile=cgFile.replace('\\','/')
		netFile=netFile.replace('\\','/')
		analyseCmd='c:/script/max/analyse.bat "'+self.G_CG_VERSION+'" "'+self.G_CG_RENDER_VERSION+'" ' + self.G_USERID+' '+self.G_TASKID + ' "' +cgFile+'" "'+netFile+'" '
		self.RBcmd(analyseCmd)
		
		self.G_ANALYSE_LOG.info('Analyse completed!')
		
		
	def RBhanResult(self):#8
		print 'Base...hanResult....'
		netFile = os.path.join(self.G_ANALYSE_WORK_TASK,self.G_CG_TXT,'_net.txt')
		errFile = os.path.join(self.G_ANALYSE_WORK_TASK,self.G_CG_TXT,'_err.txt')
		if  os.path.exists(netFile) and (not os.path.exists(errFile)):#copy ok
			copyCmd='xcopy /y /f "'+netFile+'" "'+self.G_PATH_COST+'/" '
			self.RBcmd(copyCmd)
		else:
			#error
			sys.exit(-1)
		
	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		print str(continueOnErr)+'--->>>'+str(myShell)
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
		
		self.G_ANALYSE_LOG.info(resultStr)
		self.G_ANALYSE_LOG.info(str(resultCode))
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(0)
		return resultStr
		
	def RBexecute(self):#total
		print 'Base...execute.....'
		self.G_ANALYSE_LOG.info('Render...')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBhanFile()
		self.RBreadanalyseTxt()
		self.RBanalyseConfig()
		self.RBanalyse()
		self.RBhanResult()
		

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
		self.G_ANALYSE_LOG.info('Render...')
		self.RBmakeDir()
		self.RBinitLog()
		self.RBhanFile()
		self.RBreadanalyseTxt()
		self.RBanalyseConfig()
		self.RBanalyse()
		self.RBhanResult()
		

#---------------------calss maya--------------------		
class Maya(Base):
	def __init__(self,**paramDict):
		Base.__init__(self,**paramDict)
		print "Maya INIT"

	def RBexecute(self):#Render
		print 'Maya...exec....'

		
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