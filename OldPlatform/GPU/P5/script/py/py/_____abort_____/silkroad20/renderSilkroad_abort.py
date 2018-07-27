


sourceFolder=r'\\10.50.1.20\td\huling\Model\Architecture\8e8464a9-9b28-4ad2-b190-0156466131e7'
workRender=r'c:\work\render'
bPath=r'\\10.50.1.22\td'
renderSilkroadPy=r'\\10.50.244.116\p5\script\py\py\silkroad20\RenderSilkroadMax.py'
maxB=r'B:/plugins/max'
programFiles=r'C:/Program Files'
maxVersion=r'3ds Max 2014'
pluginDict=r"{u'3rdPartyShaders': {}, u'renderSoftware': u'3ds Max', u'softwareVer': u'2014', u'plugins': {'vray': u'3.00.03'}}"
logPath=r'C:/LOG/SILKROAD20.TXT'
#encoding:utf-8
import os,sys,shutil
print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
if not os.path.exists(nodePyDir):
    os.makedirs(nodePyDir)

shutil.copy(renderSilkroadPy,nodePyDir)
print 'copyBasePy...end'
sys.path.append(nodePyDir)
from RenderSilkroadMax import RenderSilkroadMax
if(__name__=="__main__"):
    #paramDict = {'sourceFolder':sourceFolder,'workRender':workRender,'bPath':bPath}
    paramDict = {'sourceFolder':sourceFolder,'workRender':workRender,'bPath':bPath,'maxB':maxB,'programFiles':programFiles,'maxVersion':maxVersion,'pluginDict':pluginDict,'logPath':logPath}
    
    #RenderSilkroad.main(**paramDict)
    render=RenderSilkroadMax(**paramDict)
    print 'G_POOL_NAME___'
    render.run()
    

    