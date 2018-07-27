import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
from RenderBase import RenderBase
class C4D(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "C4d INIT"
		self.G_IMAGE_WIDTH=""
		self.G_IMAGE_HEIGHT=""
		self.G_IFORMAT=""
		self.outFilePath=""
		self.multiPass=""

	
	def webNetPath(self):
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			self.G_IMAGE_WIDTH=configJson['common']["imageWidth"]
			self.G_IMAGE_HEIGHT=configJson['common']["imageWidth"]
			self.G_IFORMAT=configJson['common']["iformat"]
			self.outFilePath=configJson['common']["outputFileName"]
			self.multiPass=configJson['common']["multiPass"]

			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y")
				for key in configJson["mntMap"]:
					self.RBcmd("net use "+key+" "+configJson["mntMap"][key])

	def RBrender(self):#7
		self.G_RENDER_LOG.info('[C4D.RBrender.start.....]')
		startTime = time.time()
		
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))
		
		myCgVersion = self.G_CG_VERSION
		# if myCgVersion.endswith('.64') :
		# 	myCgVersion=myCgVersion.replace('.64','')
		# if myCgVersion.endswith('.32') :
		# 	myCgVersion=myCgVersion.replace('.32','')
			
		c4dExePath=os.path.join(r'C:\Program Files\MAXON',myCgVersion,'CINEMA 4D 64 Bit.exe')
		self.outFilePath=os.path.join(self.G_RENDER_WORK_OUTPUT,self.G_OUTPUT_FILENMAE)
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