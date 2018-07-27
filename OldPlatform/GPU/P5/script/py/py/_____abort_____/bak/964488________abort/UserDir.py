import logging
import os
import sys
import subprocess
import string
import logging
import time
import shutil
import codecs
import ConfigParser


def loopWorkTaskDir(workTask):
    for fileName in os.listdir(workTask):
        
        if os.path.isfile(os.path.join(workTask,fileName)):
            continue
        dirName=fileName.lower()    
        if dirName=='net':
            pass
        if dirName=='default':
            pass
        if dirName=='a'
        print dirName
        
        

    
loopWorkTaskDir(r'D:\work\render\11111\max')