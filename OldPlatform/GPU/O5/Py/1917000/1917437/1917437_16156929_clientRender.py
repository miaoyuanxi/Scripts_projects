#encoding:utf-8
G_CG_NAME='MaxClient'
G_USERID_PARENT='1917000'
G_USERID='1917437'
G_TASKID='16156929'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\temp\16156929_render\cfg\py.cfg'
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917437'
G_VRAY_LICENSE='2'
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
##name=1917437_16156929_render.py
##requirements=|OS-Windows
##category=HW
##level=79
##customer=1917437
##nodelimit=10
##nodeblacklimit=3
##constraints=|10_90_100_102
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame2019' '2019' '2019' '1' '' '' '0' '1'
##'frame2020' '2020' '2020' '1' '' '' '0' '1'
##'frame2021' '2021' '2021' '1' '' '' '0' '1'
##'frame2022' '2022' '2022' '1' '' '' '0' '1'
##'frame2023' '2023' '2023' '1' '' '' '0' '1'
##'frame2024' '2024' '2024' '1' '' '' '0' '1'
##'frame2025' '2025' '2025' '1' '' '' '0' '1'
##'frame2026' '2026' '2026' '1' '' '' '0' '1'
##'frame2027' '2027' '2027' '1' '' '' '0' '1'
##'frame2028' '2028' '2028' '1' '' '' '0' '1'
##'frame2029' '2029' '2029' '1' '' '' '0' '1'
##'frame2030' '2030' '2030' '1' '' '' '0' '1'
##'frame2031' '2031' '2031' '1' '' '' '0' '1'
##'frame2032' '2032' '2032' '1' '' '' '0' '1'
##'frame2033' '2033' '2033' '1' '' '' '0' '1'
##'frame2034' '2034' '2034' '1' '' '' '0' '1'
##'frame2035' '2035' '2035' '1' '' '' '0' '1'
##'frame2036' '2036' '2036' '1' '' '' '0' '1'
##'frame2037' '2037' '2037' '1' '' '' '0' '1'
##'frame2038' '2038' '2038' '1' '' '' '0' '1'
##'frame2039' '2039' '2039' '1' '' '' '0' '1'
##'frame2040' '2040' '2040' '1' '' '' '0' '1'
##'frame2041' '2041' '2041' '1' '' '' '0' '1'
##'frame2042' '2042' '2042' '1' '' '' '0' '1'
##'frame2043' '2043' '2043' '1' '' '' '0' '1'
##'frame2044' '2044' '2044' '1' '' '' '0' '1'
##'frame2045' '2045' '2045' '1' '' '' '0' '1'
##'frame2046' '2046' '2046' '1' '' '' '0' '1'
##'frame2047' '2047' '2047' '1' '' '' '0' '1'
##'frame2048' '2048' '2048' '1' '' '' '0' '1'
##'frame2049' '2049' '2049' '1' '' '' '0' '1'
##'frame2050' '2050' '2050' '1' '' '' '0' '1'
##'frame2051' '2051' '2051' '1' '' '' '0' '1'
##'frame2052' '2052' '2052' '1' '' '' '0' '1'
##'frame2053' '2053' '2053' '1' '' '' '0' '1'
##'frame2054' '2054' '2054' '1' '' '' '0' '1'
##'frame2055' '2055' '2055' '1' '' '' '0' '1'
##'frame2056' '2056' '2056' '1' '' '' '0' '1'
##'frame2057' '2057' '2057' '1' '' '' '0' '1'
##'frame2058' '2058' '2058' '1' '' '' '0' '1'
##'frame2059' '2059' '2059' '1' '' '' '0' '1'
##'frame2060' '2060' '2060' '1' '' '' '0' '1'
##'frame2061' '2061' '2061' '1' '' '' '0' '1'
##'frame2062' '2062' '2062' '1' '' '' '0' '1'
##'frame2063' '2063' '2063' '1' '' '' '0' '1'
##'frame2064' '2064' '2064' '1' '' '' '0' '1'
##'frame2065' '2065' '2065' '1' '' '' '0' '1'
##'frame2066' '2066' '2066' '1' '' '' '0' '1'
##'frame2067' '2067' '2067' '1' '' '' '0' '1'
##'frame2068' '2068' '2068' '1' '' '' '0' '1'
##'frame2069' '2069' '2069' '1' '' '' '0' '1'
##'frame2070' '2070' '2070' '1' '' '' '0' '1'
##'frame2071' '2071' '2071' '1' '' '' '0' '1'
##'frame2072' '2072' '2072' '1' '' '' '0' '1'
##'frame2073' '2073' '2073' '1' '' '' '0' '1'
##'frame2074' '2074' '2074' '1' '' '' '0' '1'
##'frame2075' '2075' '2075' '1' '' '' '0' '1'
##'frame2076' '2076' '2076' '1' '' '' '0' '1'
##'frame2077' '2077' '2077' '1' '' '' '0' '1'
##'frame2078' '2078' '2078' '1' '' '' '0' '1'
##'frame2079' '2079' '2079' '1' '' '' '0' '1'
##'frame2080' '2080' '2080' '1' '' '' '0' '1'
##'frame2081' '2081' '2081' '1' '' '' '0' '1'
##'frame2082' '2082' '2082' '1' '' '' '0' '1'
##'frame2083' '2083' '2083' '1' '' '' '0' '1'
##'frame2084' '2084' '2084' '1' '' '' '0' '1'
##'frame2085' '2085' '2085' '1' '' '' '0' '1'
##'frame2086' '2086' '2086' '1' '' '' '0' '1'
##'frame2087' '2087' '2087' '1' '' '' '0' '1'
##'frame2088' '2088' '2088' '1' '' '' '0' '1'
##'frame2089' '2089' '2089' '1' '' '' '0' '1'
##'frame2090' '2090' '2090' '1' '' '' '0' '1'
##'frame2091' '2091' '2091' '1' '' '' '0' '1'
##'frame2092' '2092' '2092' '1' '' '' '0' '1'
##'frame2093' '2093' '2093' '1' '' '' '0' '1'
##'frame2094' '2094' '2094' '1' '' '' '0' '1'
##'frame2095' '2095' '2095' '1' '' '' '0' '1'
##'frame2096' '2096' '2096' '1' '' '' '0' '1'
##'frame2097' '2097' '2097' '1' '' '' '0' '1'
##'frame2098' '2098' '2098' '1' '' '' '0' '1'
##'frame2099' '2099' '2099' '1' '' '' '0' '1'
##'frame2100' '2100' '2100' '1' '' '' '0' '1'
##'frame2101' '2101' '2101' '1' '' '' '0' '1'
##'frame2102' '2102' '2102' '1' '' '' '0' '1'
##'frame2103' '2103' '2103' '1' '' '' '0' '1'
##'frame2104' '2104' '2104' '1' '' '' '0' '1'
##'frame2105' '2105' '2105' '1' '' '' '0' '1'
##'frame2106' '2106' '2106' '1' '' '' '0' '1'
##'frame2107' '2107' '2107' '1' '' '' '0' '1'
##'frame2108' '2108' '2108' '1' '' '' '0' '1'
##'frame2109' '2109' '2109' '1' '' '' '0' '1'
##'frame2110' '2110' '2110' '1' '' '' '0' '1'
##'frame2111' '2111' '2111' '1' '' '' '0' '1'
##'frame2112' '2112' '2112' '1' '' '' '0' '1'
##'frame2113' '2113' '2113' '1' '' '' '0' '1'
##'frame2114' '2114' '2114' '1' '' '' '0' '1'
##'frame2115' '2115' '2115' '1' '' '' '0' '1'
##'frame2116' '2116' '2116' '1' '' '' '0' '1'
##'frame2117' '2117' '2117' '1' '' '' '0' '1'
##'frame2118' '2118' '2118' '1' '' '' '0' '1'
##'frame2119' '2119' '2119' '1' '' '' '0' '1'
##ENDJOBS

##END
