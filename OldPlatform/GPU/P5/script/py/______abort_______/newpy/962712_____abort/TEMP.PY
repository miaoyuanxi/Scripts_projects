
    def RBrenderConfig(self):#5
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.start.....]')

        netRenderTxt=os.path.join(self.PLUGINS_MAX_SCRIPT,self.G_USERID,'netrender.txt').replace('\\','/')
        if not os.path.exists(netRenderTxt):
            self.substPath()

        if self.argsmap.has_key('currentTask'):
            self.CURRENT_TASK=self.argsmap['currentTask']

        customerScriptPath=os.path.join(self.G_MAXSCRIPT,self.G_USERID).replace('\\','/')
        
        if self.G_CG_VERSION=='3ds Max 2012' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2009':
            self.G_MAXSCRIPT_NAME='rendera.ms'
        customerMs=os.path.join(customerScriptPath,self.G_MAXSCRIPT_NAME).replace('\\','/')
        customBat=os.path.join(customerScriptPath,G_CUSTOM_BAT_NAME).replace('\\','/')
        
        self.G_PROCESS_LOG.info('customBat------'+customBat)
        self.G_PROCESS_LOG.info('maxscriptName------'+self.G_MAXSCRIPT_NAME)
        self.G_RAYVISION_MAXMS=os.path.join(self.G_MAXSCRIPT,self.G_MAXSCRIPT_NAME).replace('\\','/')
        if os.path.exists(customerMs):
            self.G_RAYVISION_MAXMS=customerMs

        #----------delete max log----------
        userprofile=os.environ["userprofile"]
        maxEnu=userprofile+'\\AppData\\Local\\Autodesk\\3dsMax\\'+self.G_CG_VERSION.replace('3ds Max ','')+' - 64bit\\enu'
        maxlog=maxEnu+'\\Network\\Max.log'
        if os.path.exists(maxlog):
            try:
                os.remove(maxlog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
        
        #----------delete vary log----------
        userTempFile=os.environ["temp"]
        myTempVrayLog=os.path.join(userTempFile,'vraylog.txt').replace('\\','/')
        if os.path.exists(myTempVrayLog):
            try:
                os.remove(myTempVrayLog)
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
                
        #----------Customer 3dsmax.ini----------
        try:
            maxIni=os.path.join(self.G_MAX_B,'ini/3dsmax',self.G_CG_VERSION,'3dsmax.ini').replace('\\','/')
            if os.path.exists(maxIni) and os.path.exists(maxEnu) :
                copyMaxiniCmd='xcopy /y /v /f "'+maxIni +'" "'+maxEnu.replace('\\','/')+'/"' 
                self.RBcmd(copyMaxiniCmd)
            maxUserIni=os.path.join(self.G_MAX_B,'ini/3dsmax',self.G_USERID,self.G_CG_VERSION,'3dsmax.ini').replace('\\','/')
            if os.path.exists(maxUserIni) and os.path.exists(maxEnu) :
                copyMaxiniCmd='xcopy /y /v /f "'+maxUserIni +'" "'+maxEnu.replace('\\','/')+'/"' 
                self.RBcmd(copyMaxiniCmd)
        except Exception, e:
            self.G_PROCESS_LOG.info('[err].3dsmaxIni Exception')
            self.G_PROCESS_LOG.info(e)
            
        #----------load max plugin----------
        maxPlugin=MaxPlugin(self.G_PROCESS_LOG,self.G_MAX_B,self.maxPluginIniPath,self.G_CG_VERSION,self.localMaxPath,self.RBgetPluginDict())
        maxPlugin.config()
        
        userHostFile=os.path.join(customerScriptPath,self.G_USER_HOST_NAME).replace('\\','/')
        self.RBconfigHost(userHostFile)
        self.G_PROCESS_LOG.info('[Max.RBrenderConfig.end.....]')