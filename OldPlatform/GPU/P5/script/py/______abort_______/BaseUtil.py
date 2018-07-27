import os,sys,shutil

def copyBasePy:
	print 'copyBasePy...'
	baseRenderPy=r'r'\\dataIp.com\p\script\py\BaseHelper.py'
	baseHelperPy=r'r'\\dataIp.com\p\script\py\BaseRender.py'
	nodePyDir=r'c:\script\py'
	shutil.copy(baseRenderPy,nodePyDir)
	shutil.copy(baseHelperPy,nodePyDir)