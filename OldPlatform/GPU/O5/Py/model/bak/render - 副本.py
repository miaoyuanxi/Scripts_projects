#encoding:utf-8
import sys,logging

##BEGIN
##Description=This is a test script
##Name=53_12354_1.py
##TotalcoreLimit=100
##Requirements=
##Priority=50
##Custom=NONO

##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION  ##ENDJOBS



##END

logging.basicConfig(filename = 'c:/pydebug2.txt', level = logging.INFO)
logging.info('sys.argv')
logging.info(sys.argv)



G_CG_NAME='Max'
G_USERID='53'
G_TASKID='310239'
G_POOL=r'\\10.50.10.3\pool'


sys.path.append(r"\\10.50.10.3\pool\script\max")
import BaseRender


if(__name__=="__main__"):	
	paramDict = {'G_USERID':G_USERID,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION}
	BaseRender.main(**paramDict)


