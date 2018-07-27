import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase

class Maya(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
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
		
		configJson=eval(open(self.G_CONFIG, "r").read())
		print configJson
		if isinstance(configJson["mntMap"],dict):
			for key in configJson["mntMap"]:
				self.RBcmd("net use * /del /y")
				self.RBcmd("net use "+key+" "+configJson["mntMap"][key])

		
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
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "'+renderTxtFile+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" '
		
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
		renderCmd=renderBat +' "'+self.G_USERID+'"  "'+self.G_TASKID+'"  "'+mayaExePath+'" "" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+ self.G_PATH_INPUTPROJECT +'" "'+ self.G_PATH_INPUTFILE+'" "'+ self.G_CONFIG+'" '
		
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