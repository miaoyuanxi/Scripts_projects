
#encoding:utf-8
import os,sys,shutil
print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
if not os.path.exists(nodePyDir):
    os.makedirs(nodePyDir)

shutil.copy(renderSilkroadPy,nodePyDir)
print 'copyBasePy...end'
sys.path.append(nodePyDir)
from RenderMaxYCX import RenderMaxYCX
if(__name__=="__main__"):
    paramDict = {'sourceFolder':sourceFolder,'scriptFile':scriptFile,'maxFolderName':MAX_FOLDER_NAME,'envPath':envPath,'workRender':workRender,'bPath':bPath,'maxB':maxB,'programFiles':programFiles,'maxVersion':maxVersion,'pluginDict':pluginDict,'logPath':logPath}
    #RenderSilkroad.main(**paramDict)
    render=RenderMaxYCX(**paramDict)
    print 'G_POOL_NAME___'
    render.run()
