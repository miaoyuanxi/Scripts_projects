#encoding:utf-8
import os,sys,subprocess,string,logging,time,shutil
class AA():

	def __init__(self):
		self.G_MERGEPIC_SCRIPT_NAME='mergepic.ms'
		self.G_MERGEPIC_BAT_NAME='mergepic.bat'
		self.G_ANALYSE_WORK='C:/WORK/analyse'
		
		
		self.G_WORK_TASK_CFG=os.path.join(self.G_ANALYSE_WORK_TASK,'cfg')
		
		self.G_WORK_TASK_TEMP = os.path.join(self.G_ANALYSE_WORK_TASK,'temp')
		self.G_WORK_TASK_RESULT=os.path.join(self.G_ANALYSE_WORK_TASK,'result')
		

	def RBcmd(self,cmdStr,continueOnErr=False,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
		print cmdStr
		
		cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
		cmdp.stdin.write('3/n')
		cmdp.stdin.write('4/n')
		while cmdp.poll()==None:
			resultLine = cmdp.stdout.readline().strip()
			
		resultStr = cmdp.stdout.read()
		resultCode = cmdp.returncode
		
		
		if not continueOnErr:
			if resultCode!=0:
				sys.exit(0)
		return resultStr
	

		
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
	
	def RBBackupPy(self):
		runPyPath,runPyName = os.path.split(os.path.abspath(sys.argv[0]))
		tempRunPy=os.path.join(runPyPath,runPyName)
		
		copyPyCmd='xcopy /y /f "'+tempRunPy+'" "'+self.G_WORK_TASK_CFG+'/" '
		workTaskRunPy=os.path.join(self.G_WORK_TASK_CFG,runPyName)
		runBatName=os.path.basename(runPyName)+'.bat'
		runBat=os.path.join(self.G_WORK_TASK_CFG,runBatName)
		fileHandle=open(runBat,'a')
		fileHandle.write('c:/python27/python.exe '+workTaskRunPy+' "'+self.G_SYS_ARGVS[1]+'" "'+self.G_SYS_ARGVS[2]+'" "'+self.G_SYS_ARGVS[3]+'" "'+self.G_SYS_ARGVS[4]+'" "'+self.G_SYS_ARGVS[5])+'"'
		fileHandle.close()
		
	
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

		
a=AA()
--a.RBconvertSmallPic()