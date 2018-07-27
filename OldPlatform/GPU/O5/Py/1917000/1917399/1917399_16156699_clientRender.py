#encoding:utf-8
G_CG_NAME='MaxClient'
G_USERID_PARENT='1917000'
G_USERID='1917399'
G_TASKID='16156699'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\temp\16156699_render\cfg\py.cfg'
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917399'
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
##name=1917399_16156699_render.py
##requirements=|OS-Windows
##category=SH
##level=50
##customer=1917399
##nodelimit=5
##nodeblacklimit=3
##constraints=|10_90_100_103
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0604' '604' '604' '1' '' '' '0' '1'
##'frame0605' '605' '605' '1' '' '' '0' '1'
##'frame0606' '606' '606' '1' '' '' '0' '1'
##'frame0607' '607' '607' '1' '' '' '0' '1'
##'frame0608' '608' '608' '1' '' '' '0' '1'
##'frame0609' '609' '609' '1' '' '' '0' '1'
##'frame0610' '610' '610' '1' '' '' '0' '1'
##'frame0611' '611' '611' '1' '' '' '0' '1'
##'frame0612' '612' '612' '1' '' '' '0' '1'
##'frame0613' '613' '613' '1' '' '' '0' '1'
##'frame0614' '614' '614' '1' '' '' '0' '1'
##'frame0615' '615' '615' '1' '' '' '0' '1'
##'frame0616' '616' '616' '1' '' '' '0' '1'
##'frame0617' '617' '617' '1' '' '' '0' '1'
##'frame0618' '618' '618' '1' '' '' '0' '1'
##'frame0619' '619' '619' '1' '' '' '0' '1'
##'frame0620' '620' '620' '1' '' '' '0' '1'
##'frame0621' '621' '621' '1' '' '' '0' '1'
##'frame0622' '622' '622' '1' '' '' '0' '1'
##'frame0623' '623' '623' '1' '' '' '0' '1'
##'frame0624' '624' '624' '1' '' '' '0' '1'
##'frame0625' '625' '625' '1' '' '' '0' '1'
##'frame0626' '626' '626' '1' '' '' '0' '1'
##'frame0627' '627' '627' '1' '' '' '0' '1'
##'frame0628' '628' '628' '1' '' '' '0' '1'
##'frame0629' '629' '629' '1' '' '' '0' '1'
##'frame0630' '630' '630' '1' '' '' '0' '1'
##'frame0631' '631' '631' '1' '' '' '0' '1'
##'frame0632' '632' '632' '1' '' '' '0' '1'
##'frame0633' '633' '633' '1' '' '' '0' '1'
##'frame0634' '634' '634' '1' '' '' '0' '1'
##'frame0635' '635' '635' '1' '' '' '0' '1'
##'frame0636' '636' '636' '1' '' '' '0' '1'
##'frame0637' '637' '637' '1' '' '' '0' '1'
##'frame0638' '638' '638' '1' '' '' '0' '1'
##'frame0639' '639' '639' '1' '' '' '0' '1'
##'frame0640' '640' '640' '1' '' '' '0' '1'
##'frame0641' '641' '641' '1' '' '' '0' '1'
##'frame0642' '642' '642' '1' '' '' '0' '1'
##'frame0643' '643' '643' '1' '' '' '0' '1'
##'frame0644' '644' '644' '1' '' '' '0' '1'
##'frame0645' '645' '645' '1' '' '' '0' '1'
##'frame0646' '646' '646' '1' '' '' '0' '1'
##'frame0647' '647' '647' '1' '' '' '0' '1'
##'frame0648' '648' '648' '1' '' '' '0' '1'
##'frame0649' '649' '649' '1' '' '' '0' '1'
##'frame0650' '650' '650' '1' '' '' '0' '1'
##'frame0651' '651' '651' '1' '' '' '0' '1'
##'frame0652' '652' '652' '1' '' '' '0' '1'
##'frame0653' '653' '653' '1' '' '' '0' '1'
##'frame0654' '654' '654' '1' '' '' '0' '1'
##'frame0655' '655' '655' '1' '' '' '0' '1'
##'frame0656' '656' '656' '1' '' '' '0' '1'
##'frame0657' '657' '657' '1' '' '' '0' '1'
##'frame0658' '658' '658' '1' '' '' '0' '1'
##'frame0659' '659' '659' '1' '' '' '0' '1'
##'frame0660' '660' '660' '1' '' '' '0' '1'
##'frame0661' '661' '661' '1' '' '' '0' '1'
##'frame0662' '662' '662' '1' '' '' '0' '1'
##'frame0663' '663' '663' '1' '' '' '0' '1'
##'frame0664' '664' '664' '1' '' '' '0' '1'
##'frame0665' '665' '665' '1' '' '' '0' '1'
##'frame0666' '666' '666' '1' '' '' '0' '1'
##'frame0667' '667' '667' '1' '' '' '0' '1'
##'frame0668' '668' '668' '1' '' '' '0' '1'
##'frame0669' '669' '669' '1' '' '' '0' '1'
##'frame0670' '670' '670' '1' '' '' '0' '1'
##'frame0671' '671' '671' '1' '' '' '0' '1'
##'frame0672' '672' '672' '1' '' '' '0' '1'
##'frame0673' '673' '673' '1' '' '' '0' '1'
##'frame0674' '674' '674' '1' '' '' '0' '1'
##'frame0675' '675' '675' '1' '' '' '0' '1'
##'frame0676' '676' '676' '1' '' '' '0' '1'
##'frame0677' '677' '677' '1' '' '' '0' '1'
##'frame0678' '678' '678' '1' '' '' '0' '1'
##'frame0679' '679' '679' '1' '' '' '0' '1'
##'frame0680' '680' '680' '1' '' '' '0' '1'
##'frame0681' '681' '681' '1' '' '' '0' '1'
##'frame0682' '682' '682' '1' '' '' '0' '1'
##'frame0683' '683' '683' '1' '' '' '0' '1'
##'frame0684' '684' '684' '1' '' '' '0' '1'
##'frame0685' '685' '685' '1' '' '' '0' '1'
##'frame0686' '686' '686' '1' '' '' '0' '1'
##'frame0687' '687' '687' '1' '' '' '0' '1'
##'frame0688' '688' '688' '1' '' '' '0' '1'
##'frame0689' '689' '689' '1' '' '' '0' '1'
##'frame0690' '690' '690' '1' '' '' '0' '1'
##'frame0691' '691' '691' '1' '' '' '0' '1'
##'frame0692' '692' '692' '1' '' '' '0' '1'
##'frame0693' '693' '693' '1' '' '' '0' '1'
##'frame0694' '694' '694' '1' '' '' '0' '1'
##'frame0695' '695' '695' '1' '' '' '0' '1'
##'frame0696' '696' '696' '1' '' '' '0' '1'
##'frame0697' '697' '697' '1' '' '' '0' '1'
##'frame0698' '698' '698' '1' '' '' '0' '1'
##'frame0699' '699' '699' '1' '' '' '0' '1'
##'frame0700' '700' '700' '1' '' '' '0' '1'
##'frame0701' '701' '701' '1' '' '' '0' '1'
##'frame0702' '702' '702' '1' '' '' '0' '1'
##'frame0703' '703' '703' '1' '' '' '0' '1'
##'frame0704' '704' '704' '1' '' '' '0' '1'
##'frame0705' '705' '705' '1' '' '' '0' '1'
##'frame0706' '706' '706' '1' '' '' '0' '1'
##'frame0707' '707' '707' '1' '' '' '0' '1'
##'frame0708' '708' '708' '1' '' '' '0' '1'
##'frame0709' '709' '709' '1' '' '' '0' '1'
##'frame0710' '710' '710' '1' '' '' '0' '1'
##'frame0711' '711' '711' '1' '' '' '0' '1'
##'frame0712' '712' '712' '1' '' '' '0' '1'
##'frame0713' '713' '713' '1' '' '' '0' '1'
##'frame0714' '714' '714' '1' '' '' '0' '1'
##'frame0715' '715' '715' '1' '' '' '0' '1'
##'frame0716' '716' '716' '1' '' '' '0' '1'
##'frame0717' '717' '717' '1' '' '' '0' '1'
##'frame0718' '718' '718' '1' '' '' '0' '1'
##'frame0719' '719' '719' '1' '' '' '0' '1'
##'frame0720' '720' '720' '1' '' '' '0' '1'
##'frame0721' '721' '721' '1' '' '' '0' '1'
##'frame0722' '722' '722' '1' '' '' '0' '1'
##'frame0723' '723' '723' '1' '' '' '0' '1'
##'frame0724' '724' '724' '1' '' '' '0' '1'
##'frame0725' '725' '725' '1' '' '' '0' '1'
##'frame0726' '726' '726' '1' '' '' '0' '1'
##'frame0727' '727' '727' '1' '' '' '0' '1'
##'frame0728' '728' '728' '1' '' '' '0' '1'
##'frame0729' '729' '729' '1' '' '' '0' '1'
##'frame0730' '730' '730' '1' '' '' '0' '1'
##'frame0731' '731' '731' '1' '' '' '0' '1'
##'frame0732' '732' '732' '1' '' '' '0' '1'
##'frame0733' '733' '733' '1' '' '' '0' '1'
##'frame0734' '734' '734' '1' '' '' '0' '1'
##'frame0735' '735' '735' '1' '' '' '0' '1'
##'frame0736' '736' '736' '1' '' '' '0' '1'
##'frame0737' '737' '737' '1' '' '' '0' '1'
##'frame0738' '738' '738' '1' '' '' '0' '1'
##'frame0739' '739' '739' '1' '' '' '0' '1'
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
##ENDJOBS

##END
