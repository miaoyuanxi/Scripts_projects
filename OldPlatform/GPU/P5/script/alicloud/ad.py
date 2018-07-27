G_JOB_ID = 'frame1001'
G_CG_START_FRAME = '1'
G_CG_END_FRAME = '2'
G_CG_BY_FRAME = '1'
G_CG_LAYER_NAME = ''
G_CG_OPTION = ''
#encoding:utf-8
_uid = '53'
_proj = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test'
_rd = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test\renders'
_rFile = r'\\10.50.1.4\d\inputData\maya\0\53\chenzhong\of3d\forest_test\scenes\aa.mb'
_opt = 'null'
import os,sys,subprocess
cmd = r'\\10.50.8.15\p5\script\alicloud\_RV_Maya_Render.bat'
cmd += ' ' + _uid
cmd += ' ' + ''
cmd += ' ' + G_CG_START_FRAME
cmd += ' ' + G_CG_END_FRAME
cmd += ' ' + G_CG_BY_FRAME
cmd += ' ' + _proj
cmd += ' ' + _rFile
cmd += ' ' + _rd
cmd += ' ' + _opt

from subprocess import Popen
p = Popen(cmd)
stdout, stderr = p.communicate()