#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963000'
G_USERID='963394'
G_TASKID='8017628'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963000\963394\8017628\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963000\963394\8017628\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\963394'
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
                

cgList=['Nuke','Preprocess','MaxClient','Merge']#preprocess,maxclient
if G_CG_NAME in cgList:
#if os.path.exists(scriptCg):
    if G_CG_NAME == 'Preprocess' or G_CG_NAME == 'MaxClient' or G_CG_NAME == 'Merge':
        G_CG_NAME_PATH = 'Max'
    else:
        G_CG_NAME_PATH = G_CG_NAME
    script2=G_POOL+'\\script2'
    scriptBase=script2+'\\Base'
    scriptCg=script2+'\\'+G_CG_NAME_PATH
    scriptNodeBase=nodePyDir+'\\Base'
    scriptNodeCg=nodePyDir+'\\'+G_CG_NAME_PATH
    print script2
    print scriptBase
    print scriptCg

    userRenderPy=script2+'\\user\\'+G_USERID
    shutil.rmtree(nodePyDir)
    copyFolder(scriptBase,scriptNodeBase)
    copyFolder(scriptCg,scriptNodeCg)
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
    RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=963394_8017628_render.py
##properties=|BJ
##level=79
##custom=963394
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0350' '350' '350' '1' '' '' '1' '1'
##'frame0351' '351' '351' '1' '' '' '1' '1'
##'frame0352' '352' '352' '1' '' '' '1' '1'
##'frame0353' '353' '353' '1' '' '' '1' '1'
##'frame0354' '354' '354' '1' '' '' '1' '1'
##'frame0355' '355' '355' '1' '' '' '1' '1'
##'frame0356' '356' '356' '1' '' '' '1' '1'
##'frame0357' '357' '357' '1' '' '' '1' '1'
##'frame0358' '358' '358' '1' '' '' '1' '1'
##'frame0359' '359' '359' '1' '' '' '1' '1'
##'frame0360' '360' '360' '1' '' '' '1' '1'
##'frame0361' '361' '361' '1' '' '' '1' '1'
##'frame0362' '362' '362' '1' '' '' '1' '1'
##'frame0363' '363' '363' '1' '' '' '1' '1'
##'frame0364' '364' '364' '1' '' '' '1' '1'
##'frame0365' '365' '365' '1' '' '' '1' '1'
##'frame0366' '366' '366' '1' '' '' '1' '1'
##'frame0367' '367' '367' '1' '' '' '1' '1'
##'frame0368' '368' '368' '1' '' '' '1' '1'
##'frame0369' '369' '369' '1' '' '' '1' '1'
##'frame0370' '370' '370' '1' '' '' '1' '1'
##'frame0371' '371' '371' '1' '' '' '1' '1'
##'frame0372' '372' '372' '1' '' '' '1' '1'
##'frame0373' '373' '373' '1' '' '' '1' '1'
##'frame0374' '374' '374' '1' '' '' '1' '1'
##'frame0375' '375' '375' '1' '' '' '1' '1'
##'frame0376' '376' '376' '1' '' '' '1' '1'
##'frame0377' '377' '377' '1' '' '' '1' '1'
##'frame0378' '378' '378' '1' '' '' '1' '1'
##'frame0379' '379' '379' '1' '' '' '1' '1'
##'frame0380' '380' '380' '1' '' '' '1' '1'
##'frame0381' '381' '381' '1' '' '' '1' '1'
##'frame0382' '382' '382' '1' '' '' '1' '1'
##'frame0383' '383' '383' '1' '' '' '1' '1'
##'frame0384' '384' '384' '1' '' '' '1' '1'
##'frame0385' '385' '385' '1' '' '' '1' '1'
##'frame0386' '386' '386' '1' '' '' '1' '1'
##'frame0387' '387' '387' '1' '' '' '1' '1'
##'frame0388' '388' '388' '1' '' '' '1' '1'
##'frame0389' '389' '389' '1' '' '' '1' '1'
##'frame0390' '390' '390' '1' '' '' '1' '1'
##'frame0391' '391' '391' '1' '' '' '1' '1'
##'frame0392' '392' '392' '1' '' '' '1' '1'
##'frame0393' '393' '393' '1' '' '' '1' '1'
##'frame0394' '394' '394' '1' '' '' '1' '1'
##'frame0395' '395' '395' '1' '' '' '1' '1'
##'frame0396' '396' '396' '1' '' '' '1' '1'
##'frame0397' '397' '397' '1' '' '' '1' '1'
##'frame0398' '398' '398' '1' '' '' '1' '1'
##'frame0399' '399' '399' '1' '' '' '1' '1'
##'frame0400' '400' '400' '1' '' '' '1' '1'
##'frame0401' '401' '401' '1' '' '' '1' '1'
##'frame0402' '402' '402' '1' '' '' '1' '1'
##'frame0403' '403' '403' '1' '' '' '1' '1'
##'frame0404' '404' '404' '1' '' '' '1' '1'
##'frame0405' '405' '405' '1' '' '' '1' '1'
##'frame0406' '406' '406' '1' '' '' '1' '1'
##'frame0407' '407' '407' '1' '' '' '1' '1'
##'frame0408' '408' '408' '1' '' '' '1' '1'
##'frame0409' '409' '409' '1' '' '' '1' '1'
##'frame0410' '410' '410' '1' '' '' '1' '1'
##'frame0411' '411' '411' '1' '' '' '1' '1'
##'frame0412' '412' '412' '1' '' '' '1' '1'
##'frame0413' '413' '413' '1' '' '' '1' '1'
##'frame0414' '414' '414' '1' '' '' '1' '1'
##'frame0415' '415' '415' '1' '' '' '1' '1'
##'frame0416' '416' '416' '1' '' '' '1' '1'
##'frame0417' '417' '417' '1' '' '' '1' '1'
##'frame0418' '418' '418' '1' '' '' '1' '1'
##'frame0419' '419' '419' '1' '' '' '1' '1'
##'frame0420' '420' '420' '1' '' '' '1' '1'
##'frame0421' '421' '421' '1' '' '' '1' '1'
##'frame0422' '422' '422' '1' '' '' '1' '1'
##'frame0423' '423' '423' '1' '' '' '1' '1'
##'frame0424' '424' '424' '1' '' '' '1' '1'
##'frame0425' '425' '425' '1' '' '' '1' '1'
##'frame0426' '426' '426' '1' '' '' '1' '1'
##'frame0427' '427' '427' '1' '' '' '1' '1'
##'frame0428' '428' '428' '1' '' '' '1' '1'
##'frame0429' '429' '429' '1' '' '' '1' '1'
##'frame0430' '430' '430' '1' '' '' '1' '1'
##'frame0431' '431' '431' '1' '' '' '1' '1'
##'frame0432' '432' '432' '1' '' '' '1' '1'
##'frame0433' '433' '433' '1' '' '' '1' '1'
##'frame0434' '434' '434' '1' '' '' '1' '1'
##'frame0435' '435' '435' '1' '' '' '1' '1'
##'frame0436' '436' '436' '1' '' '' '1' '1'
##'frame0437' '437' '437' '1' '' '' '1' '1'
##'frame0438' '438' '438' '1' '' '' '1' '1'
##'frame0439' '439' '439' '1' '' '' '1' '1'
##'frame0440' '440' '440' '1' '' '' '1' '1'
##'frame0441' '441' '441' '1' '' '' '1' '1'
##'frame0442' '442' '442' '1' '' '' '1' '1'
##'frame0443' '443' '443' '1' '' '' '1' '1'
##'frame0444' '444' '444' '1' '' '' '1' '1'
##'frame0445' '445' '445' '1' '' '' '1' '1'
##'frame0446' '446' '446' '1' '' '' '1' '1'
##'frame0447' '447' '447' '1' '' '' '1' '1'
##'frame0448' '448' '448' '1' '' '' '1' '1'
##'frame0449' '449' '449' '1' '' '' '1' '1'
##'frame0450' '450' '450' '1' '' '' '1' '1'
##'frame0451' '451' '451' '1' '' '' '1' '1'
##'frame0452' '452' '452' '1' '' '' '1' '1'
##'frame0453' '453' '453' '1' '' '' '1' '1'
##'frame0454' '454' '454' '1' '' '' '1' '1'
##'frame0455' '455' '455' '1' '' '' '1' '1'
##'frame0456' '456' '456' '1' '' '' '1' '1'
##'frame0457' '457' '457' '1' '' '' '1' '1'
##'frame0458' '458' '458' '1' '' '' '1' '1'
##'frame0459' '459' '459' '1' '' '' '1' '1'
##'frame0460' '460' '460' '1' '' '' '1' '1'
##'frame0461' '461' '461' '1' '' '' '1' '1'
##'frame0462' '462' '462' '1' '' '' '1' '1'
##'frame0463' '463' '463' '1' '' '' '1' '1'
##'frame0464' '464' '464' '1' '' '' '1' '1'
##'frame0465' '465' '465' '1' '' '' '1' '1'
##'frame0466' '466' '466' '1' '' '' '1' '1'
##'frame0467' '467' '467' '1' '' '' '1' '1'
##'frame0468' '468' '468' '1' '' '' '1' '1'
##'frame0469' '469' '469' '1' '' '' '1' '1'
##'frame0470' '470' '470' '1' '' '' '1' '1'
##'frame0471' '471' '471' '1' '' '' '1' '1'
##'frame0472' '472' '472' '1' '' '' '1' '1'
##'frame0473' '473' '473' '1' '' '' '1' '1'
##'frame0474' '474' '474' '1' '' '' '1' '1'
##'frame0475' '475' '475' '1' '' '' '1' '1'
##'frame0476' '476' '476' '1' '' '' '1' '1'
##'frame0477' '477' '477' '1' '' '' '1' '1'
##'frame0478' '478' '478' '1' '' '' '1' '1'
##'frame0479' '479' '479' '1' '' '' '1' '1'
##'frame0480' '480' '480' '1' '' '' '1' '1'
##'frame0481' '481' '481' '1' '' '' '1' '1'
##'frame0482' '482' '482' '1' '' '' '1' '1'
##'frame0483' '483' '483' '1' '' '' '1' '1'
##'frame0484' '484' '484' '1' '' '' '1' '1'
##'frame0485' '485' '485' '1' '' '' '1' '1'
##'frame0486' '486' '486' '1' '' '' '1' '1'
##'frame0487' '487' '487' '1' '' '' '1' '1'
##'frame0488' '488' '488' '1' '' '' '1' '1'
##'frame0489' '489' '489' '1' '' '' '1' '1'
##'frame0490' '490' '490' '1' '' '' '1' '1'
##'frame0491' '491' '491' '1' '' '' '1' '1'
##'frame0492' '492' '492' '1' '' '' '1' '1'
##'frame0493' '493' '493' '1' '' '' '1' '1'
##'frame0494' '494' '494' '1' '' '' '1' '1'
##'frame0495' '495' '495' '1' '' '' '1' '1'
##'frame0496' '496' '496' '1' '' '' '1' '1'
##'frame0497' '497' '497' '1' '' '' '1' '1'
##'frame0498' '498' '498' '1' '' '' '1' '1'
##'frame0499' '499' '499' '1' '' '' '1' '1'
##'frame0500' '500' '500' '1' '' '' '1' '1'
##'frame0501' '501' '501' '1' '' '' '1' '1'
##'frame0502' '502' '502' '1' '' '' '1' '1'
##'frame0503' '503' '503' '1' '' '' '1' '1'
##'frame0504' '504' '504' '1' '' '' '1' '1'
##'frame0505' '505' '505' '1' '' '' '1' '1'
##'frame0506' '506' '506' '1' '' '' '1' '1'
##'frame0507' '507' '507' '1' '' '' '1' '1'
##'frame0508' '508' '508' '1' '' '' '1' '1'
##'frame0509' '509' '509' '1' '' '' '1' '1'
##'frame0510' '510' '510' '1' '' '' '1' '1'
##'frame0511' '511' '511' '1' '' '' '1' '1'
##'frame0512' '512' '512' '1' '' '' '1' '1'
##'frame0513' '513' '513' '1' '' '' '1' '1'
##'frame0514' '514' '514' '1' '' '' '1' '1'
##'frame0515' '515' '515' '1' '' '' '1' '1'
##'frame0516' '516' '516' '1' '' '' '1' '1'
##'frame0517' '517' '517' '1' '' '' '1' '1'
##'frame0518' '518' '518' '1' '' '' '1' '1'
##'frame0519' '519' '519' '1' '' '' '1' '1'
##'frame0520' '520' '520' '1' '' '' '1' '1'
##'frame0521' '521' '521' '1' '' '' '1' '1'
##'frame0522' '522' '522' '1' '' '' '1' '1'
##'frame0523' '523' '523' '1' '' '' '1' '1'
##'frame0524' '524' '524' '1' '' '' '1' '1'
##'frame0525' '525' '525' '1' '' '' '1' '1'
##'frame0526' '526' '526' '1' '' '' '1' '1'
##'frame0527' '527' '527' '1' '' '' '1' '1'
##'frame0528' '528' '528' '1' '' '' '1' '1'
##'frame0529' '529' '529' '1' '' '' '1' '1'
##'frame0530' '530' '530' '1' '' '' '1' '1'
##'frame0531' '531' '531' '1' '' '' '1' '1'
##'frame0532' '532' '532' '1' '' '' '1' '1'
##'frame0533' '533' '533' '1' '' '' '1' '1'
##'frame0534' '534' '534' '1' '' '' '1' '1'
##'frame0535' '535' '535' '1' '' '' '1' '1'
##'frame0536' '536' '536' '1' '' '' '1' '1'
##'frame0537' '537' '537' '1' '' '' '1' '1'
##'frame0538' '538' '538' '1' '' '' '1' '1'
##'frame0539' '539' '539' '1' '' '' '1' '1'
##'frame0540' '540' '540' '1' '' '' '1' '1'
##'frame0541' '541' '541' '1' '' '' '1' '1'
##'frame0542' '542' '542' '1' '' '' '1' '1'
##'frame0543' '543' '543' '1' '' '' '1' '1'
##'frame0544' '544' '544' '1' '' '' '1' '1'
##'frame0545' '545' '545' '1' '' '' '1' '1'
##'frame0546' '546' '546' '1' '' '' '1' '1'
##'frame0547' '547' '547' '1' '' '' '1' '1'
##'frame0548' '548' '548' '1' '' '' '1' '1'
##'frame0549' '549' '549' '1' '' '' '1' '1'
##'frame0550' '550' '550' '1' '' '' '1' '1'
##'frame0551' '551' '551' '1' '' '' '1' '1'
##'frame0552' '552' '552' '1' '' '' '1' '1'
##'frame0553' '553' '553' '1' '' '' '1' '1'
##'frame0554' '554' '554' '1' '' '' '1' '1'
##'frame0555' '555' '555' '1' '' '' '1' '1'
##'frame0556' '556' '556' '1' '' '' '1' '1'
##'frame0557' '557' '557' '1' '' '' '1' '1'
##'frame0558' '558' '558' '1' '' '' '1' '1'
##'frame0559' '559' '559' '1' '' '' '1' '1'
##'frame0560' '560' '560' '1' '' '' '1' '1'
##'frame0561' '561' '561' '1' '' '' '1' '1'
##'frame0562' '562' '562' '1' '' '' '1' '1'
##'frame0563' '563' '563' '1' '' '' '1' '1'
##'frame0564' '564' '564' '1' '' '' '1' '1'
##'frame0565' '565' '565' '1' '' '' '1' '1'
##'frame0566' '566' '566' '1' '' '' '1' '1'
##'frame0567' '567' '567' '1' '' '' '1' '1'
##'frame0568' '568' '568' '1' '' '' '1' '1'
##'frame0569' '569' '569' '1' '' '' '1' '1'
##'frame0570' '570' '570' '1' '' '' '1' '1'
##'frame0571' '571' '571' '1' '' '' '1' '1'
##'frame0572' '572' '572' '1' '' '' '1' '1'
##'frame0573' '573' '573' '1' '' '' '1' '1'
##'frame0574' '574' '574' '1' '' '' '1' '1'
##'frame0575' '575' '575' '1' '' '' '1' '1'
##'frame0576' '576' '576' '1' '' '' '1' '1'
##'frame0577' '577' '577' '1' '' '' '1' '1'
##'frame0578' '578' '578' '1' '' '' '1' '1'
##'frame0579' '579' '579' '1' '' '' '1' '1'
##'frame0580' '580' '580' '1' '' '' '1' '1'
##'frame0581' '581' '581' '1' '' '' '1' '1'
##'frame0582' '582' '582' '1' '' '' '1' '1'
##'frame0583' '583' '583' '1' '' '' '1' '1'
##'frame0584' '584' '584' '1' '' '' '1' '1'
##'frame0585' '585' '585' '1' '' '' '1' '1'
##'frame0586' '586' '586' '1' '' '' '1' '1'
##'frame0587' '587' '587' '1' '' '' '1' '1'
##'frame0588' '588' '588' '1' '' '' '1' '1'
##'frame0589' '589' '589' '1' '' '' '1' '1'
##'frame0590' '590' '590' '1' '' '' '1' '1'
##'frame0591' '591' '591' '1' '' '' '1' '1'
##'frame0592' '592' '592' '1' '' '' '1' '1'
##'frame0593' '593' '593' '1' '' '' '1' '1'
##'frame0594' '594' '594' '1' '' '' '1' '1'
##'frame0595' '595' '595' '1' '' '' '1' '1'
##'frame0596' '596' '596' '1' '' '' '1' '1'
##'frame0597' '597' '597' '1' '' '' '1' '1'
##'frame0598' '598' '598' '1' '' '' '1' '1'
##'frame0599' '599' '599' '1' '' '' '1' '1'
##'frame0600' '600' '600' '1' '' '' '1' '1'
##'frame0601' '601' '601' '1' '' '' '1' '1'
##'frame0602' '602' '602' '1' '' '' '1' '1'
##'frame0603' '603' '603' '1' '' '' '1' '1'
##'frame0604' '604' '604' '1' '' '' '1' '1'
##'frame0605' '605' '605' '1' '' '' '1' '1'
##'frame0606' '606' '606' '1' '' '' '1' '1'
##'frame0607' '607' '607' '1' '' '' '1' '1'
##'frame0608' '608' '608' '1' '' '' '1' '1'
##'frame0609' '609' '609' '1' '' '' '1' '1'
##'frame0610' '610' '610' '1' '' '' '1' '1'
##'frame0611' '611' '611' '1' '' '' '1' '1'
##'frame0612' '612' '612' '1' '' '' '1' '1'
##'frame0613' '613' '613' '1' '' '' '1' '1'
##'frame0614' '614' '614' '1' '' '' '1' '1'
##'frame0615' '615' '615' '1' '' '' '1' '1'
##'frame0616' '616' '616' '1' '' '' '1' '1'
##'frame0617' '617' '617' '1' '' '' '1' '1'
##'frame0618' '618' '618' '1' '' '' '1' '1'
##'frame0619' '619' '619' '1' '' '' '1' '1'
##'frame0620' '620' '620' '1' '' '' '1' '1'
##'frame0621' '621' '621' '1' '' '' '1' '1'
##'frame0622' '622' '622' '1' '' '' '1' '1'
##'frame0623' '623' '623' '1' '' '' '1' '1'
##'frame0624' '624' '624' '1' '' '' '1' '1'
##'frame0625' '625' '625' '1' '' '' '1' '1'
##'frame0626' '626' '626' '1' '' '' '1' '1'
##'frame0627' '627' '627' '1' '' '' '1' '1'
##'frame0628' '628' '628' '1' '' '' '1' '1'
##'frame0629' '629' '629' '1' '' '' '1' '1'
##'frame0630' '630' '630' '1' '' '' '1' '1'
##'frame0631' '631' '631' '1' '' '' '1' '1'
##'frame0632' '632' '632' '1' '' '' '1' '1'
##'frame0633' '633' '633' '1' '' '' '1' '1'
##'frame0634' '634' '634' '1' '' '' '1' '1'
##'frame0635' '635' '635' '1' '' '' '1' '1'
##'frame0636' '636' '636' '1' '' '' '1' '1'
##'frame0637' '637' '637' '1' '' '' '1' '1'
##'frame0638' '638' '638' '1' '' '' '1' '1'
##'frame0639' '639' '639' '1' '' '' '1' '1'
##'frame0640' '640' '640' '1' '' '' '1' '1'
##'frame0641' '641' '641' '1' '' '' '1' '1'
##'frame0642' '642' '642' '1' '' '' '1' '1'
##'frame0643' '643' '643' '1' '' '' '1' '1'
##'frame0644' '644' '644' '1' '' '' '1' '1'
##'frame0645' '645' '645' '1' '' '' '1' '1'
##'frame0646' '646' '646' '1' '' '' '1' '1'
##'frame0647' '647' '647' '1' '' '' '1' '1'
##'frame0648' '648' '648' '1' '' '' '1' '1'
##'frame0649' '649' '649' '1' '' '' '1' '1'
##'frame0650' '650' '650' '1' '' '' '1' '1'
##'frame0651' '651' '651' '1' '' '' '1' '1'
##'frame0652' '652' '652' '1' '' '' '1' '1'
##'frame0653' '653' '653' '1' '' '' '1' '1'
##'frame0654' '654' '654' '1' '' '' '1' '1'
##'frame0655' '655' '655' '1' '' '' '1' '1'
##'frame0656' '656' '656' '1' '' '' '1' '1'
##'frame0657' '657' '657' '1' '' '' '1' '1'
##'frame0658' '658' '658' '1' '' '' '1' '1'
##'frame0659' '659' '659' '1' '' '' '1' '1'
##'frame0660' '660' '660' '1' '' '' '1' '1'
##'frame0661' '661' '661' '1' '' '' '1' '1'
##'frame0662' '662' '662' '1' '' '' '1' '1'
##'frame0663' '663' '663' '1' '' '' '1' '1'
##'frame0664' '664' '664' '1' '' '' '1' '1'
##'frame0665' '665' '665' '1' '' '' '1' '1'
##'frame0666' '666' '666' '1' '' '' '1' '1'
##'frame0667' '667' '667' '1' '' '' '1' '1'
##'frame0668' '668' '668' '1' '' '' '1' '1'
##'frame0669' '669' '669' '1' '' '' '1' '1'
##'frame0670' '670' '670' '1' '' '' '1' '1'
##'frame0671' '671' '671' '1' '' '' '1' '1'
##'frame0672' '672' '672' '1' '' '' '1' '1'
##'frame0673' '673' '673' '1' '' '' '1' '1'
##'frame0674' '674' '674' '1' '' '' '1' '1'
##'frame0675' '675' '675' '1' '' '' '1' '1'
##'frame0676' '676' '676' '1' '' '' '1' '1'
##'frame0677' '677' '677' '1' '' '' '1' '1'
##'frame0678' '678' '678' '1' '' '' '1' '1'
##'frame0679' '679' '679' '1' '' '' '1' '1'
##'frame0680' '680' '680' '1' '' '' '1' '1'
##'frame0681' '681' '681' '1' '' '' '1' '1'
##'frame0682' '682' '682' '1' '' '' '1' '1'
##'frame0683' '683' '683' '1' '' '' '1' '1'
##'frame0684' '684' '684' '1' '' '' '1' '1'
##'frame0685' '685' '685' '1' '' '' '1' '1'
##'frame0686' '686' '686' '1' '' '' '1' '1'
##'frame0687' '687' '687' '1' '' '' '1' '1'
##'frame0688' '688' '688' '1' '' '' '1' '1'
##'frame0689' '689' '689' '1' '' '' '1' '1'
##'frame0690' '690' '690' '1' '' '' '1' '1'
##'frame0691' '691' '691' '1' '' '' '1' '1'
##'frame0692' '692' '692' '1' '' '' '1' '1'
##'frame0693' '693' '693' '1' '' '' '1' '1'
##'frame0694' '694' '694' '1' '' '' '1' '1'
##'frame0695' '695' '695' '1' '' '' '1' '1'
##'frame0696' '696' '696' '1' '' '' '1' '1'
##'frame0697' '697' '697' '1' '' '' '1' '1'
##'frame0698' '698' '698' '1' '' '' '1' '1'
##'frame0699' '699' '699' '1' '' '' '1' '1'
##'frame0700' '700' '700' '1' '' '' '1' '1'
##'frame0701' '701' '701' '1' '' '' '1' '1'
##'frame0702' '702' '702' '1' '' '' '1' '1'
##'frame0703' '703' '703' '1' '' '' '1' '1'
##'frame0704' '704' '704' '1' '' '' '1' '1'
##'frame0705' '705' '705' '1' '' '' '1' '1'
##'frame0706' '706' '706' '1' '' '' '1' '1'
##'frame0707' '707' '707' '1' '' '' '1' '1'
##'frame0708' '708' '708' '1' '' '' '1' '1'
##'frame0709' '709' '709' '1' '' '' '1' '1'
##'frame0710' '710' '710' '1' '' '' '1' '1'
##'frame0711' '711' '711' '1' '' '' '1' '1'
##'frame0712' '712' '712' '1' '' '' '1' '1'
##'frame0713' '713' '713' '1' '' '' '1' '1'
##'frame0714' '714' '714' '1' '' '' '1' '1'
##'frame0715' '715' '715' '1' '' '' '1' '1'
##'frame0716' '716' '716' '1' '' '' '1' '1'
##'frame0717' '717' '717' '1' '' '' '1' '1'
##'frame0718' '718' '718' '1' '' '' '1' '1'
##'frame0719' '719' '719' '1' '' '' '1' '1'
##'frame0720' '720' '720' '1' '' '' '1' '1'
##ENDJOBS

##END
