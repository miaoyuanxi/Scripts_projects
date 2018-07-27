#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16157984'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r''
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917342'
G_VRAY_LICENSE='1'
#script_param_mark#
import os,sys,shutil


print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
if G_RENDEROS=='Linux':
    nodePyDir=r'/root/rayvision/script/py'
if not os.path.exists(nodePyDir):
    os.makedirs(nodePyDir)
    
    

def copyPyFolder(pyFolder):
    if os.path.exists(pyFolder):
        for root, dirs, files in os.walk(pyFolder):
            print 'copyBasePy...'
            for i in xrange (0, files.__len__()):
                sf = os.path.join(root, files[i])
                shutil.copy(sf,nodePyDir)
                
def copyFolder(source,target):
    if not os.path.exists(target):
        os.makedirs(target)
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            print 'copyBasePy...'
            for dirname in  dirs:
                tdir=os.path.join(root,dirname)
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
            for i in xrange (0, files.__len__()):
                sf = os.path.join(root, files[i])
                folder=target+root[len(source):len(root)]+"/"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                shutil.copy(sf,folder)
                

cgList=['Nuke','Preprocess','Max','MaxClient','Merge','Blender','C4D','Lightwave','Clarisse','SketchUp','Vue','Vray','OctaneRender','Softimage','Mrstand','Maya','MayaPre','MayaClient','Houdini','Katana','Keyshot']#preprocess,maxclient
if G_CG_NAME in cgList:
#if os.path.exists(scriptCg):
    if G_CG_NAME == 'Preprocess' or G_CG_NAME == 'MaxClient' or G_CG_NAME == 'Merge':
        G_CG_NAME_PATH = 'Max'
    elif G_CG_NAME == 'MayaPre' or G_CG_NAME == 'MayaClient':
        G_CG_NAME_PATH = 'Maya'
    else:
        G_CG_NAME_PATH = G_CG_NAME
    script2=G_POOL+'/script2'
    scriptBase=script2+'/Base'
    scriptCg=script2+'/'+G_CG_NAME_PATH
    scriptUtil=script2+'/Util'
    scriptNodeBase=nodePyDir+'/Base'
    scriptNodeCg=nodePyDir+'/'+G_CG_NAME_PATH
    scriptNodeUtil=nodePyDir+'/Util'
    print script2
    print scriptBase
    print scriptCg
    print scriptUtil

    userRenderPy=script2+'/user/'+G_USERID
    try:
        shutil.rmtree(nodePyDir)
    except:
        pass
    copyFolder(scriptBase,scriptNodeBase)
    copyFolder(scriptCg,scriptNodeCg)
    copyFolder(scriptUtil,scriptNodeUtil)
    copyFolder(userRenderPy,nodePyDir)
    sys.path.append(scriptNodeBase)
else:
    copyPyFolder(baseRenderPy)
    copyPyFolder(userRenderPy)

print 'copyBasePy...end'

sys.path.append(nodePyDir)

import RenderAction


if(__name__=="__main__"):
    paramDict = {'G_JOB_ID':G_JOB_ID,'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_NODE_PY':nodePyDir,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS,'G_RENDEROS':G_RENDEROS,'G_CG_TILE':G_CG_TILE,'G_CG_TILECOUNT':G_CG_TILECOUNT}
    try:
        paramDict['G_SCHEDULER_CLUSTER_ID']=G_SCHEDULER_CLUSTER_ID
    except:
        pass
        
    try:
        paramDict['G_SCHEDULER_CLUSTER_NODES']=G_SCHEDULER_CLUSTER_NODES
    except:
        pass
        
    try:
        paramDict['G_HOUDINI_TYPE']=G_HOUDINI_TYPE
    except:
        pass
        
    try:
        paramDict['G_VRAY_LICENSE']=G_VRAY_LICENSE
    except:
        pass
    RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=1917342_16157984_render.py
