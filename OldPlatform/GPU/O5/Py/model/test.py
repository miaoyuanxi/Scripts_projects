import sys
import os,shutil
G_JOB_ID = 'frame0004'
G_CG_START_FRAME = '4'
G_CG_END_FRAME = '4'
G_CG_BY_FRAME = '1'
G_CG_LAYER_NAME = ''
G_CG_OPTION = ''
#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='119000'
G_USERID='119365'
G_TASKID='3058'
G_POOL=r'\\10.50.19.150\p5'

print 'LQ_copyBasePy...start'
baseHelperPy=r'\\10.50.19.150\p5\script\py\BaseHelper.py'
baseRenderPy=r'\\10.50.19.150\p5\script\py\BaseRender.py'
nodePyDir=r'c:\script\py'
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
shutil.copy(baseRenderPy,nodePyDir)
shutil.copy(baseHelperPy,nodePyDir)
print 'copyBasePy...end'
sys.path.append(r'c:\script\py')
sys.path.append(r'D:\work\render\3058\cfg')

import BaseRender
#import MayaClient

from BaseRender import MayaClient












#-----------------------Render----------------------------------------
# abc
class MYRenderAction():
	def __init__(self,**paramDict):
		cgName=paramDict['G_CG_NAME']
		print 'cgName=================='+cgName
		exec('MYRenderAction.__bases__=('+cgName+',)')
		exec(cgName+'.__init__(self,**paramDict)')
		#Base.__init__(self,**paramDict)
	
	def RBrender(self):#7
		self.G_RENDER_LOG.info('[-----==-==-=-UUSER_Maya.RBrender.start----------]')
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
		#self.RBcmd(renderCmd,True,False)
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_RENDER_LOG.info('[---------------------------==-==-=-USER_Maya.RBrender.end----------]')
		
	def RBexecute(self):#Render
		self.RBBackupPy()
		self.RBinitLog()
		self.G_RENDER_LOG.info('[USER-MAYA.RBexecute.start...]')
		self.RBprePy()
		self.RBmakeDir()
		self.G_RENDER_LOG.info('[-----------------------USER-MAYA------------------]')
		self.RBcopyTempFile()
		self.RBreadCfg()
		self.RBhanFile()
		
		
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		
		print 'test........................'
		#self.G_RENDER_LOG.info('[Maya.RBexecute.end.....]')
		
		
		
if(__name__=="__main__"):
	paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION}
	#BaseRender.main(**paramDict)
	render=MYRenderAction(**paramDict)
	print 'G_POOL_NAME___'+render.G_POOL
	render.RBexecute()
