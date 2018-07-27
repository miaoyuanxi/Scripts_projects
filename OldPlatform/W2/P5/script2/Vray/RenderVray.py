#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
import string
import logging
import time
import shutil
import threading
from socket import *
from RenderBase import RenderBase
class Vray(RenderBase):
	def __init__(self,**paramDict):
		RenderBase.__init__(self,**paramDict)
		print "Vray INIT"
		self.cgfile=""
		self.outputFileName=""
		self.projectPath=""
		self.cgv=""
		self.G_LOCAL_IP = ''
		self.G_NODE_PY = paramDict['G_NODE_PY']
		# platform
		# self.G_PLATFORM = ''
		# platform_dict = {'10':'1000','9':'1002','5':'1005','8':'1008','19':'1009','16':'1016'}
		# for key,values in platform_dict.items():
			# if self.G_TASKID.startswith(key):
				# self.G_PLATFORM = values
				
		# vray distribute
		self.VRAY_DISTRIBUTE=False
		if paramDict.has_key('G_SCHEDULER_CLUSTER_NODES'):
			self.G_SCHEDULER_CLUSTER_NODES = paramDict['G_SCHEDULER_CLUSTER_NODES']
			if self.G_SCHEDULER_CLUSTER_NODES:
				self.VRAY_DISTRIBUTE=True
		print "VRAY_DISTRIBUTE:" + str(self.VRAY_DISTRIBUTE)
		
	def webNetPath(self):
		self.G_PROCESS_LOG.info('[Vray.webNetPath.start.....]')
		if os.path.exists(self.G_CONFIG):
			configJson=eval(open(self.G_CONFIG, "r").read())
			print configJson
			self.cgfile=configJson['common']["cgFile"]
			self.outputFileName=configJson['common']["outputFileName"]
			self.iformat=configJson['common']["iformat"]
			self.cgName=configJson['common']["cgSoftName"]
			projectName= configJson['common']["projectSymbol"]
			replacePath="\\"+projectName+"\\"+self.cgName+"\\"
			if isinstance(configJson["mntMap"],dict):
				self.RBcmd("net use * /del /y",myLog=True)
				for key in configJson["mntMap"]:
					newPath =configJson["mntMap"][key].replace("/","\\").replace(replacePath,"\\")
					# self.RBcmd("net use "+key+" "+newPath)
					net_use_cmd = "net use "+key+" \""+newPath+"\""
					self.RBcmd(net_use_cmd.decode(sys.getdefaultencoding()).encode(sys.getfilesystemencoding()),myLog=True)
		self.G_PROCESS_LOG.info('[Vray.webNetPath.end.....]') 

	def getPlugin(self):
		self.G_PROCESS_LOG.info('[Vray.getPlugin.start.....]')
		if os.path.exists(self.G_PLUGINS):
			configJson=eval(open(self.G_PLUGINS, "r").read())
			if isinstance(configJson["plugins"],dict):
				for key in configJson["plugins"]:
					self.pluginName=key
					self.pluginVersion=configJson["plugins"][key]
		self.G_PROCESS_LOG.info('[Vray.getPlugin.end.....]')

	def parseFileName(self,nameStr,frames):
		if "#" in nameStr:
			nameArray=nameStr.split(" ")
			name=nameArray[0]
			end=name.rindex("#")+1
			start=name.index("#")
			restr=name[start:end]
			frameStr=self.formatFrame(frames,"0",end-start,False)
			return name.replace(restr,frameStr)
		else:
			return nameStr

	def formatFrame(self,frame,fillstr,length,append):
		s=frame
		for i in range(length-len(frame)):
			if append:
				s=s+fillstr
			else:
				s=fillstr+s
		return s
	
	'''
		copy文件
	'''
	def RBcopyTempFile(self):
		self.RBlog('拷贝配置文件','start')
		self.RBlog('拷贝以下配置文件：')
		self.G_PROCESS_LOG.info('[Vray.RBcopyTempFile.start.....]')
		
		if vars(self).has_key('G_CONFIG'):
			self.pythonCopy(self.G_CONFIG.replace('\\','/'),self.G_RENDER_WORK_TASK_CFG.replace('\\','/'))
		if vars(self).has_key('G_PLUGINS'):
			self.pythonCopy(self.G_PLUGINS.replace('\\','/'),self.G_RENDER_WORK_TASK_CFG.replace('\\','/'))
			
		tempFull=self.G_POOL_TASK
		self.RBlog(tempFull)
		#if self.G_RENDEROS=='Linux':
		#    tempFull=self.G_POOL_TASK
		self.pythonCopy(tempFull.replace('\\','/'),self.G_RENDER_WORK_TASK.replace('\\','/'))
		self.G_PROCESS_LOG.info('[Vray.RBcopyTempFile.end.....]')
		self.RBlog('done','end')
	
	def RBrenderConfig(self):
		self.G_PROCESS_LOG.info('[Vray.RBrenderConfig.start.....]')
		
		#send cmd to node ip
		self.vrayDistributeNode()
		
		#wait node's vray.exe server to start
		self.waitDistributeNode()
		
		self.G_PROCESS_LOG.info('[Vray.RBrenderConfig.end.....]') 
	
	def RBrender(self):#7
		self.G_PROCESS_LOG.info('[Vray.RBrender.start.....]')
		startTime = time.time()
		self.G_FEE_LOG.info('startTime='+str(int(startTime)))

		output = self.G_RENDER_WORK_OUTPUT.replace('/','\\')+"\\"+self.outputFileName.replace(':','')+"."+self.iformat
		filePath=self.parseFileName(self.cgfile,self.G_CG_START_FRAME)
		# bat='B:\\plugins\\V-Ray_standalone\\vray_stan.bat'
		# renderCmd=bat+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+self.pluginName.replace(" for x64","")+'" "'+self.pluginVersion.replace("Vray ","")+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+filePath+'" "'+output+'"'
		
		is_distribute = '0'
		render_ip_num = 1
		render_ip = self.G_LOCAL_IP
		if self.VRAY_DISTRIBUTE:
			is_distribute = '1'
			render_ip_num = len(self.G_SCHEDULER_CLUSTER_NODES.split(',')) + 1  # master ip + node ip
			render_ip = self.G_LOCAL_IP + ',' + self.G_SCHEDULER_CLUSTER_NODES
		
		bat = 'B:\\plugins\\V-Ray_standalone\\vraystandalone_distribute_render.bat'
		#B:\plugins\V-Ray_standalone\vraystandalone_distribute_render.bat "18627910" "147285" "Standalone" "vray 3.20.03" "1" "1" "1" "E:\dxStudio\1507703396284.vrscene" "D:\1507624710979.jpg" "1" "11" "127.0.0.1;10.60.70.151;10.60.70.152;10.60.70.153;10.60.70.154;10.60.70.155;10.60.70.156;10.60.70.157;10.60.70.191;10.60.70.192;10.60.70.193"
		renderCmd = bat+' "'+self.G_USERID+'" "'+self.G_TASKID+'" "'+self.pluginName.replace(" for x64","")+'" "'+self.pluginVersion+'" "'+self.G_CG_START_FRAME+'" "' + self.G_CG_END_FRAME +'" "'+self.G_CG_BY_FRAME +'" "'+filePath+'" "'+output+'" "'+is_distribute+'" "'+str(render_ip_num)+'" "'+render_ip.replace(',',';')+'"'
		
		self.G_PROCESS_LOG.info(renderCmd)
		self.RBcmd(renderCmd,True,False)
		
		#rename %taskid%_render.log --> frame0001_render.log
		src_log_name = os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_TASKID+'_render.log'))
		dest_log_name = os.path.join(self.G_LOG_WORK,self.G_TASKID,(self.G_JOB_NAME+'_render.log'))
		os.rename(src_log_name,dest_log_name)
		
		endTime = time.time()
		self.G_FEE_LOG.info('endTime='+str(int(endTime)))
		self.G_PROCESS_LOG.info('[Vray.RBrender.end.....]')
	
	# Wait for the node computer's vray.exe service to start
	def waitDistributeNode(self):
		if self.VRAY_DISTRIBUTE:
			self.G_PROCESS_LOG.info('[Vray.waitDistributeNode.start....]')
			vray_node_ip_list = []    #list of node ip that started vray.exe server
			
			def check_vray_cmd(thread_name,node_ip):
				self.G_PROCESS_LOG.info("%s begin: %s\n" % (thread_name,time.ctime(time.time())))
				username = 'enfuzion'
				if self.G_PLATFORM == '1008':
					password = 'abc123456'
				elif self.G_PLATFORM == '1009':
					password = 'ruiyun2017'
				else:
					password = 'ruiyun2016'
				check_cmd = 'tasklist /S %s /U %s /P %s /FI "IMAGENAME eq vray.exe"' % (node_ip,username,password)
				cmdp = subprocess.Popen(check_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
				while cmdp.poll()==None:
					result_str = cmdp.stdout.read().strip()
					if result_str!='' and 'vray.exe' in result_str:
						self.G_PROCESS_LOG.info(result_str)
						if node_ip not in vray_node_ip_list:
							vray_node_ip_list.append(node_ip)
					
				resultCode = cmdp.returncode        
				self.G_PROCESS_LOG.info('resultCode...'+str(resultCode))
				self.G_PROCESS_LOG.info("%s end: %s\n" % (thread_name,time.ctime(time.time())))
				
			node_ip_list = []
			wait_time = 8  #waiting time(min)
			for node_ip in self.G_SCHEDULER_CLUSTER_NODES.split(','):
				node_ip_list.append(node_ip)
			self.G_PROCESS_LOG.info('node ip list:%s' % node_ip_list)
			node_ip_num = len(node_ip_list)  #numbers of node ip
			if node_ip_list:
				for i in range(wait_time):
					thread_list = []  #thread list
					for node_ip in node_ip_list:                
						t = threading.Thread(target=check_vray_cmd,args=("Check vray.exe-%s" % (node_ip),node_ip))
						thread_list.append(t)
					for t in thread_list:
						t.start()
					for t in thread_list:
						t.join()
						
					while True:
						active_thread_list = threading.enumerate()
						self.G_PROCESS_LOG.info('active thread list:%s' % active_thread_list)
						active_thread_num = threading.active_count()
						if active_thread_num == 1:  #<_MainThread(MainThread, started 4092)>
							break
						time.sleep(5)
					self.G_PROCESS_LOG.info('vray.exe node ip list:%s' % vray_node_ip_list)
					if len(vray_node_ip_list) == node_ip_num:
						break
					else:
						if i == (wait_time - 1):
							if len(vray_node_ip_list)/(node_ip_num*1.0) < 0.6:
								self.G_PROCESS_LOG.info('[err]The percentage of render node machines is less than 60%')
								sys.exit(-1)
					time.sleep(60)
			else:
				self.G_PROCESS_LOG.info('nodeIP_list is empty\n')
			self.G_PROCESS_LOG.info('[Vray.waitDistributeNode.end....]')
	
	def vrayDistributeNode(self):
		def send_cmd(thread_name,local_ip,node_ip):
			self.G_PROCESS_LOG.info("%s start: %s\n" % (thread_name,time.ctime(time.time())))
			
			from_addr = os.path.join(self.G_POOL,'script2','Vray','VrayDistribute.py')
			from_addr_user = os.path.join(self.G_POOL,'script2','User',self.G_USERID,'Vray','VrayDistribute.py')
			if os.path.exists(from_addr_user):
				from_addr = from_addr_user
			to_addr = os.path.normpath('\\\\' + node_ip + '\\' + self.G_NODE_PY.replace(':','$'))
			
			copy_node_script_path='xcopy /Y /V /F "%s" "%s"' % (from_addr,to_addr)
			if not os.path.exists(to_addr):
				os.makedirs(to_addr)
			self.RBcmd(copy_node_script_path,myLog=True)
			
			node_script_path = os.path.join(self.G_NODE_PY,'VrayDistribute.py')
			munu_port = '10001'
			if self.G_PLATFORM == '1016':
				munu_port = '10011'
			run_node_py_cmd='B:/tools/munu_agent_controller.exe %s %s "C:\\Python27\\python.exe %s "%s" "%s" "%s" "c:\\log""' % (node_ip,munu_port,node_script_path,self.PLUGINPATH,self.G_TASKID,local_ip)
			self.RBcmd(run_node_py_cmd,myLog=True)
			
			self.G_PROCESS_LOG.info("%s over: %s\n" % (thread_name,time.ctime(time.time())))

		if self.VRAY_DISTRIBUTE:
			self.G_PROCESS_LOG.info('---------TODO Vray distribute---------') 
			##get IP
			#self.G_LOCAL_IP = gethostbyname(gethostname())  #169.254.41.243
			ipList = gethostbyname_ex(gethostname())  #('GA010', [], ['10.60.1.10', '169.254.41.243'])
			self.G_LOCAL_IP = ipList[2][0]  #get localhost IP：10.60.1.10
			node_ip_list = self.G_SCHEDULER_CLUSTER_NODES.split(',')
			self.G_PROCESS_LOG.info('Master IP:'+self.G_LOCAL_IP)
			self.G_PROCESS_LOG.info('Node IP:'+str(node_ip_list))
			
			thread_list = []  #thread list
			##send command with multi thread
			if node_ip_list:
				for nodeIP in node_ip_list:
					#thread.start_new_thread(send_cmd,("Thread-%s" % (nodeIP),self.G_LOCAL_IP,nodeIP))
					t = threading.Thread(target=send_cmd,args=("Thread-%s" % (nodeIP),self.G_LOCAL_IP,nodeIP))
					thread_list.append(t)
				for t in thread_list:
					t.start()
				for t in thread_list:
					t.join()
			else:
				self.G_PROCESS_LOG.info('node_ip_list is empty\n') 
			time.sleep(30)
		
	def RBexecute(self):#Render
		
		print 'Vray.execute.....'
		self.RBBackupPy()
		self.RBinitLog()
		self.G_PROCESS_LOG.info('[Vray.RBexecute.start.....]')
		self.RBnodeClean()
		self.RBprePy()
		self.copyBlack()
		self.RBmakeDir()
		self.RBcopyTempFile()
		self.delSubst()
		self.webNetPath()
		self.getPlugin()
		self.RBreadCfg()
		self.RBhanFile()
		self.RBrenderConfig()
		self.RBwriteConsumeTxt()
		self.resourceMonitor()
		self.RBrender()
		self.RBconvertSmallPic()
		self.RBhanResult()
		self.RBpostPy()
		self.G_PROCESS_LOG.info('[Blender.RBexecute.end.....]')