##requirements=|OS-Windows
##category=SH
##level=79
##custom=1917342
##nodelimit=20
##nodeblacklimit=3
##constraints=10_90_100_101
##priority=20
##autorestartlimit=4
##jobdurationlimit=3600
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0740' '740' '740' '1' '' '' '0' '1'
##'frame0741' '741' '741' '1' '' '' '0' '1'
##'frame0742' '742' '742' '1' '' '' '0' '1'
##'frame0743' '743' '743' '1' '' '' '0' '1'
##'frame0744' '744' '744' '1' '' '' '0' '1'
##'frame0745' '745' '745' '1' '' '' '0' '1'
##'frame0746' '746' '746' '1' '' '' '0' '1'
##'frame0747' '747' '747' '1' '' '' '0' '1'
##'frame0748' '748' '748' '1' '' '' '0' '1'
##'frame0749' '749' '749' '1' '' '' '0' '1'
##'frame0750' '750' '750' '1' '' '' '0' '1'
##'frame0751' '751' '751' '1' '' '' '0' '1'
##'frame0752' '752' '752' '1' '' '' '0' '1'
##'frame0753' '753' '753' '1' '' '' '0' '1'
##'frame0754' '754' '754' '1' '' '' '0' '1'
##'frame0755' '755' '755' '1' '' '' '0' '1'
##'frame0756' '756' '756' '1' '' '' '0' '1'
##'frame0757' '757' '757' '1' '' '' '0' '1'
##'frame0758' '758' '758' '1' '' '' '0' '1'
##'frame0759' '759' '759' '1' '' '' '0' '1'
##'frame0760' '760' '760' '1' '' '' '0' '1'
##'frame0761' '761' '761' '1' '' '' '0' '1'
##'frame0762' '762' '762' '1' '' '' '0' '1'
##'frame0763' '763' '763' '1' '' '' '0' '1'
##'frame0764' '764' '764' '1' '' '' '0' '1'
##'frame0765' '765' '765' '1' '' '' '0' '1'
##'frame0766' '766' '766' '1' '' '' '0' '1'
##'frame0767' '767' '767' '1' '' '' '0' '1'
##'frame0768' '768' '768' '1' '' '' '0' '1'
##'frame0769' '769' '769' '1' '' '' '0' '1'
##'frame0770' '770' '770' '1' '' '' '0' '1'
##'frame0771' '771' '771' '1' '' '' '0' '1'
##'frame0772' '772' '772' '1' '' '' '0' '1'
##'frame0773' '773' '773' '1' '' '' '0' '1'
##'frame0774' '774' '774' '1' '' '' '0' '1'
##'frame0775' '775' '775' '1' '' '' '0' '1'
##'frame0776' '776' '776' '1' '' '' '0' '1'
##'frame0777' '777' '777' '1' '' '' '0' '1'
##'frame0778' '778' '778' '1' '' '' '0' '1'
##'frame0779' '779' '779' '1' '' '' '0' '1'
##'frame0780' '780' '780' '1' '' '' '0' '1'
##'frame0781' '781' '781' '1' '' '' '0' '1'
##'frame0782' '782' '782' '1' '' '' '0' '1'
##'frame0783' '783' '783' '1' '' '' '0' '1'
##'frame0784' '784' '784' '1' '' '' '0' '1'
##'frame0785' '785' '785' '1' '' '' '0' '1'
##'frame0786' '786' '786' '1' '' '' '0' '1'
##'frame0787' '787' '787' '1' '' '' '0' '1'
##'frame0788' '788' '788' '1' '' '' '0' '1'
##'frame0789' '789' '789' '1' '' '' '0' '1'
##'frame0790' '790' '790' '1' '' '' '0' '1'
##'frame0791' '791' '791' '1' '' '' '0' '1'
##'frame0792' '792' '792' '1' '' '' '0' '1'
##'frame0793' '793' '793' '1' '' '' '0' '1'
##'frame0794' '794' '794' '1' '' '' '0' '1'
##'frame0795' '795' '795' '1' '' '' '0' '1'
##'frame0796' '796' '796' '1' '' '' '0' '1'
##'frame0797' '797' '797' '1' '' '' '0' '1'
##'frame0798' '798' '798' '1' '' '' '0' '1'
##'frame0799' '799' '799' '1' '' '' '0' '1'
##'frame0800' '800' '800' '1' '' '' '0' '1'
##'frame0801' '801' '801' '1' '' '' '0' '1'
##'frame0802' '802' '802' '1' '' '' '0' '1'
##'frame0803' '803' '803' '1' '' '' '0' '1'
##'frame0804' '804' '804' '1' '' '' '0' '1'
##'frame0805' '805' '805' '1' '' '' '0' '1'
##'frame0806' '806' '806' '1' '' '' '0' '1'
##'frame0807' '807' '807' '1' '' '' '0' '1'
##'frame0808' '808' '808' '1' '' '' '0' '1'
##'frame0809' '809' '809' '1' '' '' '0' '1'
##'frame0810' '810' '810' '1' '' '' '0' '1'
##'frame0811' '811' '811' '1' '' '' '0' '1'
##'frame0812' '812' '812' '1' '' '' '0' '1'
##'frame0813' '813' '813' '1' '' '' '0' '1'
##'frame0814' '814' '814' '1' '' '' '0' '1'
##'frame0815' '815' '815' '1' '' '' '0' '1'
##'frame0816' '816' '816' '1' '' '' '0' '1'
##'frame0817' '817' '817' '1' '' '' '0' '1'
##'frame0818' '818' '818' '1' '' '' '0' '1'
##'frame0819' '819' '819' '1' '' '' '0' '1'
##'frame0820' '820' '820' '1' '' '' '0' '1'
##'frame0821' '821' '821' '1' '' '' '0' '1'
##'frame0822' '822' '822' '1' '' '' '0' '1'
##'frame0823' '823' '823' '1' '' '' '0' '1'
##'frame0824' '824' '824' '1' '' '' '0' '1'
##'frame0825' '825' '825' '1' '' '' '0' '1'
##'frame0826' '826' '826' '1' '' '' '0' '1'
##'frame0827' '827' '827' '1' '' '' '0' '1'
##'frame0828' '828' '828' '1' '' '' '0' '1'
##'frame0829' '829' '829' '1' '' '' '0' '1'
##'frame0830' '830' '830' '1' '' '' '0' '1'
##'frame0831' '831' '831' '1' '' '' '0' '1'
##'frame0832' '832' '832' '1' '' '' '0' '1'
##'frame0833' '833' '833' '1' '' '' '0' '1'
##'frame0834' '834' '834' '1' '' '' '0' '1'
##'frame0835' '835' '835' '1' '' '' '0' '1'
##'frame0836' '836' '836' '1' '' '' '0' '1'
##'frame0837' '837' '837' '1' '' '' '0' '1'
##'frame0838' '838' '838' '1' '' '' '0' '1'
##'frame0839' '839' '839' '1' '' '' '0' '1'
##'frame0840' '840' '840' '1' '' '' '0' '1'
##'frame0841' '841' '841' '1' '' '' '0' '1'
##'frame0842' '842' '842' '1' '' '' '0' '1'
##'frame0843' '843' '843' '1' '' '' '0' '1'
##'frame0844' '844' '844' '1' '' '' '0' '1'
##'frame0845' '845' '845' '1' '' '' '0' '1'
##'frame0846' '846' '846' '1' '' '' '0' '1'
##'frame0847' '847' '847' '1' '' '' '0' '1'
##'frame0848' '848' '848' '1' '' '' '0' '1'
##'frame0849' '849' '849' '1' '' '' '0' '1'
##'frame0850' '850' '850' '1' '' '' '0' '1'
##'frame0851' '851' '851' '1' '' '' '0' '1'
##'frame0852' '852' '852' '1' '' '' '0' '1'
##'frame0853' '853' '853' '1' '' '' '0' '1'
##'frame0854' '854' '854' '1' '' '' '0' '1'
##'frame0855' '855' '855' '1' '' '' '0' '1'
##'frame0856' '856' '856' '1' '' '' '0' '1'
##'frame0857' '857' '857' '1' '' '' '0' '1'
##'frame0858' '858' '858' '1' '' '' '0' '1'
##'frame0859' '859' '859' '1' '' '' '0' '1'
##'frame0860' '860' '860' '1' '' '' '0' '1'
##'frame0861' '861' '861' '1' '' '' '0' '1'
##'frame0862' '862' '862' '1' '' '' '0' '1'
##'frame0863' '863' '863' '1' '' '' '0' '1'
##'frame0864' '864' '864' '1' '' '' '0' '1'
##'frame0865' '865' '865' '1' '' '' '0' '1'
##'frame0866' '866' '866' '1' '' '' '0' '1'
##'frame0867' '867' '867' '1' '' '' '0' '1'
##'frame0868' '868' '868' '1' '' '' '0' '1'
##'frame0869' '869' '869' '1' '' '' '0' '1'
##'frame0870' '870' '870' '1' '' '' '0' '1'
##'frame0871' '871' '871' '1' '' '' '0' '1'
##'frame0872' '872' '872' '1' '' '' '0' '1'
##'frame0873' '873' '873' '1' '' '' '0' '1'
##'frame0874' '874' '874' '1' '' '' '0' '1'
##'frame0875' '875' '875' '1' '' '' '0' '1'
##'frame0876' '876' '876' '1' '' '' '0' '1'
##'frame0877' '877' '877' '1' '' '' '0' '1'
##'frame0878' '878' '878' '1' '' '' '0' '1'
##'frame0879' '879' '879' '1' '' '' '0' '1'
##'frame0880' '880' '880' '1' '' '' '0' '1'
##'frame0881' '881' '881' '1' '' '' '0' '1'
##'frame0882' '882' '882' '1' '' '' '0' '1'
##'frame0883' '883' '883' '1' '' '' '0' '1'
##'frame0884' '884' '884' '1' '' '' '0' '1'
##'frame0885' '885' '885' '1' '' '' '0' '1'
##'frame0886' '886' '886' '1' '' '' '0' '1'
##'frame0887' '887' '887' '1' '' '' '0' '1'
##'frame0888' '888' '888' '1' '' '' '0' '1'
##'frame0889' '889' '889' '1' '' '' '0' '1'
##'frame0890' '890' '890' '1' '' '' '0' '1'
##'frame0891' '891' '891' '1' '' '' '0' '1'
##'frame0892' '892' '892' '1' '' '' '0' '1'
##'frame0893' '893' '893' '1' '' '' '0' '1'
##'frame0894' '894' '894' '1' '' '' '0' '1'
##'frame0895' '895' '895' '1' '' '' '0' '1'
##'frame0896' '896' '896' '1' '' '' '0' '1'
##'frame0897' '897' '897' '1' '' '' '0' '1'
##'frame0898' '898' '898' '1' '' '' '0' '1'
##'frame0899' '899' '899' '1' '' '' '0' '1'
##'frame0900' '900' '900' '1' '' '' '0' '1'
##'frame0901' '901' '901' '1' '' '' '0' '1'
##'frame0902' '902' '902' '1' '' '' '0' '1'
##'frame0903' '903' '903' '1' '' '' '0' '1'
##'frame0904' '904' '904' '1' '' '' '0' '1'
##'frame0905' '905' '905' '1' '' '' '0' '1'
##'frame0906' '906' '906' '1' '' '' '0' '1'
##'frame0907' '907' '907' '1' '' '' '0' '1'
##'frame0908' '908' '908' '1' '' '' '0' '1'
##'frame0909' '909' '909' '1' '' '' '0' '1'
##'frame0910' '910' '910' '1' '' '' '0' '1'
##'frame0911' '911' '911' '1' '' '' '0' '1'
##'frame0912' '912' '912' '1' '' '' '0' '1'
##'frame0913' '913' '913' '1' '' '' '0' '1'
##'frame0914' '914' '914' '1' '' '' '0' '1'
##'frame0915' '915' '915' '1' '' '' '0' '1'
##'frame0916' '916' '916' '1' '' '' '0' '1'
##'frame0917' '917' '917' '1' '' '' '0' '1'
##'frame0918' '918' '918' '1' '' '' '0' '1'
##'frame0919' '919' '919' '1' '' '' '0' '1'
##'frame0920' '920' '920' '1' '' '' '0' '1'
##'frame0921' '921' '921' '1' '' '' '0' '1'
##'frame0922' '922' '922' '1' '' '' '0' '1'
##'frame0923' '923' '923' '1' '' '' '0' '1'
##'frame0924' '924' '924' '1' '' '' '0' '1'
##'frame0925' '925' '925' '1' '' '' '0' '1'
##'frame0926' '926' '926' '1' '' '' '0' '1'
##'frame0927' '927' '927' '1' '' '' '0' '1'
##'frame0928' '928' '928' '1' '' '' '0' '1'
##'frame0929' '929' '929' '1' '' '' '0' '1'
##'frame0930' '930' '930' '1' '' '' '0' '1'
##'frame0931' '931' '931' '1' '' '' '0' '1'
##'frame0932' '932' '932' '1' '' '' '0' '1'
##'frame0933' '933' '933' '1' '' '' '0' '1'
##'frame0934' '934' '934' '1' '' '' '0' '1'
##'frame0935' '935' '935' '1' '' '' '0' '1'
##'frame0936' '936' '936' '1' '' '' '0' '1'
##'frame0937' '937' '937' '1' '' '' '0' '1'
##'frame0938' '938' '938' '1' '' '' '0' '1'
##'frame0939' '939' '939' '1' '' '' '0' '1'
##'frame0940' '940' '940' '1' '' '' '0' '1'
##'frame0941' '941' '941' '1' '' '' '0' '1'
##'frame0942' '942' '942' '1' '' '' '0' '1'
##'frame0943' '943' '943' '1' '' '' '0' '1'
##'frame0944' '944' '944' '1' '' '' '0' '1'
##'frame0945' '945' '945' '1' '' '' '0' '1'
##'frame0946' '946' '946' '1' '' '' '0' '1'
##'frame0947' '947' '947' '1' '' '' '0' '1'
##'frame0948' '948' '948' '1' '' '' '0' '1'
##'frame0949' '949' '949' '1' '' '' '0' '1'
##'frame0950' '950' '950' '1' '' '' '0' '1'
##'frame0951' '951' '951' '1' '' '' '0' '1'
##'frame0952' '952' '952' '1' '' '' '0' '1'
##'frame0953' '953' '953' '1' '' '' '0' '1'
##'frame0954' '954' '954' '1' '' '' '0' '1'
##'frame0955' '955' '955' '1' '' '' '0' '1'
##'frame0956' '956' '956' '1' '' '' '0' '1'
##'frame0957' '957' '957' '1' '' '' '0' '1'
##'frame0958' '958' '958' '1' '' '' '0' '1'
##'frame0959' '959' '959' '1' '' '' '0' '1'
##'frame0960' '960' '960' '1' '' '' '0' '1'
##'frame0961' '961' '961' '1' '' '' '0' '1'
##'frame0962' '962' '962' '1' '' '' '0' '1'
##'frame0963' '963' '963' '1' '' '' '0' '1'
##'frame0964' '964' '964' '1' '' '' '0' '1'
##'frame0965' '965' '965' '1' '' '' '0' '1'
##'frame0966' '966' '966' '1' '' '' '0' '1'
##'frame0967' '967' '967' '1' '' '' '0' '1'
##'frame0968' '968' '968' '1' '' '' '0' '1'
##'frame0969' '969' '969' '1' '' '' '0' '1'
##'frame0970' '970' '970' '1' '' '' '0' '1'
##ENDJOBS

##END
