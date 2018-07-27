import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Houdini(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
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