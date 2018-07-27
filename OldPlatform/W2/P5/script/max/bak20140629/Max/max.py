#encoding:utf-8
import os,sys,subprocess,string,logging
import Tkinter as TK
import ttk as TTK
import xml.dom.minidom as DOM
import win32gui
import wmi


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

logging.basicConfig(filename='c:/oomax.log',level=logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s')
'''
todo
考虑从服务器拷贝插件，
从服务器或者本地拷贝XML配置文件
根据XML配置智能加载插件
'''
class Max:
	def __init__(self,master):
		frame=TK.Frame(master)
		frame.pack()
		
		self.maxDict=self.readXML()
		maxs = self.maxDict.keys()
		
		maxList = self.maxDict['maxList']
		'''
		for max in maxs :			
			maxList.append(max)
		maxList.sort(reverse = True)
		'''
		
		self.label=TK.Label(frame,text="打开3ds Max",font='14').grid(row=0,columnspan=2)
		
		self.label2=TK.Label(frame,text="3ds Max").grid(row=1,column=0,sticky=TK.E)
		maxTex = TK.StringVar(frame,'选择max版本')
		self.maxListbox=TTK.Combobox(frame,  textvariable=maxTex,values=maxList,state='readonly')	
		self.maxListbox.current(0)
		self.maxListbox.bind("<<ComboboxSelected>>", self.pluginHandler)
		self.maxListbox.grid(row=1,column=1)
		
		self.label3=TK.Label(frame,text="Vray").grid(row=2,column=0,sticky=TK.E)
		vrTex = TK.StringVar(frame,'选择Vray')
		self.vrListbox=TTK.Combobox(frame,text=vrTex,values=['选择Vray'],state='readonly')		
		self.vrListbox.grid(row=2,column=1)
		
		self.label4=TK.Label(frame,text="Multiscatter").grid(row=3,column=0,sticky=TK.E)
		msTex = TK.StringVar(frame,'Select Multiscatter')
		self.msListbox=TTK.Combobox(frame,text=msTex,values=['Select Multiscatter'],state='readonly')	
		self.msListbox.grid(row=3,column=1)
		
		self.maxBtn =TK.Button(frame,text='打 开',width=8,height=1, font='16',command=self.sub)
		self.maxBtn.grid(row=4,columnspan=2,sticky=TK.E)
		
		
		self.msgLabel=TK.Label(frame,text='',fg='red').grid(row=5,columnspan=2,sticky=TK.W)
		
		
	def readXML(self):
		maxDict = {}
		xmlPath,filename = os.path.split(os.path.abspath(sys.argv[0]))
		xmlPath=os.path.join(xmlPath,'max.xml')
		logging.info('xmlPath..'+xmlPath)
		maxDoc = DOM.parse(xmlPath)
		maxs = maxDoc.getElementsByTagName('max')
		maxList=[]
		for max in maxs:
			maxName = max.getAttribute('name')			
			pluginDict ={}
			plugins = max.childNodes
			for plugin in plugins:
				if plugin.nodeType==maxDoc.ELEMENT_NODE:
					pluginList=[]
					pluginName = plugin.nodeName
					
					pp = plugin.childNodes
					for p in pp:
						if p.nodeType==maxDoc.ELEMENT_NODE:
							
							pluginList.append(p.childNodes[0].nodeValue)
					pluginDict[pluginName]=pluginList
			maxDict[maxName]=pluginDict	
			maxList.append(maxName)
		maxDict['maxList']=maxList
		
		return maxDict


		
	
	
	def checkProcess(self,processName):
		c = wmi.WMI ()
		maxList=[]
		for process in c.Win32_Process (name=processName):
			print "%5s  %s" % (process.ProcessId, process.Name)
			
			maxList.append(process.ExecutablePath.replace('\\','/'))
		return maxList

	def sub(self):
		maxVersion=self.maxListbox.get()
		vrVersion=str(self.vrListbox.get())
		msVersion=self.msListbox.get()
		logging.info('maxVersion..'+maxVersion)
		logging.info('vrVersion..'+vrVersion)
		logging.info('msVersion..'+msVersion)
		
		if maxVersion=='':
			win32gui.MessageBox(0,self.code('请选择需要打开的max版本'),self.code('错误'),0)
		else:
			maxExe = 'C:/Program Files/Autodesk/'+maxVersion+'/3dsmax.exe'
			
			hasMaxProcess = 'false'
			maxList = self.checkProcess('3dsmax.exe')
			for maxe in maxList:
				print maxe
				if maxe==maxExe:
					hasMaxProcess='true'
					break
					
			if hasMaxProcess=='true' :
				print 'has max2012.......'
				if win32gui.MessageBox(0,self.code('当前版本的max进程已打开，\n可能会造成切换版本或加载插件失败，\n请关掉对应版本的MAX再切换'),self.code('错误'),4)==6:
					print 'yes...'
					self.openMax()
				else:
					print 'no...'
			else:
				self.openMax()
			
	def openMax(self):
		maxVersion=self.maxListbox.get()
		vrVersion=str(self.vrListbox.get())
		msVersion=self.msListbox.get()

		maxPath = 'C:/Program Files/Autodesk/'+maxVersion+'/'
		
		maxIni = maxPath +'plugin.ini'
		if maxVersion=='3ds Max 2014' or maxVersion=='3ds Max 2013':
			maxIni = maxPath +'en-US/plugin.ini'
		
		standIni = 'C:/PLUGINS/ini/standard/'+maxVersion+'.ini'
		print ("maxIni.."+maxIni)
		if vrVersion!='' and vrVersion.startswith('vray'):
			#env
			pathEnv = os.environ['path']
			resultEnv='C:/PLUGINS/vray/'+vrVersion+'/'+maxVersion+';'+pathEnv
			os.environ['path']=resultEnv
			#ini
			pluginIni = 'C:/PLUGINS/ini/vray/'+vrVersion+'/'+maxVersion+'/plugin.ini'
			subprocess.call(['c:/concat.exe',maxIni,standIni,pluginIni])
			
		else:
			subprocess.call(['c:/concat.exe',maxIni,standIni])#ini
		
		print "----------plugin-----------"
		print msVersion
		if msVersion!='' and msVersion.startswith('multiscatter') :
			source='C:/PLUGINS/multiscatter/'+msVersion+"/"+maxVersion+'/*'
			print source+"-->>" + maxPath
			subprocess.call(['xcopy','/y','/f','/e',source,maxPath])
		
		batPath,batName = os.path.split(os.path.abspath(sys.argv[0]))
		batPath = os.path.join(batPath,'del.bat')
		logging.info('batPath..'+batPath)
		if os.path.exists(batPath):
			shortMaxVersion=maxVersion.replace('3ds Max ','')
			print shortMaxVersion
			delBat = batPath + " " + shortMaxVersion
			os.system(delBat)
		max=maxPath+'3dsmax.exe'
		logging.info('openMax..'+max)
		subprocess.Popen(max)
	
	def code(self,str):
		type = sys.getfilesystemencoding()
		str2 = str.decode('UTF-8').encode(type)
		return str2
	
	def pluginHandler(self,event):
		
		maxVersion=self.maxListbox.get()
		pluginDict = self.maxDict[maxVersion]
		vrList = pluginDict['vray']
		msList = pluginDict['multiscatter']
		self.vrListbox['values']=[]
		self.msListbox['values']=[]
		self.vrListbox['values']=vrList
		self.msListbox['values']=msList
		
		
		
		
win=TK.Tk()
win.title('3ds Max')
win.geometry('300x150')
icoPath,icoName = os.path.split(os.path.abspath(sys.argv[0]))
icoPath=os.path.join(icoPath,'dk.ico')
win.iconbitmap(icoPath)
max=Max(win)
win.mainloop()