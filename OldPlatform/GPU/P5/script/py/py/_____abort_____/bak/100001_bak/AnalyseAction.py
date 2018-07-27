import os,sys,subprocess,string,logging,time,shutil
import logging
from AnalysisBase import *
from AnalysisMax import *
from AnalysisMaya import *
from AnalysisHoudini import *
from AnalysisLightWave import *
from AnalysisC4D import *
from AnalysisSoftImage import *
from AnalysisBlender import *

class AnalyseAction():
	def __init__(self,**paramDict):
		cgName=paramDict['G_CG_NAME']
		print 'cgName=================='+cgName
		exec('AnalyseAction.__bases__=('+cgName+',)')
		exec(cgName+'.__init__(self,**paramDict)')
	'''
	def RBrender(self):#Render command
		print 'AnalyseAction..max...render....'
	'''
#-----------------------main-------------------------------
def main(**paramDict):
	analyse=AnalyseAction(**paramDict)
	print 'G_POOL_NAME___'+analyse.G_POOL
	analyse.RBexecute()