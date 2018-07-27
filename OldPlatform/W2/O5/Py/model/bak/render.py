
import os,sys,shutil


print 'copyBasePy...start'
baseHelperPy=r'\\10.50.8.15\p5\script\py\BaseHelper.py'
baseRenderPy=r'\\10.50.8.15\p5\script\py\BaseRender.py'
nodePyDir=r'c:\script\py'
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
shutil.copy(baseRenderPy,nodePyDir)
shutil.copy(baseHelperPy,nodePyDir)
print 'copyBasePy...end'

sys.path.append(nodePyDir)
import BaseRender


if(__name__=="__main__"):	
	paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION}
	BaseRender.main(**paramDict)


##BEGIN
##description=This is a test script
##name=render.py
##requirements=
##properties=
##level=50
##custom=NONO
##nodelimit=1
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION  ##ENDJOBS

##END