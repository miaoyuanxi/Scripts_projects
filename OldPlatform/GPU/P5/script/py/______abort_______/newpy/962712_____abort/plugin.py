
class MaxPlugin():
    def __init__(self,processLog,maxB,iniPath,cgVersion,pluginDict):
        print 'config lugin...'
        
        self.G_LOCAL_AUTODESK='C:/Program Files/Autodesk'
        self.G_PROCESS_LOG=processLog
        self.G_MAX_B=maxB
        self.G_PLUGIN_INI=self.G_MAX_B+'/ini'
        self.G_CG_VERSION=cgVersion
        self.G_PLUGIN_DICT=pluginDict
        #MaxClient.__init__(self,**paramDict)
        print "maxclient-----"
       
    def delete(self):
        print 'config lugin...',self.G_PROCESS_LOG
        self.G_PROCESS_LOG.info('[Max.RVloadPlugin start]')
        self.G_PROCESS_LOG.info('\n\n------------------------------------------------------------[Start Config plugin]--------------------------------------------------------\n\n')
        defDelPath=self.G_MAX_B+ '/script/delFile.bat' 
        print 'defDelPath...',defDelPath
        delCmd='"'+defDelPath+'"'+' '+'"'+self.G_CG_VERSION+'"'
        if os.path.exists(defDelPath):
            self.G_PROCESS_LOG.info('pluginDelCmd------'+defDelPath)
            self.runcmd(delCmd)
            self.G_PROCESS_LOG.info('pluginDelCmd...finished+\n')
            
    
    def getIncludeIni(self):
        self.G_PROCESS_LOG.info('\n\n--------------------------------[Start config ini ]--------------------------------\n\n')
        self.G_PROCESS_LOG.info('getIncludeIni...start------\n')
        standIni=os.path.join(self.G_PLUGIN_INI,'standard',self.G_CG_VERSION,'plugin_include.ini').replace('\\','/')
        includeIniList=[]
        if os.path.exists(standIni):
            f=open(standIni)
            sourceinclude=f.read()
            f.close()
            includeIniList.append(sourceinclude)
            
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:  
                pluginVersion=pluginDict[pluginName]
                pluginPath=os.path.join(self.G_PLUGIN_INI,pluginName,pluginName+pluginVersion,self.G_CG_VERSION,'plugin_include.ini').replace('\\','/')
                if os.path.exists(pluginPath):
                    f=open(pluginPath)
                    sourceinclude=f.read()
                    f.close()
                    includeIniList.append(sourceinclude) 
                
        return includeIniList
        
    def getDirectoryIni(self):
        self.G_PROCESS_LOG.info('getDirectoryIni...start------\n')
        standIni=os.path.join(self.G_PLUGIN_INI,'standard',self.G_CG_VERSION,'plugin_directory.ini')
        directoryIniList=[]
        if os.path.exists(standIni):
            f=open(standIni)
            sourcedirectory=f.read()
            f.close()
            directoryIniList.append(sourcedirectory)
            
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:  
                pluginVersion=pluginDict[pluginName]
                pluginPath=os.path.join(self.G_PLUGIN_INI,pluginName,pluginName+pluginVersion,self.G_CG_VERSION,'plugin_directory.ini').replace('\\','/')
                if os.path.exists(pluginPath):
                    f=open(pluginPath)
                    sourcedirectory=f.read()
                    f.close()
                    directoryIniList.append(sourcedirectory)
        return directoryIniList
        
    def writeIni(self):
        self.G_PROCESS_LOG.info('writeIni...start------\n')
        includeIniList=self.getIncludeIni()
        directoryIniList=self.getDirectoryIni()
        targetPath=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION,'en-US','plugin.ini').replace('\\','/')
        if self.G_CG_VERSION=='3ds Max 2010' or self.G_CG_VERSION=='3ds Max 2011' or self.G_CG_VERSION=='3ds Max 2012':
            targetPath=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION,'plugin.ini').replace('\\','/') 
        if os.path.exists(targetPath):
            os.system('del /s /q "%s"' % (targetPath)) 
            self.G_PROCESS_LOG.info('del ini'+targetPath+'\n')
        self.G_PROCESS_LOG.info('write ini to '+targetPath+'\n')
        f=open(targetPath,'wb')
        if includeIniList: 
            f.write('[Include]'+'\n')
            for includeIni in includeIniList:
                f.write(includeIni+'\n')
            
        if directoryIniList: 
            f.write('[Directory]'+'\n')
            for directoryIni in directoryIniList:
                f.write(directoryIni+'\n')
        self.G_PROCESS_LOG.info('write ini finished\n')
        f.close()    
        self.G_PROCESS_LOG.info('writeIni...end\n')
        
        
    def copyConfigPlugin(self):
        self.G_PROCESS_LOG.info('\n\n--------------------------------[start copy plugin]--------------------------------\n\n')
        allPlugDict=self.G_PLUGIN_DICT
        if allPlugDict and allPlugDict.has_key('plugins'):
            pluginDict=allPlugDict['plugins']
            for pluginName in pluginDict:
                if pluginName=="vray":
                    pluginVersion=pluginDict[pluginName]
                    pluginBatPath=os.path.join(self.G_MAX_B,pluginName,'script',pluginName + '.bat').replace('\\','/')
                    cmdDir='"'+pluginBatPath+'" "'+self.G_CG_VERSION+'" "'+pluginName+'" "'+pluginName+pluginVersion+'" "'+self.G_MAX_B+'"'
                    if os.path.exists(pluginBatPath):
                        self.runcmd(cmdDir)
                    self.G_PROCESS_LOG.info('copyConfigPlugin----'+pluginName+pluginVersion+'\n')
                else:
                    pluginVersion=pluginDict[pluginName]
                    pluginBatPath=os.path.join(self.G_MAX_B,pluginName,'script',pluginName + '.bat').replace('\\','/')
                    cmdDir='"'+pluginBatPath+'" "'+self.G_CG_VERSION+'" "'+pluginName+'" "'+pluginName+pluginVersion+'" "'+self.G_MAX_B+'"'
                    if os.path.exists(pluginBatPath):
                        self.runcmd(cmdDir)
                    else:
                        srcDir=os.path.join(self.G_MAX_B,pluginName,pluginName+pluginVersion,self.G_CG_VERSION).replace('\\','/')
                        dstDir=os.path.join(self.G_LOCAL_AUTODESK,self.G_CG_VERSION).replace('\\','/')
                        os.system('robocopy /e /ns /nc /nfl /ndl /np "%s" "%s"' % (srcDir,dstDir))
                    self.G_PROCESS_LOG.info('copyConfigPlugin----'+pluginName+pluginVersion+'\n')
        self.G_PROCESS_LOG.info('Config Plugin...finished\n')
    
    def runcmd(self,cmdStr):
        cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        while True:
            resultLine=cmdp.stdout.readline()
            if resultLine == '' and cmdp.poll()!=None:
                break
            self.G_PROCESS_LOG.info(resultLine)
        resultCode=cmdp.returncode
        
    def config(self):
        self.delete()
        self.writeIni()
        self.copyConfigPlugin()
        
        