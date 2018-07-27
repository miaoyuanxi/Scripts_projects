#encoding:utf-8

#global const var
_uid = '53'
_proj = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test'
_rd = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test\renders'
_rFile = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test\scenes\aa.mb'
_opt = 'null'

import os,sys,subprocess

#construct cmd
cmd = '_RV_Maya_Render.bat'
cmd += ' ' + _uid
cmd += ' ' + ''
cmd += ' ' + G_CG_START_FRAME
cmd += ' ' + G_CG_END_FRAME
cmd += ' ' + G_CG_BY_FRAME
cmd += ' ' + _proj
cmd += ' ' + _rFile
cmd += ' ' + _rd
cmd += ' ' + _opt

#run cmd
from subprocess import Popen
p = Popen(cmd, cwd=r"\\10.50.8.15\p5\script\alicloud")


#print quit
stdout, stderr = p.communicate()


##BEGIN
##name=
##description=
##custom=
##nodelimit=
##level=
##nodeblacklimit=
##properties=
##requirements=
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION 
##'frame1001' '1' '2' '1' '' ''
##'frame1002' '7' '9' '2' '' ''
##ENDJOBS
##END