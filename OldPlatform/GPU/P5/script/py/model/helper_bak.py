
import os,sys,shutil


print 'copyBasePy...start'
baseRenderPy=r'\\192.168.0.94\p\script\py\BaseHelper.py'
baseHelperPy=r'\\192.168.0.94\p\script\py\BaseRender.py'
nodePyDir=r'c:\script\py'
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
shutil.copy(baseRenderPy,nodePyDir)
shutil.copy(baseHelperPy,nodePyDir)
print 'copyBasePy...end'
#-----------------------------------------------------
#以下作为模板由平台读入
#支客户假如有定制模板，则忽略此模板
sys.path.append(nodePyDir)
import BaseHelper


if(__name__=="__main__"):
	paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL}
	BaseHelper.main(**paramDict)


##BEGIN
##description=This is a helper script
##name=helper.py
##nodelimit=100
##requirements=
##properties=
##level=98
##custom=cc

##JOBS G_JOB_ID 

##'helperJob'	

##ENDJOBS

##END
