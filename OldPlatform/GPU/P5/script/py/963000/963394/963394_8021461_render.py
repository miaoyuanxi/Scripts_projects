#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963000'
G_USERID='963394'
G_TASKID='8021461'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963000\963394\8021461\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963000\963394\8021461\plugins.json'
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
##name=963394_8021461_render.py
##properties=|BJ
##level=79
##custom=963394
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0000' '0' '0' '1' '' '' '1' '1'
##'frame0001' '1' '1' '1' '' '' '1' '1'
##'frame0002' '2' '2' '1' '' '' '1' '1'
##'frame0003' '3' '3' '1' '' '' '1' '1'
##'frame0004' '4' '4' '1' '' '' '1' '1'
##'frame0005' '5' '5' '1' '' '' '1' '1'
##'frame0006' '6' '6' '1' '' '' '1' '1'
##'frame0007' '7' '7' '1' '' '' '1' '1'
##'frame0008' '8' '8' '1' '' '' '1' '1'
##'frame0009' '9' '9' '1' '' '' '1' '1'
##'frame0010' '10' '10' '1' '' '' '1' '1'
##'frame0011' '11' '11' '1' '' '' '1' '1'
##'frame0012' '12' '12' '1' '' '' '1' '1'
##'frame0013' '13' '13' '1' '' '' '1' '1'
##'frame0014' '14' '14' '1' '' '' '1' '1'
##'frame0015' '15' '15' '1' '' '' '1' '1'
##'frame0016' '16' '16' '1' '' '' '1' '1'
##'frame0017' '17' '17' '1' '' '' '1' '1'
##'frame0018' '18' '18' '1' '' '' '1' '1'
##'frame0019' '19' '19' '1' '' '' '1' '1'
##'frame0020' '20' '20' '1' '' '' '1' '1'
##'frame0021' '21' '21' '1' '' '' '1' '1'
##'frame0022' '22' '22' '1' '' '' '1' '1'
##'frame0023' '23' '23' '1' '' '' '1' '1'
##'frame0024' '24' '24' '1' '' '' '1' '1'
##'frame0025' '25' '25' '1' '' '' '1' '1'
##'frame0026' '26' '26' '1' '' '' '1' '1'
##'frame0027' '27' '27' '1' '' '' '1' '1'
##'frame0028' '28' '28' '1' '' '' '1' '1'
##'frame0029' '29' '29' '1' '' '' '1' '1'
##'frame0030' '30' '30' '1' '' '' '1' '1'
##'frame0031' '31' '31' '1' '' '' '1' '1'
##'frame0032' '32' '32' '1' '' '' '1' '1'
##'frame0033' '33' '33' '1' '' '' '1' '1'
##'frame0034' '34' '34' '1' '' '' '1' '1'
##'frame0035' '35' '35' '1' '' '' '1' '1'
##'frame0036' '36' '36' '1' '' '' '1' '1'
##'frame0037' '37' '37' '1' '' '' '1' '1'
##'frame0038' '38' '38' '1' '' '' '1' '1'
##'frame0039' '39' '39' '1' '' '' '1' '1'
##'frame0040' '40' '40' '1' '' '' '1' '1'
##'frame0041' '41' '41' '1' '' '' '1' '1'
##'frame0042' '42' '42' '1' '' '' '1' '1'
##'frame0043' '43' '43' '1' '' '' '1' '1'
##'frame0044' '44' '44' '1' '' '' '1' '1'
##'frame0045' '45' '45' '1' '' '' '1' '1'
##'frame0046' '46' '46' '1' '' '' '1' '1'
##'frame0047' '47' '47' '1' '' '' '1' '1'
##'frame0048' '48' '48' '1' '' '' '1' '1'
##'frame0049' '49' '49' '1' '' '' '1' '1'
##'frame0050' '50' '50' '1' '' '' '1' '1'
##'frame0051' '51' '51' '1' '' '' '1' '1'
##'frame0052' '52' '52' '1' '' '' '1' '1'
##'frame0053' '53' '53' '1' '' '' '1' '1'
##'frame0054' '54' '54' '1' '' '' '1' '1'
##'frame0055' '55' '55' '1' '' '' '1' '1'
##'frame0056' '56' '56' '1' '' '' '1' '1'
##'frame0057' '57' '57' '1' '' '' '1' '1'
##'frame0058' '58' '58' '1' '' '' '1' '1'
##'frame0059' '59' '59' '1' '' '' '1' '1'
##'frame0060' '60' '60' '1' '' '' '1' '1'
##'frame0061' '61' '61' '1' '' '' '1' '1'
##'frame0062' '62' '62' '1' '' '' '1' '1'
##'frame0063' '63' '63' '1' '' '' '1' '1'
##'frame0064' '64' '64' '1' '' '' '1' '1'
##'frame0065' '65' '65' '1' '' '' '1' '1'
##'frame0066' '66' '66' '1' '' '' '1' '1'
##'frame0067' '67' '67' '1' '' '' '1' '1'
##'frame0068' '68' '68' '1' '' '' '1' '1'
##'frame0069' '69' '69' '1' '' '' '1' '1'
##'frame0070' '70' '70' '1' '' '' '1' '1'
##'frame0071' '71' '71' '1' '' '' '1' '1'
##'frame0072' '72' '72' '1' '' '' '1' '1'
##'frame0073' '73' '73' '1' '' '' '1' '1'
##'frame0074' '74' '74' '1' '' '' '1' '1'
##'frame0075' '75' '75' '1' '' '' '1' '1'
##'frame0076' '76' '76' '1' '' '' '1' '1'
##'frame0077' '77' '77' '1' '' '' '1' '1'
##'frame0078' '78' '78' '1' '' '' '1' '1'
##'frame0079' '79' '79' '1' '' '' '1' '1'
##'frame0080' '80' '80' '1' '' '' '1' '1'
##'frame0081' '81' '81' '1' '' '' '1' '1'
##'frame0082' '82' '82' '1' '' '' '1' '1'
##'frame0083' '83' '83' '1' '' '' '1' '1'
##'frame0084' '84' '84' '1' '' '' '1' '1'
##'frame0085' '85' '85' '1' '' '' '1' '1'
##'frame0086' '86' '86' '1' '' '' '1' '1'
##'frame0087' '87' '87' '1' '' '' '1' '1'
##'frame0088' '88' '88' '1' '' '' '1' '1'
##'frame0089' '89' '89' '1' '' '' '1' '1'
##'frame0090' '90' '90' '1' '' '' '1' '1'
##'frame0091' '91' '91' '1' '' '' '1' '1'
##'frame0092' '92' '92' '1' '' '' '1' '1'
##'frame0093' '93' '93' '1' '' '' '1' '1'
##'frame0094' '94' '94' '1' '' '' '1' '1'
##'frame0095' '95' '95' '1' '' '' '1' '1'
##'frame0096' '96' '96' '1' '' '' '1' '1'
##'frame0097' '97' '97' '1' '' '' '1' '1'
##'frame0098' '98' '98' '1' '' '' '1' '1'
##'frame0099' '99' '99' '1' '' '' '1' '1'
##'frame0100' '100' '100' '1' '' '' '1' '1'
##'frame0101' '101' '101' '1' '' '' '1' '1'
##'frame0102' '102' '102' '1' '' '' '1' '1'
##'frame0103' '103' '103' '1' '' '' '1' '1'
##'frame0104' '104' '104' '1' '' '' '1' '1'
##'frame0105' '105' '105' '1' '' '' '1' '1'
##'frame0106' '106' '106' '1' '' '' '1' '1'
##'frame0107' '107' '107' '1' '' '' '1' '1'
##'frame0108' '108' '108' '1' '' '' '1' '1'
##'frame0109' '109' '109' '1' '' '' '1' '1'
##'frame0110' '110' '110' '1' '' '' '1' '1'
##'frame0111' '111' '111' '1' '' '' '1' '1'
##'frame0112' '112' '112' '1' '' '' '1' '1'
##'frame0113' '113' '113' '1' '' '' '1' '1'
##'frame0114' '114' '114' '1' '' '' '1' '1'
##'frame0115' '115' '115' '1' '' '' '1' '1'
##'frame0116' '116' '116' '1' '' '' '1' '1'
##'frame0117' '117' '117' '1' '' '' '1' '1'
##'frame0118' '118' '118' '1' '' '' '1' '1'
##'frame0119' '119' '119' '1' '' '' '1' '1'
##'frame0120' '120' '120' '1' '' '' '1' '1'
##'frame0121' '121' '121' '1' '' '' '1' '1'
##'frame0122' '122' '122' '1' '' '' '1' '1'
##'frame0123' '123' '123' '1' '' '' '1' '1'
##'frame0124' '124' '124' '1' '' '' '1' '1'
##'frame0125' '125' '125' '1' '' '' '1' '1'
##'frame0126' '126' '126' '1' '' '' '1' '1'
##'frame0127' '127' '127' '1' '' '' '1' '1'
##'frame0128' '128' '128' '1' '' '' '1' '1'
##'frame0129' '129' '129' '1' '' '' '1' '1'
##'frame0130' '130' '130' '1' '' '' '1' '1'
##'frame0131' '131' '131' '1' '' '' '1' '1'
##'frame0132' '132' '132' '1' '' '' '1' '1'
##'frame0133' '133' '133' '1' '' '' '1' '1'
##'frame0134' '134' '134' '1' '' '' '1' '1'
##'frame0135' '135' '135' '1' '' '' '1' '1'
##'frame0136' '136' '136' '1' '' '' '1' '1'
##'frame0137' '137' '137' '1' '' '' '1' '1'
##'frame0138' '138' '138' '1' '' '' '1' '1'
##'frame0139' '139' '139' '1' '' '' '1' '1'
##'frame0140' '140' '140' '1' '' '' '1' '1'
##'frame0141' '141' '141' '1' '' '' '1' '1'
##'frame0142' '142' '142' '1' '' '' '1' '1'
##'frame0143' '143' '143' '1' '' '' '1' '1'
##'frame0144' '144' '144' '1' '' '' '1' '1'
##'frame0145' '145' '145' '1' '' '' '1' '1'
##'frame0146' '146' '146' '1' '' '' '1' '1'
##'frame0147' '147' '147' '1' '' '' '1' '1'
##'frame0148' '148' '148' '1' '' '' '1' '1'
##'frame0149' '149' '149' '1' '' '' '1' '1'
##'frame0150' '150' '150' '1' '' '' '1' '1'
##'frame0151' '151' '151' '1' '' '' '1' '1'
##'frame0152' '152' '152' '1' '' '' '1' '1'
##'frame0153' '153' '153' '1' '' '' '1' '1'
##'frame0154' '154' '154' '1' '' '' '1' '1'
##'frame0155' '155' '155' '1' '' '' '1' '1'
##'frame0156' '156' '156' '1' '' '' '1' '1'
##'frame0157' '157' '157' '1' '' '' '1' '1'
##'frame0158' '158' '158' '1' '' '' '1' '1'
##'frame0159' '159' '159' '1' '' '' '1' '1'
##'frame0160' '160' '160' '1' '' '' '1' '1'
##'frame0161' '161' '161' '1' '' '' '1' '1'
##'frame0162' '162' '162' '1' '' '' '1' '1'
##'frame0163' '163' '163' '1' '' '' '1' '1'
##'frame0164' '164' '164' '1' '' '' '1' '1'
##'frame0165' '165' '165' '1' '' '' '1' '1'
##'frame0166' '166' '166' '1' '' '' '1' '1'
##'frame0167' '167' '167' '1' '' '' '1' '1'
##'frame0168' '168' '168' '1' '' '' '1' '1'
##'frame0169' '169' '169' '1' '' '' '1' '1'
##'frame0170' '170' '170' '1' '' '' '1' '1'
##'frame0171' '171' '171' '1' '' '' '1' '1'
##'frame0172' '172' '172' '1' '' '' '1' '1'
##'frame0173' '173' '173' '1' '' '' '1' '1'
##'frame0174' '174' '174' '1' '' '' '1' '1'
##'frame0175' '175' '175' '1' '' '' '1' '1'
##'frame0176' '176' '176' '1' '' '' '1' '1'
##'frame0177' '177' '177' '1' '' '' '1' '1'
##'frame0178' '178' '178' '1' '' '' '1' '1'
##'frame0179' '179' '179' '1' '' '' '1' '1'
##'frame0180' '180' '180' '1' '' '' '1' '1'
##'frame0181' '181' '181' '1' '' '' '1' '1'
##'frame0182' '182' '182' '1' '' '' '1' '1'
##'frame0183' '183' '183' '1' '' '' '1' '1'
##'frame0184' '184' '184' '1' '' '' '1' '1'
##'frame0185' '185' '185' '1' '' '' '1' '1'
##'frame0186' '186' '186' '1' '' '' '1' '1'
##'frame0187' '187' '187' '1' '' '' '1' '1'
##'frame0188' '188' '188' '1' '' '' '1' '1'
##'frame0189' '189' '189' '1' '' '' '1' '1'
##'frame0190' '190' '190' '1' '' '' '1' '1'
##'frame0191' '191' '191' '1' '' '' '1' '1'
##'frame0192' '192' '192' '1' '' '' '1' '1'
##'frame0193' '193' '193' '1' '' '' '1' '1'
##'frame0194' '194' '194' '1' '' '' '1' '1'
##'frame0195' '195' '195' '1' '' '' '1' '1'
##'frame0196' '196' '196' '1' '' '' '1' '1'
##'frame0197' '197' '197' '1' '' '' '1' '1'
##'frame0198' '198' '198' '1' '' '' '1' '1'
##'frame0199' '199' '199' '1' '' '' '1' '1'
##'frame0200' '200' '200' '1' '' '' '1' '1'
##'frame0201' '201' '201' '1' '' '' '1' '1'
##'frame0202' '202' '202' '1' '' '' '1' '1'
##'frame0203' '203' '203' '1' '' '' '1' '1'
##'frame0204' '204' '204' '1' '' '' '1' '1'
##'frame0205' '205' '205' '1' '' '' '1' '1'
##'frame0206' '206' '206' '1' '' '' '1' '1'
##'frame0207' '207' '207' '1' '' '' '1' '1'
##'frame0208' '208' '208' '1' '' '' '1' '1'
##'frame0209' '209' '209' '1' '' '' '1' '1'
##'frame0210' '210' '210' '1' '' '' '1' '1'
##'frame0211' '211' '211' '1' '' '' '1' '1'
##'frame0212' '212' '212' '1' '' '' '1' '1'
##'frame0213' '213' '213' '1' '' '' '1' '1'
##'frame0214' '214' '214' '1' '' '' '1' '1'
##'frame0215' '215' '215' '1' '' '' '1' '1'
##'frame0216' '216' '216' '1' '' '' '1' '1'
##'frame0217' '217' '217' '1' '' '' '1' '1'
##'frame0218' '218' '218' '1' '' '' '1' '1'
##'frame0219' '219' '219' '1' '' '' '1' '1'
##'frame0220' '220' '220' '1' '' '' '1' '1'
##'frame0221' '221' '221' '1' '' '' '1' '1'
##'frame0222' '222' '222' '1' '' '' '1' '1'
##'frame0223' '223' '223' '1' '' '' '1' '1'
##'frame0224' '224' '224' '1' '' '' '1' '1'
##'frame0225' '225' '225' '1' '' '' '1' '1'
##'frame0226' '226' '226' '1' '' '' '1' '1'
##'frame0227' '227' '227' '1' '' '' '1' '1'
##'frame0228' '228' '228' '1' '' '' '1' '1'
##'frame0229' '229' '229' '1' '' '' '1' '1'
##'frame0230' '230' '230' '1' '' '' '1' '1'
##'frame0231' '231' '231' '1' '' '' '1' '1'
##'frame0232' '232' '232' '1' '' '' '1' '1'
##'frame0233' '233' '233' '1' '' '' '1' '1'
##'frame0234' '234' '234' '1' '' '' '1' '1'
##'frame0235' '235' '235' '1' '' '' '1' '1'
##'frame0236' '236' '236' '1' '' '' '1' '1'
##'frame0237' '237' '237' '1' '' '' '1' '1'
##'frame0238' '238' '238' '1' '' '' '1' '1'
##'frame0239' '239' '239' '1' '' '' '1' '1'
##'frame0240' '240' '240' '1' '' '' '1' '1'
##'frame0241' '241' '241' '1' '' '' '1' '1'
##'frame0242' '242' '242' '1' '' '' '1' '1'
##'frame0243' '243' '243' '1' '' '' '1' '1'
##'frame0244' '244' '244' '1' '' '' '1' '1'
##'frame0245' '245' '245' '1' '' '' '1' '1'
##'frame0246' '246' '246' '1' '' '' '1' '1'
##'frame0247' '247' '247' '1' '' '' '1' '1'
##'frame0248' '248' '248' '1' '' '' '1' '1'
##'frame0249' '249' '249' '1' '' '' '1' '1'
##'frame0250' '250' '250' '1' '' '' '1' '1'
##'frame0251' '251' '251' '1' '' '' '1' '1'
##'frame0252' '252' '252' '1' '' '' '1' '1'
##'frame0253' '253' '253' '1' '' '' '1' '1'
##'frame0254' '254' '254' '1' '' '' '1' '1'
##'frame0255' '255' '255' '1' '' '' '1' '1'
##'frame0256' '256' '256' '1' '' '' '1' '1'
##'frame0257' '257' '257' '1' '' '' '1' '1'
##'frame0258' '258' '258' '1' '' '' '1' '1'
##'frame0259' '259' '259' '1' '' '' '1' '1'
##'frame0260' '260' '260' '1' '' '' '1' '1'
##'frame0261' '261' '261' '1' '' '' '1' '1'
##'frame0262' '262' '262' '1' '' '' '1' '1'
##'frame0263' '263' '263' '1' '' '' '1' '1'
##'frame0264' '264' '264' '1' '' '' '1' '1'
##'frame0265' '265' '265' '1' '' '' '1' '1'
##'frame0266' '266' '266' '1' '' '' '1' '1'
##'frame0267' '267' '267' '1' '' '' '1' '1'
##'frame0268' '268' '268' '1' '' '' '1' '1'
##'frame0269' '269' '269' '1' '' '' '1' '1'
##'frame0270' '270' '270' '1' '' '' '1' '1'
##'frame0271' '271' '271' '1' '' '' '1' '1'
##'frame0272' '272' '272' '1' '' '' '1' '1'
##'frame0273' '273' '273' '1' '' '' '1' '1'
##'frame0274' '274' '274' '1' '' '' '1' '1'
##'frame0275' '275' '275' '1' '' '' '1' '1'
##'frame0276' '276' '276' '1' '' '' '1' '1'
##'frame0277' '277' '277' '1' '' '' '1' '1'
##'frame0278' '278' '278' '1' '' '' '1' '1'
##'frame0279' '279' '279' '1' '' '' '1' '1'
##'frame0280' '280' '280' '1' '' '' '1' '1'
##'frame0281' '281' '281' '1' '' '' '1' '1'
##'frame0282' '282' '282' '1' '' '' '1' '1'
##'frame0283' '283' '283' '1' '' '' '1' '1'
##'frame0284' '284' '284' '1' '' '' '1' '1'
##'frame0285' '285' '285' '1' '' '' '1' '1'
##'frame0286' '286' '286' '1' '' '' '1' '1'
##'frame0287' '287' '287' '1' '' '' '1' '1'
##'frame0288' '288' '288' '1' '' '' '1' '1'
##'frame0289' '289' '289' '1' '' '' '1' '1'
##'frame0290' '290' '290' '1' '' '' '1' '1'
##'frame0291' '291' '291' '1' '' '' '1' '1'
##'frame0292' '292' '292' '1' '' '' '1' '1'
##'frame0293' '293' '293' '1' '' '' '1' '1'
##'frame0294' '294' '294' '1' '' '' '1' '1'
##'frame0295' '295' '295' '1' '' '' '1' '1'
##'frame0296' '296' '296' '1' '' '' '1' '1'
##'frame0297' '297' '297' '1' '' '' '1' '1'
##'frame0298' '298' '298' '1' '' '' '1' '1'
##'frame0299' '299' '299' '1' '' '' '1' '1'
##'frame0300' '300' '300' '1' '' '' '1' '1'
##'frame0301' '301' '301' '1' '' '' '1' '1'
##'frame0302' '302' '302' '1' '' '' '1' '1'
##'frame0303' '303' '303' '1' '' '' '1' '1'
##'frame0304' '304' '304' '1' '' '' '1' '1'
##'frame0305' '305' '305' '1' '' '' '1' '1'
##'frame0306' '306' '306' '1' '' '' '1' '1'
##'frame0307' '307' '307' '1' '' '' '1' '1'
##'frame0308' '308' '308' '1' '' '' '1' '1'
##'frame0309' '309' '309' '1' '' '' '1' '1'
##'frame0310' '310' '310' '1' '' '' '1' '1'
##'frame0311' '311' '311' '1' '' '' '1' '1'
##'frame0312' '312' '312' '1' '' '' '1' '1'
##'frame0313' '313' '313' '1' '' '' '1' '1'
##'frame0314' '314' '314' '1' '' '' '1' '1'
##'frame0315' '315' '315' '1' '' '' '1' '1'
##'frame0316' '316' '316' '1' '' '' '1' '1'
##'frame0317' '317' '317' '1' '' '' '1' '1'
##'frame0318' '318' '318' '1' '' '' '1' '1'
##'frame0319' '319' '319' '1' '' '' '1' '1'
##'frame0320' '320' '320' '1' '' '' '1' '1'
##'frame0321' '321' '321' '1' '' '' '1' '1'
##'frame0322' '322' '322' '1' '' '' '1' '1'
##'frame0323' '323' '323' '1' '' '' '1' '1'
##'frame0324' '324' '324' '1' '' '' '1' '1'
##'frame0325' '325' '325' '1' '' '' '1' '1'
##'frame0326' '326' '326' '1' '' '' '1' '1'
##'frame0327' '327' '327' '1' '' '' '1' '1'
##'frame0328' '328' '328' '1' '' '' '1' '1'
##'frame0329' '329' '329' '1' '' '' '1' '1'
##'frame0330' '330' '330' '1' '' '' '1' '1'
##'frame0331' '331' '331' '1' '' '' '1' '1'
##'frame0332' '332' '332' '1' '' '' '1' '1'
##'frame0333' '333' '333' '1' '' '' '1' '1'
##'frame0334' '334' '334' '1' '' '' '1' '1'
##'frame0335' '335' '335' '1' '' '' '1' '1'
##'frame0336' '336' '336' '1' '' '' '1' '1'
##'frame0337' '337' '337' '1' '' '' '1' '1'
##'frame0338' '338' '338' '1' '' '' '1' '1'
##'frame0339' '339' '339' '1' '' '' '1' '1'
##'frame0340' '340' '340' '1' '' '' '1' '1'
##'frame0341' '341' '341' '1' '' '' '1' '1'
##'frame0342' '342' '342' '1' '' '' '1' '1'
##'frame0343' '343' '343' '1' '' '' '1' '1'
##'frame0344' '344' '344' '1' '' '' '1' '1'
##'frame0345' '345' '345' '1' '' '' '1' '1'
##'frame0346' '346' '346' '1' '' '' '1' '1'
##'frame0347' '347' '347' '1' '' '' '1' '1'
##'frame0348' '348' '348' '1' '' '' '1' '1'
##'frame0349' '349' '349' '1' '' '' '1' '1'
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
##ENDJOBS

##END
