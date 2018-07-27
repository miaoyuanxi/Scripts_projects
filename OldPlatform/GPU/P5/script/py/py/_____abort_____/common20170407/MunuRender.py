#encoding:utf-8


G_SCENE_NAME=r'\\10.50.1.3\d\test.max'
G_SCENE_PROJECT=r'\\10.50.1.3\d'
G_OUTPUT=r'\\10.50.1.3\d\output'



import os,sys,shutil

munuBasePy=r'\\10.50.8.15\p5\script\py\py\MunuBase.py'
nodePyDir=r'c:/script/py/'

if not os.path.exists(nodePyDir):
    os.makedirs(nodePyDir)
os.system('xcopy /y /v "'+munuBasePy+'" "'+nodePyDir+'"')

sys.path.append(nodePyDir)

import RenderAction
if(__name__=="__main__"):	
	paramDict = {'G_SYS_ARGVS':sys.argv,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_SCENE_NAME':G_SCENE_NAME,'G_SCENE_PROJECT':G_SCENE_PROJECT,'G_OUTPUT':G_OUTPUT}
	RenderAction.main(**paramDict)

#script_param_mark#
##BEGIN
##description=This is a fast script
##name=render.py
##requirements=nono
##level=88
##custom=88
##nodelimit=8
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION 
##'frame0000' '0' '0' '1' '' ''
##'frame0001' '1' '1' '1' '' ''
##'frame0002' '2' '2' '1' '' ''
##'frame0003' '3' '3' '1' '' ''
##'frame0004' '4' '4' '1' '' ''
##'frame0005' '5' '5' '1' '' ''
##'frame0006' '6' '6' '1' '' ''
##'frame0007' '7' '7' '1' '' ''
##'frame0008' '8' '8' '1' '' ''
##'frame0009' '9' '9' '1' '' ''
##'frame0010' '10' '10' '1' '' ''
##ENDJOBS

##END
