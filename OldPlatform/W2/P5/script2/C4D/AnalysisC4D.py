#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import AnalysisBase

reload(sys)
sys.setdefaultencoding('utf-8')

class C4D(AnalysisBase):
    def __init__(self,**paramDict):
        AnalysisBase.__init__(self,**paramDict)
        print "c4d.INIT"
        print "c4d argv"+sys.argv[5]
        self.G_ANALYSE_LOG.info('[c4d argv]'+sys.argv[5])
        
        self.CGV=''
        
    def RBhanFile(self):#3 copy script,copy from pool,#unpack
        self.G_ANALYSE_LOG.info('[c4d.RBhanFile.start.....]')

        self.G_ANALYSE_LOG.info('[c4d.RBhanFile.end.....]')
        
    def RBconfig(self):#5
        self.G_ANALYSE_LOG.info('[c4d.RBconfig.start.....]')
        self.G_ANALYSE_LOG.info('[c4d.RBconfig.end.....]')
        self.G_ANALYSE_LOG.info('\n')

    def copyPyp(self):
        '''
        1.loading custom analyse config 
        '''
        cconfig_path = r"B:\\plugins\\C4D\\script\\cconfigs\\" + self.G_USERID
        print('copy_cconfig_path: %s' % cconfig_path)
        code="R13_05DFD2A0";
        if self.CGV=="R14":
            code="R14_4A9E4467"
        if self.CGV=="R15":
            code="R15_53857526"
        if self.CGV=="R16":
            code="R16_14AF56B1"
        if self.CGV=="R17":
            code="R17_8DE13DAD"
        if self.CGV=="R18":
            code="R18_62A5E681"
        if self.CGV=="R19":
            code="R19_BFE04C39"
                
        if not os.path.exists(cconfig_path):
            source = r"B:\\plugins\\C4D\\script\\Analys.pyp"
            path = r"C:\\users\\enfuzion\\AppData\\Roaming\\MAXON\\CINEMA 4D " + code + "\\plugins\\"
            self.pythonCopy(source,path)
            print(111)
        else:
            source = cconfig_path + "\\Analys.pyp"
            path = r"C:\\users\\enfuzion\\AppData\\Roaming\\MAXON\\CINEMA 4D " + code + "\\plugins\\"
            self.pythonCopy(source,path)
            print(2222)
        
        '''
        source_R19 = r"B:\\plugins\\C4D\\script\\Analys_R19.pyp"
        if self.CGV=="R19":
            self.pythonCopy(source_R19,path)
        else:
            self.pythonCopy(source,path)
        '''

    def plugin(self):
        self.G_ANALYSE_LOG.info('[self.G_PLUGINS.....]'+self.G_PLUGINS)
        if os.path.exists(self.G_PLUGINS):
            configJson=eval(open(self.G_PLUGINS, "r").read())
            if isinstance(configJson["plugins"],dict):
                node=self.getNode()
                myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
                for key in configJson["plugins"]:
                    cmd = r'B:\\plugins\\C4D\\script\\plugin.bat "'+myCgVersion+'" "'+key+'" "'+configJson["plugins"][key]+'" "'+node+'"'
                    self.RBcmd(cmd,True,False,myLog=True)

    def getNode(self):
        node=sys.argv[5]
        if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
            return "ABCDEF"
        if "K" in node:
            return "K"
        if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
            return "LNOPQ"
        if "G" in node or "H" in node or "J" in node:
            return "GHJ"
        return "ABCDEF"
    
    def setPluginByPyFile(self):
        self.G_ANALYSE_LOG.info('\n')
        self.G_ANALYSE_LOG.info('[c4d.Plugin.config.start...]')
        self.G_ANALYSE_LOG.info('[c4d.配置插件.开始...]'.decode('utf-8').encode('gbk'))
        
        if os.path.exists(self.G_PLUGINS):
            configJson = eval(open(self.G_PLUGINS, "r").read())
            self.G_ANALYSE_LOG.info(configJson)
            if isinstance(configJson["plugins"], dict):
                node = self.getNode()
                myCgVersion = configJson["renderSoftware"] + " " + configJson["softwareVer"]
                
                '''
                2.加载自定义插件脚本 loading custom C4DCustomPluginManager config
                '''
                #custom_script_name = 'C4DCustomPluginManager.py' 
                plugin_custom_script = 'B:/plugins/C4D/script/cconfigs/%s' % (str(self.G_USERID))
                if os.path.exists(plugin_custom_script):#判断文件夹是否存在
                    self.G_ANALYSE_LOG.info('plugin_custom_script: %s' % plugin_custom_script)
                    self.G_ANALYSE_LOG.info("loading custom config!!!")
                    sys.path.append(plugin_custom_script)
                    try:
                        from C4DCustomPluginManager import C4DPlugin, C4DPluginManagerCenter
                    except ImportError:
                        pass
                else:
                    self.G_ANALYSE_LOG.info("loading default config!!!")
                    from C4DPluginManager import C4DPlugin, C4DPluginManagerCenter
                '''
                loading default C4DPluginManager
                '''
                
                plugin_mgr = C4DPluginManagerCenter(self.G_USERID)
                #plugin_mgr.copy_R18_exe(myCgVersion)
                #self.G_ANALYSE_LOG.info('copy_R18_exe.done...')
                #self.G_ANALYSE_LOG.info('R18的64bit拷贝完成...'.decode('utf-8').encode('gbk'))
                for key in configJson["plugins"]:
                    plugin = C4DPlugin()
                    plugin.plugin_name = key
                    plugin.plugin_version = configJson["plugins"][key]
                    plugin.soft_version = configJson["renderSoftware"] + ' ' + configJson["softwareVer"]
                    plugin.node = node
                    
                    self.G_ANALYSE_LOG.info('[ python = C:\\Python27\\python.exe "B:\\plugins\\C4D\\script\\C4DPluginManager.py" "%s" "%s" "%s" "%s" ]' % (plugin.plugin_name, \
                                                                                plugin.plugin_version, \
                                                                                plugin.soft_version, \
                                                                                plugin.node))
     
                    #plugin_list.append(plugin)  
                    plugin_mgr.get_dll(plugin.soft_version)
                    self.G_ANALYSE_LOG.info('[c4d.libmmd.dll copy done..]')
                    self.G_ANALYSE_LOG.info('[c4d.R19.053 copy done..]')
                    
                    result = plugin_mgr.set_custom_env(plugin)

                #result = plugin_mgr.set_custom_envs(plugin_list)             
        
        self.G_ANALYSE_LOG.info('[c4d.Plugin.config.end...]')
        self.G_ANALYSE_LOG.info('[c4d.配置插件.结束...]'.decode('utf-8').encode('gbk'))
        self.G_ANALYSE_LOG.info('\n')
    
    '''
    def setPluginByPyFile(self):
        if os.path.exists(self.G_PLUGINS):
            configJson=eval(open(self.G_PLUGINS, "r").read())
            if isinstance(configJson["plugins"],dict):
                node=self.getNode()
                myCgVersion = configJson["renderSoftware"] +" "+configJson["softwareVer"]
                for key in configJson["plugins"]:
                    self.setPluginByVersion(myCgVersion,key,configJson["plugins"][key],node)
        self.setCustomePlugin()

    def setPluginByVersion(self,softVersion,plugin,pluginVersion,node):
        nomalFilePath = "B:\\plugins\\C4D\\script\\SetCfdPlugin_Normal.py"
        if os.path.exists(nomalFilePath):
            #result = execfile(nomalFilePath)
            cmd = 'python "'+ nomalFilePath +'" "'+softVersion+'" "'+plugin+'" "'+pluginVersion+'" "'+node+'"'
            self.RBcmd(cmd,True,False)
            #if result==1:
                #otherFilePath = "B:\\plugins\\C4D\\other_script\\"+plugin+"\\"+pluginVersion.replace(" ","_")+"\\"+softVersion+"\\SetCfdPlugin_other.py"
                #if os.path.exists(otherFilePath):
                    #execfile(otherFilePath,softVersion,plugin,pluginVersion,node)
                #else:
                    #self.G_RENDER_LOG.info('[C4D pluginFile not exist....otherFilePath--.]'+otherFilePath)
        else:
            self.G_ANALYSE_LOG.info('[C4D pluginFile not exist.....nomalFilePath---]'+nomalFilePath)

    def setCustomePlugin(self):
        customFilePath = "B:\\plugins\\C4D\\script\\custom_script\\"+self.G_USERID+"\\SetCfdPlugin_custom.py"
        if os.path.exists(customFilePath):
            #result = execfile(customFilePath)
            cmd = 'python "'+ customFilePath +'"'
            self.RBcmd(cmd,True,False)
        else:
            self.G_ANALYSE_LOG.info('[C4D pluginFile not exist.....customFilePath---]'+customFilePath)    
    '''

    def RBanalyse(self):#7
        self.G_ANALYSE_LOG.info('[c4d.RBanalyse.start...]')
        self.G_ANALYSE_LOG.info('[c4d.cmd命令分析.开始...]'.decode('utf-8').encode('gbk'))
        netFile = os.path.join(self.G_WORK_TASK,(self.G_CG_TXTNAME+'_net.txt'))
        netFile=netFile.replace('\\','/')

        myCgVersion = "CINEMA 4D "+self.CGV
        """
        loading custom C4D.bat
        """
        cconfig_path = "B:/plugins/C4D/script/cconfigs/" + self.G_USERID + "/C4D.bat"
        self.G_ANALYSE_LOG.info('cconfig_path: %s' % cconfig_path)
        
        c4dbat_default='B:/plugins/C4D/script/C4D.bat'

        #14.0.361
        c4dExePath=os.path.join(r'C:\Program Files\MAXON',myCgVersion,'CINEMA 4D 64 Bit.exe')
        self.G_ANALYSE_LOG.info('IMAGENAME = ' + os.environ.get('IMAGENAME'))
        if os.path.exists(c4dExePath) == False:
            self.G_ANALYSE_LOG.error(c4dExePath + ' is not exists!!!')
            self.G_ANALYSE_LOG.error('IMAGENAME = ' + os.environ.get('IMAGENAME'))
            return
        
        analyseCmd=c4dbat_default+' "'+myCgVersion+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '
        
        if os.path.exists(cconfig_path):
            analyseCmd=cconfig_path+' "'+myCgVersion+'" "'+self.G_TASKID+'" "' +self.CGFILE+'" "'+netFile+'" '+self.G_USERID

        self.G_ANALYSE_LOG.info('cmds: %s' % analyseCmd)
        self.RBcmd(analyseCmd,True,False,myLog=True)
        self.G_ANALYSE_LOG.info('[c4d.RBanalyse.end...]')
        self.G_ANALYSE_LOG.info('[c4d.cmd命令分析.结束...]'.decode('utf-8').encode('gbk'))
        self.G_ANALYSE_LOG.info('\n')

    def webNetPath(self):
        if os.path.exists(self.G_CONFIG):
            configJson=eval(open(self.G_CONFIG, "r").read())
            self.CGFILE=configJson['common']["cgFile"]
            self.CGSOFT=configJson['common']["cgSoftName"]
            self.CGV=configJson['common']["cgv"]
            self.RTASKID=configJson['common']["taskId"]
            print configJson
            if isinstance(configJson["mntMap"],dict):
                self.RBcmd("net use * /del /y",myLog=True)
                for key in configJson["mntMap"]:
                    # self.RBcmd("net use "+key+" "+configJson["mntMap"][key].replace('/','\\'))
                    self.RBcmd("net use "+key+" \""+configJson["mntMap"][key].replace('/','\\')+"\"",myLog=True)
        
    def RBexecute(self):#Render
        self.G_ANALYSE_LOG.info('[c4d.RBexecute.start...]')
        self.G_ANALYSE_LOG.info('[c4d.分析.开始...]'.decode('utf-8').encode('gbk'))
        self.RBBackupPy()
        self.RBinitLog()
        self.RBmakeDir()
        self.delSubst()
        self.webNetPath()
        self.RBprePy()
        self.RBcopyTempFile()#copy py.cfg max file
        self.RBreadCfg()
        self.RBhanFile()
        self.RBconfig()    
        self.copyPyp()    
        #self.plugin()
        self.setPluginByPyFile()
        self.RBanalyse()
        self.RBpostPy()
        self.RBhanResult()
        self.G_ANALYSE_LOG.info('[c4d.RBexecute.end...]')
        self.G_ANALYSE_LOG.info('[c4d.分析.完成...]'.decode('utf-8').encode('gbk'))